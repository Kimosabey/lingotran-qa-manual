# HANDOFF — paste this into Claude Code

Unzip this folder anywhere on your PC, `cd` into it, run `claude`, and paste the block
below as your first message. Claude Code reads `CLAUDE.md` automatically, so the prompt
stays short on purpose — the rules live in the file, not in the prompt.

---

## First message

```
I'm continuing work on the Lingotran QA Engineering Field Manual in this repo.

Read these first, in order:
  1. CLAUDE.md  — the hard rules, design tokens, component patterns, current state
  2. CONTEXT.md — why those rules exist, and which structural changes have already
                  been considered and rejected
  3. dist/lingotran-qa-field-manual.html — the built artifact
  4. assets/lingotran-brand-guidelines.html — the authoritative brand system

Ignore archive/ except as historical reference — it holds a superseded 30-page chapter
written to an abandoned template, and deliberately contains patterns that are now banned.

Workflow for every change:
1. Edit the relevant fragment in src/ — never edit dist/ directly, it is generated.
2. Run: bash scripts/build.sh
3. Run: python3 scripts/verify.py
4. Do not consider a change done until verify passes clean.

The manual is currently ~28 pages against a 50-page ceiling, so there is room, but
verify.py FAILS below 70% tables and code and the mix is ~71%. Prefer a table over
paragraphs every time — a prose-heavy addition will fail the build, not merely drift.

Before you change anything, give me a one-paragraph summary of what you understand
the manual to be, plus the one decision in CONTEXT.md you think is most at risk of
being accidentally reversed. Don't start editing until I confirm.
```

---

## Why it's shaped this way

- **`CLAUDE.md` carries the rules, not the prompt.** Claude Code re-reads it every
  session, so the constraints survive context resets. A long pasted prompt does not.
- **The "summarise before editing" step** catches a misread cheaply. If it comes back
  describing a generic QA textbook, correct it before any file is touched.
- **`verify.py` is the contract.** It encodes the rules that are easy to violate by
  accident — the page ceiling, the prose/table ratio, the `Lingotran` spelling, the
  banned textbook sections, competing-product references. Gate on it.

---

## Folder layout

```
lingotran-qa-manual/
├─ CLAUDE.md            standing rules — Claude Code reads this automatically
├─ CONTEXT.md           decision log — WHY the rules exist, what was rejected
├─ HANDOFF.md           this file
├─ src/                 six ordered HTML fragments — EDIT THESE
│  ├─ 01-shell-00-01.html    <head>, CSS, nav, hero, TOC, modules 00–01
│  ├─ 02-mod-02-03.html      architecture + layer trace, requirements
│  ├─ 03-mod-04-06.html      React, Node/Express, PostgreSQL
│  ├─ 04-mod-07-08.html      speech pipeline, automation
│  ├─ 05-mod-09-11.html      non-functional, defects/RCA, AI-assisted QA
│  └─ 06-mod-12-close.html   templates/checklists, footer, filter script
├─ dist/
│  └─ lingotran-qa-field-manual.html   GENERATED — do not edit
├─ .claude/             the tooling the manual describes, as real files
│  ├─ skills/           lt-pr-trace · lt-story-interrogate · lt-sql-guard
│  ├─ agents/           pr-triage · flake-hunter
│  ├─ hooks/guard-db.py deterministic PreToolUse gate (blocks writes/prod/secrets)
│  └─ settings.json     wires the hook, allowlists the build
├─ README.md            public-facing overview
├─ vercel.json          static deploy — / serves the manual
├─ archive/             superseded 30-page chapter — reference only, never build from
├─ assets/
│  └─ lingotran-brand-guidelines.html  authoritative colour/type reference
└─ scripts/
   ├─ build.sh          concat src/*.html -> dist/
   └─ verify.py         tag balance, page budget, ratio, compliance
```

Fragments concatenate in filename order. Fragment `01` opens `<head>` and `<body>`;
fragment `06` closes them. If you add a fragment, name it so it sorts into the right
position, and keep module IDs (`m00`–`m13`) in sync with the TOC in fragment 01.

---

## Suggested next tasks

Pick one — ordered by value, not effort.

1. **Module 08 — Playwright fixtures.** Auth fixtures, per-worker database isolation,
   sharding, triaging a failed trace. The largest remaining content gap.
2. **Teacher and institution admin** — class management, enrolment, seat limits, role
   boundaries, progress reports. Where renewal is decided. This would be `m14`; `m13`
   is taken by the Claude Code module.
3. **Replace the ASCII architecture diagram** in 2.1 with inline SVG, matching the
   animated flow already in 13.5.
4. **Plain-English pass** over Modules 01–06 and 08–12. Module 07 has had one; the
   rest have not.


---

## Guardrails worth restating

- Everything is **Lingotran**. Stack tool names are fine; other companies as subject
  matter are not.
- **Shashi Kumar** is the QA engineer in examples.
- **Light theme only.** Code blocks light, never dark.
- **No textbook sections** — no Learning Objectives, Why This Matters, Chapter Summary,
  or Knowledge Check. `verify.py` fails the build if they reappear.
- If a change pushes past **50 pages**, cut something before shipping.
