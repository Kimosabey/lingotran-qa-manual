# Lingotran · QA Engineering Field Manual

A single-file HTML reference manual for QA engineers working on **Lingotran**, a
language-learning platform sold to schools and institutions.

**Live:** https://lingotran-qa-manual.vercel.app

It is a **field manual, not a textbook** — meant to be filtered and searched at a desk
mid-task, never read front to back. Thirteen collapsible modules behind a live filter
box. Every design and content decision follows from that one constraint.

---

## The artifact

`dist/lingotran-qa-field-manual.html` — one file, no build dependencies, no external
JS, opens by double-click and prints straight into a doc.

| | |
|---|---|
| Modules | 14 (`m00`–`m13`) |
| Length | 33.6 pages against a 50-page ceiling |
| Content mix | 70% tables and code |
| Theme | Light only, Nunito, brand tokens from `assets/` |

---

## Layout

```
├─ CLAUDE.md      standing rules — the what
├─ CONTEXT.md     decision log — the why, and what was already rejected
├─ HANDOFF.md     how to pick this up in a new session
├─ src/           six ordered HTML fragments — EDIT THESE
├─ dist/          GENERATED single-file artifact — never edit directly
├─ scripts/       build.sh (concat) · verify.py (the contract)
├─ assets/        authoritative brand guidelines
└─ archive/       superseded 30-page chapter — reference only, never build from
```

Fragments concatenate in filename order. Fragment `01` carries `<head>` and opens
`<body>`; fragment `06` closes them.

---

## Working on it

```bash
# 1. edit the relevant fragment in src/
bash scripts/build.sh      # concat src/*.html -> dist/
python3 scripts/verify.py  # gate — must pass clean before shipping
```

`verify.py` is the contract, not a formality. It fails the build on:

| Check | Why it exists |
|---|---|
| Tag balance across 10 tag types | A single unclosed `<div>` silently breaks the filter |
| Page count under 50 | An unread manual has zero quality impact |
| Structured content ≥ 70% | Prose drift turns a field manual back into a textbook |
| Hero facts match reality | The module and page counts in the hero silently went stale once |
| `LingoTran` spelling | Lowercase `t`, always |
| Competing-product references | Every example is Lingotran |
| Shashi Kumar present | The standing QA engineer in worked examples |
| Banned textbook sections | Learning Objectives · Why This Topic Matters · Chapter Summary · Knowledge Check |
| `prefers-reduced-motion` + `:focus-visible` | Accessibility guards from the brand system |

**Read `CONTEXT.md` before proposing structural changes.** Most have already been
considered and rejected, with the reasoning recorded — including the original
34-section template that projected to ~1,200 pages and was abandoned.

---

## Versions and branches

| Branch / tag | Role |
|---|---|
| `main` | **Released.** Vercel deploys this to production on every push |
| `develop` | Working branch. Merge to `main` to release |
| `vN.N.N` | Tagged release. `v3.0.0` is current |

Revision in the hero and footer tracks the tag — bump both together.

| Version | What changed |
|---|---|
| `v3.0.0` | Speech corrected to the browser Web Speech API; Modules 07 and 13 expanded; dev/UAT confirmed HTTP; `.claude/` toolchain shipped; cream editorial theme; WCAG 1.4.1 fixed; `verify.py` hardened |
| `v2.0` | The 14-module field manual, rebuilt from the abandoned handbook template |

Because `main` deploys straight to production, **`verify.py` must pass before merging.**
It has caught a stale hero, four ratio breaches and a destroyed logo already.

## Deployment

Static. `vercel.json` points the output directory at `dist/` and rewrites `/` to the
manual, so the root URL serves it directly. Any push to `main` redeploys.
