#!/usr/bin/env python3
"""Checa se git / gh / python estão prontos pra usar o plugin team-ludens neste
repo. Read-only, exceto o marcador de 'setup validado' escrito só no fim, se
tudo obrigatório passar. hash scheme em sync com scripts/setup_reminder.py."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ORG = "gcarvalhow"


def marker_path(cwd):
    data_dir = os.environ.get("CLAUDE_PLUGIN_DATA") or str(
        Path.home() / ".claude" / "team-ludens" / "data"
    )
    normalized = os.path.normcase(os.path.normpath(cwd))
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]
    return Path(data_dir) / "setup-status" / f"{digest}.json"


def run(args):
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=30)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as exc:  # noqa: BLE001
        return 1, str(exc)


class Check:
    def __init__(self, name, ok, detail, remediation):
        self.name = name
        self.ok = ok
        self.detail = detail
        self.remediation = remediation


def check_git():
    if not shutil.which("git"):
        return Check("git instalado", False, "não encontrado no PATH",
                     "instale o git: https://git-scm.com/downloads")
    code, out = run(["git", "rev-parse", "--is-inside-work-tree"])
    if code != 0:
        return Check("git — repositório", False, "diretório atual não é um repo git",
                     "rode este comando de dentro de um clone de um repo *.ludens")
    code, out = run(["git", "remote", "get-url", "origin"])
    if code != 0 or "ludens" not in out:
        return Check("git — remote origin", False, f"origin: {out.strip() or 'ausente'}",
                     "confirme que o clone é de um repo gcarvalhow/*.ludens")
    return Check("git", True, out.strip(), "")


def check_gh():
    if not shutil.which("gh"):
        return Check("gh instalado", False, "não encontrado no PATH",
                     "instale o GitHub CLI: https://cli.github.com")
    code, out = run(["gh", "auth", "status"])
    if code != 0:
        return Check("gh — autenticado", False, out.strip(),
                     "rode `gh auth login` (fora desta sessão — é interativo)")
    code, out = run(["gh", "repo", "view", f"{ORG}/docs.ludens", "--json", "name"])
    if code != 0:
        return Check("gh — acesso à org", False, out.strip(),
                     f"a conta autenticada não enxerga {ORG}/docs.ludens — cheque os escopos do token")
    return Check("gh", True, "autenticado e enxerga gcarvalhow/*.ludens", "")


def check_python():
    if sys.version_info < (3, 10):
        return Check("python >= 3.10", False, f"versão atual {sys.version.split()[0]}",
                     "as skills usam scripts Python 3.10+ — atualize o python do PATH")
    return Check("python", True, sys.version.split()[0], "")


def main():
    checks = [check_git(), check_gh(), check_python()]
    print("== team-ludens :: checagem de ambiente ==\n")
    all_ok = True
    for c in checks:
        mark = "OK  " if c.ok else "FALHA"
        print(f"[{mark}] {c.name}: {c.detail}")
        if not c.ok:
            all_ok = False
            print(f"        → {c.remediation}")
    print()
    if all_ok:
        path = marker_path(os.getcwd())
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"validated": True}), encoding="utf-8")
        print("Tudo obrigatório passou. Marcador salvo — o lembrete de SessionStart não aparece mais neste repo.")
    else:
        print("Corrija os itens em FALHA e rode /team-ludens:setup de novo.")
        sys.exit(1)


if __name__ == "__main__":
    main()
