---
name: lt-playwright
description: Convert a Lingotran manual test case into a Playwright spec under the house rules, then run it. Use when automating a case that has already been written.
---

# Manual case to Playwright spec

## House rules — all six, every time

| Rule | Why |
|---|---|
| Seed state via the **API**, never the UI | The single largest source of flake and runtime |
| Locate by `getByRole` with an accessible name | Survives restyling, and doubles as an a11y check |
| Never `waitForTimeout` | A fixed sleep is either flaky or slow, usually both |
| **Assert the database** at the end | A green UI over a wrong row is what reaches production |
| One assertion theme per test | A failure should name the defect without a debugger |
| Fresh data per test | Shared fixtures create order dependence that only shows up in CI |

Helpers `seedLearner` and `seedTeacher` already exist. `pg` returns `bigint` as a string,
so `count` comparisons are against `'3'`, not `3`.

## Then run it

Run the spec. Iterate until green.

**If it passes on the first run before the feature exists, that is a broken assertion.**
Say so — do not report success.

## Do not automate these

Real microphone capture, scoring quality, and exploratory charters. They need a human
and a real device (8.2). If the case depends on speech, note that it cannot run on HTTP
dev or UAT at all — the browser blocks the API without a secure context.
