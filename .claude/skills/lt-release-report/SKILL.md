---
name: lt-release-report
description: Assemble the Lingotran release readiness statement from pipeline artifacts, in plain English for a non-engineering reader. Use before a release sign-off.
---

# Release readiness

Assembles the eleven-row table in 12.2 into one page a head of department can act on.

## Inputs

Test run links, pipeline results, the REF corpus report, the k6 summary, the cross-school
SQL output, the axe report, migration up/down logs, the open defect list, and the feature
flag config diff.

## Structure

Three sections, in this order:

1. **What changed** — in product terms, not ticket titles.
2. **What is untested and accepted as risk** — the most valuable section on the page.
3. **What to watch in week one** — specific, with the signal that would mean trouble.

## Rules

- **Every claim traces to an input.** If there is no artifact, the row is "not evidenced",
  never "assumed fine".
- **Plain English.** No stack terminology. The reader cares whether lessons run on Monday.
- **Neutral tone.** Do not reassure and do not alarm.
- Standing Lingotran caveats that belong in section 2 unless resolved: speech cannot be
  verified on UAT while it is HTTP (2.3), and the REF corpus only ran on localhost or
  production.

## Never

- Never write "it is fine."
- **Never recommend go or no-go.** QA states risk; the business decides. A model has
  neither the customer context nor the contractual exposure to make that call (Module 11).
- Never omit a failing check to make the page read better. The omission is the defect.
