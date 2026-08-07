#!/usr/bin/env python3
"""
PreToolUse guard for Bash commands touching a database.

Blocks, deterministically and regardless of what the model intends:
  - any write/DDL statement issued through psql or a connection string
  - any command referencing a production host or the prod database name
  - obvious credential literals on the command line

Exit 0 = allow. Exit 2 = block, and stderr is shown to Claude as the reason.

Wired from .claude/settings.json as a PreToolUse hook on Bash.
Scoped narrowly on purpose: commands with no database or credential marker are
never inspected, so ordinary development is untouched.
"""
import json
import re
import sys

# Only inspect commands that actually look database- or credential-shaped.
TRIGGERS = re.compile(
    r"\b(psql|pg_dump|pg_restore|pgcli|postgres(?:ql)?://|PGPASSWORD|DATABASE_URL)\b",
    re.I,
)

WRITE_SQL = re.compile(
    r"\b(INSERT\s+INTO|UPDATE\s+\w|DELETE\s+FROM|TRUNCATE|DROP\s+(TABLE|DATABASE|SCHEMA|INDEX)"
    r"|ALTER\s+(TABLE|DATABASE|SCHEMA)|CREATE\s+(TABLE|DATABASE|SCHEMA|INDEX)"
    r"|GRANT|REVOKE|COMMIT|ROLLBACK)\b",
    re.I,
)

# Production markers. Staging and local are explicitly allowed.
PROD_HOST = re.compile(
    r"(prod|production)[-.\w]*\.(postgres\.database\.azure\.com|lingotran\.com)"
    r"|\blingotran-prod\b"
    r"|\bapi\.lingotran\.com\b",
    re.I,
)

SECRET = re.compile(
    r"(PGPASSWORD\s*=\s*[\"']?[^\s\"';]{6,})"
    r"|(://[^:/\s]+:[^@/\s]{6,}@)",  # user:password@host
    re.I,
)


def block(reason: str, fix: str) -> None:
    print(f"BLOCKED by .claude/hooks/guard-db.py\n\n{reason}\n\n{fix}", file=sys.stderr)
    sys.exit(2)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0  # never fail closed on a malformed payload

    if payload.get("tool_name") != "Bash":
        return 0

    cmd = (payload.get("tool_input") or {}).get("command", "")
    if not cmd or not TRIGGERS.search(cmd):
        return 0

    if PROD_HOST.search(cmd):
        block(
            "This command references a Lingotran production host.",
            "Production is read-only smoke against the canary account, never a shell. "
            "Point at staging or a local container instead.",
        )

    if WRITE_SQL.search(cmd):
        stmt = WRITE_SQL.search(cmd).group(0).upper()
        block(
            f"This command contains a write or DDL statement ({stmt}).",
            "Validation queries are SELECT-only. If a check genuinely needs a write, "
            "say so and let a human run it deliberately.",
        )

    if SECRET.search(cmd):
        block(
            "This command appears to carry a credential inline.",
            "Use an environment variable or .pgpass. A credential on the command line "
            "lands in shell history and in the transcript.",
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
