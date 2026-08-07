# CLAUDE.md — Lingotran QA Engineering Field Manual

Standing context for this repo. Read before any edit.

**Also read `CONTEXT.md`** — it records *why* these rules exist and which structural
changes have already been considered and rejected. This file is the *what*; that one is
the *why*. If a rule here seems arbitrary, the reasoning is there.

---

## 1. What this is

A single-file HTML reference manual for QA engineers working on **Lingotran** — a
language-learning platform sold to schools and institutions.

It is a **field manual, not a textbook.** It is meant to be filtered and searched at a
desk mid-task, never read front to back. Every design and content decision follows from
that.

**Deliverable:** `dist/lingotran-qa-field-manual.html` — one file, no build dependencies,
no external JS, opens by double-click.

---

## 2. Hard rules — do not violate

1. **Lingotran is the only product discussed.** Every example, scenario, user, domain,
   table, endpoint, bug, and incident is Lingotran. Never introduce Microsoft, Amazon,
   Netflix, Atlassian, Adobe, Shopify, Duolingo, Babbel, Rosetta Stone, or any other
   company as *subject matter*.
   - **Allowed exception:** tool and platform names that make up the stack — React,
     Node, Express, PostgreSQL, Azure, Azure DevOps, Playwright, Postman, Bruno, k6,
     JMeter, axe, NVDA, VoiceOver. These are the environment, not competing products.
   - **Google is now in that exception.** Speech runs on the browser Web Speech API,
     which is Google-backed. Google is a real sub-processor for learner audio, so it
     must be nameable — plainly, in the architecture and in the privacy checks. It was
     previously banned outright; that restriction was correct only while Google was not
     part of the stack.
2. **Shashi Kumar** is the standing QA engineer in every worked example. No other
   invented tester names.
3. **Spelling is `Lingotran`** — lowercase `t`. Never `LingoTran`. The only lowercase
   form permitted is inside the hostname `api.lingotran.com`.
4. **Light theme only.** No dark backgrounds anywhere except the hero gradient. Code
   blocks are light (`--code-bg`), never dark.
5. **Page ceiling: 50.** Currently ~28.4. Measure with `scripts/verify.py` after any
   content change. If a change pushes past 50, cut before shipping.
6. **Customer domains are `school.edu`.** Learner emails, teacher emails, test fixtures.
7. **Never build from `archive/`.** It holds the superseded 30-page Chapter 1 written to
   an abandoned template, and deliberately contains every banned pattern. Reference
   only — see `archive/README.md`.

---

## 3. Content ratio — the thing that makes it a manual

Target roughly **75% tables and code, 25% prose.** Current mix:

| Component | Volume | Pages |
|---|---|---|
| Prose | 3,840 words | 8.0 |
| Code | 363 lines | 7.0 |
| Tables | 403 rows | 13.4 |
| **Total** | | **28.4** |

Page maths used by `verify.py`: prose ÷ 480 wpp, code ÷ 52 lines/pp, tables ÷ 30 rows/pp.

**When adding content, prefer a table.** Prose is for connective tissue and for the
judgement calls a table cannot hold. If a new section is mostly paragraphs, it is
probably textbook filler — cut it or convert it.

`verify.py` fails below **70%**. The mix is currently 72%, so the guard is live rather
than theoretical: a prose-heavy addition will fail the build, not merely drift. Callout
boxes count as prose — they are worth their cost when they name a failure mode, but
three boxes and an intro paragraph will move the ratio a full point.

**Banned section types** (they were deliberately removed and must not come back):
Learning Objectives · Why This Topic Matters · Chapter Summary · Knowledge Check
questions · Business Perspective as its own section.

---

## 4. Design system

Derived from `assets/lingotran-brand-guidelines.html`. That file is authoritative — read
it before changing any colour or type decision.

```css
--brand-purple:#41009A;  --violet:#7C4DFF;  --pill-purple:#412485;
--ink:#1A1A2E;  --ink-deep:#1A0B2E;  --body:#3C3C46;  --muted:#666;
--border:#E2E2E8;  --lilac:#F0E6FF;  --cream:#FAF6F0;  --off-white:#FAFAFA;
--coral-text:#DC2800;  --success-text:#008168;  --alert-text:#E60000;  --caption-safe:#727272;
--code-bg:#FBF9FF;  --code-br:#E4D9FA;  --code-ink:#2A1B45;
font: 'Nunito' — 900 logo · 800 headings · 700 subheads/pills · 600 buttons · 500 body
```

**Accessibility, non-negotiable** (from the brand guidelines):
- Never put raw `--coral`, `--success`, `--alert`, or `--caption` as text on a light
  background — they fail WCAG AA. Use the `-text` siblings.
- Text on the brand gradient is **white only**.
- Every interactive element needs a visible `:focus-visible` ring, 3px solid `#41009A`.
- Motion wrapped in `@media (prefers-reduced-motion:reduce)`.

---

## 5. Component patterns

Reuse these. Do not invent new ones without reason.

| Pattern | Markup | Use for |
|---|---|---|
| Module | `<details class="mod" id="mNN"><summary><span class="n">NN</span> Title<span class="pp">N p</span></summary><div class="inner">` | Every top-level module |
| Layer trace | `.trace > .lyr > .i / .l / .v` | The signature device — layer, file, what QA validates |
| Callout | `.box` / `.box.warn` / `.box.good` with `<b class="bl">LABEL</b>` | Judgement calls, traps, rules |
| Code | `<div class="fn">path/file.ts</div><pre>` | Any code sample; `<b>` keyword, `<i>` comment, `<u>` the line that matters |
| Table | `.tw > table` | Default for everything |
| Pill | `.pill` | Inline tags |

**Module IDs are `m00`–`m13`** and must stay in sync with the `.toc` list and the module
count in the hero. `verify.py` enforces all three.

**Background motion.** The `.bgfx` layer (three blurred drifting blobs) and the hero
gradient shift are CSS-only. They inherit the global `prefers-reduced-motion` kill switch
and are suppressed in `@media print`. Keep both properties for anything new.

---

## 6. Voice

- Second person, present tense, imperative where it is an instruction.
- State the consequence, not the definition. "Two instances → real limit is 20/min" beats
  "rate limiting restricts request frequency."
- Every claim earns its place by changing what the reader does next.
- Name the failure mode. The most valuable sentences in the manual are the ones that say
  *why a defect escapes*, not what the defect is.
- No motivational framing, no "in today's fast-paced world", no restating the heading.

---

## 7. Build

Source is split into six ordered fragments in `src/`. They concatenate into one file —
fragment 1 carries `<head>` and opens `<body>`, fragment 6 closes them.

```bash
bash scripts/build.sh      # concat src/*.html -> dist/lingotran-qa-field-manual.html
python3 scripts/verify.py  # tag balance, page count, compliance checks
```

`verify.py` must pass clean before shipping. It checks:
- every tag balanced (details, table, tr, td, div, pre, summary, p)
- page count under the 50 ceiling
- zero `LingoTran` typos
- zero competing-product references
- Shashi Kumar present
- the filter script parses

---

## 8. Current state

**Complete — 14 modules, ~28.4 pages:**

| # | Module | Pages |
|---|---|---|
| 00 | How to use this manual | 1 |
| 01 | The QA operating model | 6 |
| 02 | Lingotran architecture & the layer trace | 5 |
| 03 | Requirements to test design | 4 |
| 04 | Frontend testing · React | 4 |
| 05 | API testing · Node & Express | 4 |
| 06 | Database testing · PostgreSQL | 4 |
| 07 | The speech pipeline | 6 |
| 08 | Automation · ATDD to pipeline | 5 |
| 09 | Performance, security, accessibility | 5 |
| 10 | Defects, RCA & production | 5 |
| 11 | AI-assisted QA | 6 |
| 12 | Templates & checklists | 4 |
| 13 | Claude Code · skills, subagents & the QA pipeline | 5 |

*(Per-module page labels in `<span class="pp">` are indicative, set by hand. The real
total comes from `verify.py`.)*

**~22 pages of headroom** against the 50 ceiling.

**Open / candidates for the headroom:**
- Module 08 — Playwright fixture patterns, sharding, trace-on-failure triage.
- Teacher and institution admin — class management, enrolment, seat limits, role
  boundaries, progress reports. Still thin, and where renewal is decided. Note the
  `m13` slot is now taken by the Claude Code module; this would be `m14`.
- Real screenshots of the lesson player (none present; all diagrams are ASCII/CSS).
- Replace the ASCII architecture diagram in 2.1 with inline SVG using brand tokens.

---

## 9. Domain facts — keep consistent

- **Stack:** React + TypeScript SPA (Azure Static Web Apps) · Node/Express API (Azure App
  Service, **2 instances**) · PostgreSQL 15 Flexible Server · Azure Blob for audio ·
  **browser Web Speech API** (Google-backed ASR/STT, plus `speechSynthesis` for TTS —
  runs client-side, so learner audio leaves the device to Google, not via our API) ·
  Application Insights · Azure DevOps.
- **The institution multiplier:** ~30 learners per class share **one NAT IP** on shared
  devices, many on iPad Safari. This drives the rate-limiter incident, the k6 single-IP
  load profile, and the risk scoring. It is the single most important contextual fact.
- **Many learners are minors** — cross-account data exposure is a safeguarding incident
  with regulatory weight, not a normal Sev-2.
- **Known defect class:** pronunciation scoring has historically penalised
  accented-but-correct speech (systematic false negatives against the core user base).
  Guarded by REF-02 in the reference corpus.
- **IDs:** stories `LT-nnnn` · incidents `LT-INC-nnnn` · defects `LT-nnnn` ·
  test cases `LT-F01` (frontend) etc.
- **Recurring examples:** story `LT-1187` extended sessions · incident `LT-INC-0219`
  NAT rate-limiter outage · defect `LT-4471` attempt limit resets on reload.
- **REF corpus:** REF-01 native clean · REF-02 accented correct · REF-03 noisy ·
  REF-04 wrong words fluent · REF-05 partial · REF-06 silence · REF-07 wrong language ·
  REF-08 60s boundary.
