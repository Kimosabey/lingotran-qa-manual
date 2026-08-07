# AGENTS.md — one standard, whichever tool you drive

Tool-agnostic entry point. Claude Code, Cursor, Antigravity and anything else agentic
should be pointed here. **The standard lives in this repo, not in a tool's settings** —
otherwise three tools grow three divergent copies of the house rules and the one a
teammate uses is the one you never reviewed.

## Read these first

| File | What it carries |
|---|---|
| `CLAUDE.md` | The hard rules, design tokens, current state |
| `CONTEXT.md` | Why those rules exist, and what was already rejected |
| `.claude/skills/` | Repeatable procedures — PR tracing, story interrogation, SQL |
| `.claude/agents/` | Read-only fan-out workers |

## The rules that do not bend

1. **Lingotran is the only product discussed.** Stack tools are fine as the environment.
2. **Never edit `dist/`.** It is generated. Edit `src/`, run `bash scripts/build.sh`.
3. **`python scripts/verify.py` must pass before anything is considered done.**
4. **SELECT-only against a database, and never production.** Enforced by
   `.claude/hooks/guard-db.py` under Claude Code; every other tool must honour it by
   convention, because the hook cannot reach them.
5. **Never paste learner audio, learner names, credentials or connection strings** into
   any prompt. Learners are children. Redact to IDs and correlation IDs.
6. **Agents propose, deterministic checks dispose.** Nothing an agent says turns a gate
   green. If it can, it was never a gate.

## Division of labour

| Tool | Use it for | Do not use it for |
|---|---|---|
| **Claude Code** | Repo-wide work, running the build and verify, fan-out review, anything that must be gated | — |
| **Cursor** | Writing and refactoring individual spec files, in-editor speed | Multi-file agentic runs that need a gate |
| **Antigravity** | Driving a real browser, capturing evidence, exploratory support | Anything whose result is trusted without a human reading it |

Only Claude Code carries the deterministic hook. **Gating stays there.** The other tools
are accelerators, and their output re-enters through the same pipeline as anyone else's.

## Before you claim something works

Run it. `bash scripts/build.sh && python scripts/verify.py`. A green verify is a fact;
"this should work" is not.
