---
name: lt-pr-trace
description: Map a Lingotran PR diff onto the layer trace and list the tests each touched layer requires. Use when reviewing any pull request, reading a diff, or deciding what to test for a change.
---

# Layer-trace a Lingotran PR

Read the diff. **Do not summarise it back.**

## 1. Locate every change on the trace

| # | Layer | Typical file |
|---|---|---|
| 1 | React component | `LessonPlayer.tsx`, `RecordControl.tsx` |
| 2 | API client | `lib/apiClient.ts` |
| 3 | Route | `routes/*.routes.ts` |
| 4 | Middleware | `authenticate`, `rateLimit` |
| 5 | Validator | zod schema |
| 6 | Controller | `*.controller.ts` |
| 7 | Service | `*.service.ts` — most bugs live here |
| 8 | Repository | `*.repository.ts` |
| 9 | PostgreSQL | schema, indexes, migrations |
| 10 | Response | JSON envelope |
| 11 | React render | state update |

## 2. Expand downstream

Output the layers touched **plus every layer downstream of them**. A change at
layer 9 can break all ten above it; a change at layer 7 cannot break layer 1.

## 3. List the tests each layer in that set requires

Concrete cases, not categories.

## 4. Flag these explicitly, each on its own line

- A new route whose **sibling verbs** were not also checked for auth
- Any new query with no `EXPLAIN` against staging volumes (200 local rows prove nothing)
- Any **check-then-act** sequence — read, decide, write — needs a two-concurrent-request test
- Any state held **in process memory** — the API runs 2+ instances, so the real limit is
  configured × instance count
- Anything touching **learner audio** — region, retention, deletion, sub-processors
- Any user-visible **text length limit** — `str.length` counts UTF-16 units, so Devanagari
  and Tamil names hit an 80-char limit at ~20 visible characters

## 5. Close with what you could not determine from the diff alone

## Hard rule

**Never state that a change is safe.** Report what it touches and what that requires.
Whether it ships is a human decision.
