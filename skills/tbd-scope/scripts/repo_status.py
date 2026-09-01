#!/usr/bin/env python3
"""Estado real do projeto Ludens: issues abertas nos repos *.ludens + itens do
Project @ludens que casem as palavras-chave. Read-only (só `gh`)."""
import json
import subprocess
import sys

ORG = "gcarvalhow"
REPOS = ["api.ludens", "web.ludens", "docs.ludens", "team.ludens"]
PROJECT_NUMBER = "2"


def run(args):
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return result.stdout


def search_issues(keywords):
    query = " ".join(keywords)
    print(f"== Issues abertas casando: {query!r} ==")
    found = False
    for repo in REPOS:
        out = run([
            "gh", "issue", "list", "--repo", f"{ORG}/{repo}", "--state", "open",
            "--search", query, "--json", "number,title,url", "--limit", "20",
        ])
        if not out:
            continue
        items = json.loads(out)
        for it in items:
            found = True
            print(f"  {repo}#{it['number']}: {it['title']}\n    {it['url']}")
    if not found:
        print("  (nada encontrado)")


def project_items(keywords):
    print(f"\n== Itens do Project @{ORG}/{PROJECT_NUMBER} casando: {' '.join(keywords)!r} ==")
    out = run([
        "gh", "project", "item-list", PROJECT_NUMBER, "--owner", ORG,
        "--format", "json", "--limit", "200",
    ])
    if not out:
        print("  (não foi possível ler o Project)")
        return
    items = json.loads(out).get("items", [])
    lowered = [k.lower() for k in keywords]
    hits = [
        it for it in items
        if any(k in json.dumps(it, ensure_ascii=False).lower() for k in lowered)
    ]
    if not hits:
        print("  (nada encontrado)")
        return
    for it in hits:
        title = it.get("title", "?")
        status = it.get("status", "-")
        repo = it.get("repository", "-")
        print(f"  [{status}] {repo}: {title}")


def main():
    keywords = sys.argv[1:]
    if not keywords:
        print("uso: repo_status.py <palavra-chave> [palavra-chave ...]")
        sys.exit(1)
    search_issues(keywords)
    project_items(keywords)


if __name__ == "__main__":
    main()
