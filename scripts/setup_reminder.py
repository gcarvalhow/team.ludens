import hashlib
import json
import os
import sys
from pathlib import Path

# hash scheme deve ficar em sync com skills/setup/scripts/check_environment.py


def marker_path(cwd):
    data_dir = os.environ.get("CLAUDE_PLUGIN_DATA") or str(Path.home() / ".claude" / "team-ludens" / "data")
    normalized = os.path.normcase(os.path.normpath(cwd))
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]
    return Path(data_dir) / "setup-status" / f"{digest}.json"


def main() -> None:
    try:
        payload = json.load(sys.stdin)
        cwd = payload.get("cwd", "")
        if not cwd:
            return
        if marker_path(cwd).exists():
            return
        print(json.dumps({
            "systemMessage": (
                "Setup do plugin team-ludens ainda não validado neste repo. "
                "Rode /team-ludens:setup pra checar git/gh/python antes de usar o fluxo TBD."
            )
        }))
    except Exception:
        return


if __name__ == "__main__":
    main()
