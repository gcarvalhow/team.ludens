import re
import sys
import json

MUTATING_PATTERNS = [
    r"\bgit\s+push\b",
    r"\bgit\s+commit\b",
    r"\bgit\s+merge\b",
    r"\bgit\s+rebase\b",
    r"\bgit\s+reset\b",
    r"\bgh\s+(issue|pr)\s+(create|edit|close|comment|merge)\b",
    r"\bgh\s+project\s+(item-add|item-edit|item-create|edit|field-create)\b",
    r"\bgh\s+api\s+.*-X\s*(POST|PUT|PATCH|DELETE)\b",
    r"\balembic\s+(upgrade|downgrade)\b",
]


def main() -> None:
    payload = json.load(sys.stdin)
    if payload.get("tool_name") != "Bash":
        return

    command = payload.get("tool_input", {}).get("command", "")
    for pattern in MUTATING_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": (
                        "Este agente é consultivo e somente leitura — comando de mutação "
                        f"bloqueado: `{command}`. Explique o que precisaria rodar e devolva "
                        "isso como recomendação, não execute."
                    ),
                }
            }))
            return


if __name__ == "__main__":
    main()
