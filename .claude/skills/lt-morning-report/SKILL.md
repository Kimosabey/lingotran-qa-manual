---
name: lt-morning-report
description: Assemble the Lingotran QA morning report from overnight pipeline artifacts — speech corpus, load, data isolation, accessibility, pipeline health. Use at the start of the day or when asked what changed overnight.
---

# The 09:30 report

Read the overnight artifacts and produce **one screen** a QA engineer can act on before
scrum at 10:00. Not a dashboard, not a summary of everything that ran — a ranked list of
what moved.

## Inputs

| Source | What to take from it |
|---|---|
| REF corpus run | Per-clip transcript match %, and the delta against the previous run |
| k6 class burst | p95, error rate, and the 429 count (must be zero) |
| Standing SQL (6.2) | Cross-school rows, orphans, soft-delete leaks, attempt-limit violations |
| axe scan | New violations only, on changed views |
| Pipeline | Failures, and any spec that failed then passed on re-run |
| Deploy log | Last deploy, migration, flag flip, config edit |

## Rules

- **Rank by consequence, not by section order.** A REF-02 breach outranks a slow test
  every time.
- **Report deltas, not absolutes.** "p95 742ms" means little; "742ms, was 610ms" is a
  finding.
- **Zero is a result.** Say "cross-school rows: 0", never omit it — a silent check is
  indistinguishable from one that did not run.
- **If a job did not run, say so loudly.** A missing REF run is worse than a failing one,
  because it looks like nothing is wrong.
- State **what changed overnight** — deploy, migration, flag, config. Almost every
  overnight regression traces to one of those four.
- End with a single **first action**.

## Never

- Never decide severity or release readiness. Rank and report; a human decides.
- Never say a breach is acceptable. Report the number against the floor and stop.
- Never fill a gap with an estimate. Missing data is reported as missing.

## Shape

```
LINGOTRAN QA · MORNING REPORT · <date>

<AREA>        <headline number> <delta>   <ok | BREACH>
  ...one indented line per finding, worst first

WHAT CHANGED  deploy · migration · flag · config
FIRST ACTION  <the single thing to do before scrum>
```
