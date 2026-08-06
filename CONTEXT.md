# CONTEXT.md — how this manual got its shape

Decision history from the originating sessions. Read this before proposing structural
changes — most of them have already been considered and rejected for reasons recorded
here.

`CLAUDE.md` says *what* the rules are. This file says *why*, so you can tell a
principled exception from an accidental violation.

---

## The original brief, and why it was abandoned

The project started from a "Senior QA Engineering Handbook (Enterprise Edition)" master
prompt specifying:

- 35–45 chapters, 8–15 pages each
- **34 mandatory sections in every chapter** — Introduction, Learning Objectives, Why
  This Topic Matters, Enterprise Concepts, Architecture Diagram, Workflow Diagram,
  Step-by-Step Process, QA/Developer/Business Perspectives, Source Code Walkthrough,
  API Walkthrough, Database Walkthrough, Azure DevOps Perspective, Example Scenario,
  Positive/Negative/Boundary/Equivalence/Security test cases, Performance, Accessibility,
  Common Production Bugs, RCA, Risk Analysis, Regression Scope, Automation
  Opportunities, AI Assistance, Common Mistakes, Best Practices, Senior QA Tips,
  Checklist, Chapter Summary, Knowledge Check
- One chapter at a time, approval between each

**Chapter 1 was built to that spec in full.** It is preserved in
`archive/chapter-01-superseded.html`.

Then it was measured:

| | |
|---|---|
| Chapter 1 as built | **30 pages** (13,491 words, 18 code blocks, 25 tables) |
| Spec ceiling per chapter | 15 pages |
| Overrun | **2×** |
| Projected total at 40 chapters | **~1,200 pages** |
| Sessions required | ~40 |

The 34-section template was the cause. Thirty-four sections × ~400 words is 13,000 words
before a single table or code block exists. The template *guarantees* the overrun —
it is not a discipline problem.

**Decision:** abandon the chapter/section model entirely. Rebuild as a field manual of
13 modules at ~20 pages total.

**Rationale:** a 1,200-page handbook is not read, and an unread handbook has zero
quality impact regardless of how good it is. The binding constraint on a QA reference is
not comprehensiveness — it is whether someone opens it mid-task.

---

## Decision log

### D1 · Field manual, not handbook
Reference to be filtered and searched at a desk, never read front to back. Everything
else follows from this. Rejected alternatives: 24 chapters at ~14 pages (~340 pages),
and tiered templates (~700 pages). Both still too large to be opened mid-task.

### D2 · ~75% tables and code
Measured mix: 2,455 prose words / 248 code lines / 289 table rows. Prose is connective
tissue and judgement calls only. **If a new section is mostly paragraphs, it is textbook
filler.** `verify.py` fails below 60% structured content.

### D3 · Eight section types banned outright
Learning Objectives · Why This Topic Matters · Chapter Summary · Knowledge Check ·
Business Perspective as its own section · Developer Perspective as its own section ·
Step-by-Step Process as its own section · Equivalence Partitioning separate from
Boundary Values.

Measured cost in Chapter 1: Knowledge Check 1.02pp, Step-by-Step 0.89pp, Why This
Matters 0.70pp, Chapter Summary 0.64pp, Learning Objectives 0.32pp — all pure prose,
zero tables, zero code. They restate the heading or serve a course format this is not.

`verify.py` fails the build if any reappear. **This is the rule most likely to be
violated by accident**, because "expand this module" naturally invites re-adding them.

### D4 · Glossary written once, not per chapter
The original template repeated Enterprise Concepts (QA/QC/QE, shift-left, test pyramid)
in every chapter — 2.08pp × 40 chapters ≈ 83 pages of restated definitions. Now a single
table in Module 12.7.

### D5 · TDD is literacy, not a chapter
Test-Driven Development is a developer inner-loop practice. QA never runs red-green-
refactor. Giving it a chapter teaches a ritual the reader will never perform and implies
QA should be writing unit tests for React components.

**What QA actually needs** is the ability to read a test-driven PR and judge it — four
questions, now in Module 8.1. **ATDD is the QA-owned equivalent**: acceptance criteria
as Given/When/Then agreed before the sprint, realised as Playwright specs. Same
tests-first discipline, at the layer where QA has authority.

Do not add a standalone TDD chapter. This was argued and settled.

### D6 · The layer trace is the signature device
Module 2.2 — eleven rows from `LessonPlayer.tsx` down to the JSON envelope, each stating
what QA validates there. Used as a diff checklist: mark the layers a PR touches, test
those plus everything downstream.

Every other module hangs off it. Module 12.4's PR checklist references it directly.
**Do not restructure it without restructuring what depends on it.**

### D7 · Lingotran only
Every example, user, domain, table, endpoint, bug, and incident is Lingotran. The
original master prompt named Microsoft, Google, Amazon, Atlassian, Netflix, Adobe and
Shopify — but as a *style* reference ("write like an internal manual at…"), never as
content. That framing correctly never entered the text.

Stack tools are exempt: React, Node, Express, PostgreSQL, Azure, Azure DevOps,
Playwright, Postman, Bruno, k6, JMeter, axe, NVDA, VoiceOver. They are the environment
being tested, not competing products.

Placeholder domains were unified onto `school.edu` — `x.com` was removed because it is
now a real product.

### D8 · Shashi Kumar
Standing QA engineer in worked examples. Currently in 6 places. `John Smith` appears
once in the original Chapter 1 as a deliberate counter-example about unrepresentative
test data ("our users are not John Smith") — that inversion is the point and was left
intact there.

### D9 · Light theme, HTML, single file
No dark surfaces except the hero gradient. Code blocks light (`--code-bg`), which
departs from the brand guidelines' dark `pre` — a deliberate override, requested
explicitly.

HTML chosen over PDF/docx: searchable, filterable, no build dependency, prints to Google
Docs when needed via the `@media print` rule that force-expands collapsed modules.

### D10 · Collapsible modules + live filter
The manual opens as a one-screen index. The filter hides non-matching modules and
highlights hits inline. This is what makes 20 pages behave like a reference rather than
a document.

### D11 · 50-page ceiling
Currently 19.5. Headroom is for depth in existing modules, not new breadth. If a change
pushes past 50, cut before shipping.

---

## Domain reasoning worth preserving

**The institution multiplier.** Lingotran sells to schools. ~30 learners per class share
one NAT IP on shared devices, many on iPad Safari. Every defect is multiplied by class
size before anyone notices. This single fact drives the rate-limiter incident
(LT-INC-0219), the k6 single-source-IP load profile, the risk scoring in Module 1.3, and
the "test from one IP" rule. **It is the most important contextual fact in the manual.**

**Minors.** A large share of learners are children. Cross-account exposure of identity,
audio, or progress is a safeguarding incident with regulatory weight — not a normal
Sev-2. Module 9.2 says this explicitly and it should not be softened.

**The accent false-negative.** Pronunciation scoring has historically penalised
accented-but-correct speech — systematic false negatives against exactly the core user
base. Invisible to any suite using native-speaker clips or stubbed responses, because
the stub always returns a good score. Guarded by REF-02 in the reference corpus with a
permanent floor assertion. **This is the highest-value single check in the manual.**

**Check-then-act.** Module 5.3's attempt-limit race is the template for a whole defect
class: read a count, decide, then write, non-atomically. Sequential testing can never
find it. Wherever this pattern appears, the test is two simultaneous requests asserting
exactly one succeeds.

---

## ⚠ About `archive/chapter-01-superseded.html`

Kept for reference only. It is the 30-page original built to the abandoned 34-section
template.

**It deliberately contains every pattern now banned** — Learning Objectives, Why This
Topic Matters, Chapter Summary, Knowledge Check, per-chapter Enterprise Concepts.

**Do not use it as a style reference. Do not copy its structure. Do not merge it into
`src/`.** Its value is the worked content — the LT-1187 story interrogation, the
LT-INC-0219 RCA, the production-bug escape table — all of which has already been carried
across into the modules in denser form.

If asked to "restore" or "expand back to" the original format, point at this file and
the 1,200-page projection first.
