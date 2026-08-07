---
name: lt-story-interrogate
description: Interrogate a Lingotran user story or acceptance criteria before any test cases are written. Use during refinement, when handed a vague story, or when ACs look thin.
---

# Interrogate a story before writing a single case

Lingotran context you must assume:

- Sold to **schools**, not individuals. A class is ~30 learners sharing **one NAT IP**
  on shared devices, many on **iPad Safari**.
- **Many learners are minors.** Cross-account exposure of identity, audio or progress
  is a safeguarding incident with regulatory weight, not a normal Sev-2.
- Customer domains are `school.edu`. Stories are `LT-nnnn`.

## Ask, at minimum

1. **Lifetime and boundaries** — is a duration measured from an event or from inactivity?
2. **Transition from existing state** — what happens to records created before this change?
3. **Security invalidation** — does a credential change revoke what this creates?
4. **Role scope** — does this apply to *student* accounts on shared classroom devices?
   If yes, ask why.
5. **Revocation** — can an admin see and undo it during an incident? Without that the
   feature has no off switch.
6. **Interaction with refresh/retry** — can the mechanism be chained to defeat its own limit?
7. **Contractual limits** — do signed district contracts cap this?
8. **Class scale** — what happens when 30 learners do this within the same minute?

## Output

A table: `Question the ACs do not answer | Why it changes the test plan`.

## Hard rules

- **Flag ambiguity; never resolve it by guessing.** An assumed answer is the defect.
- Do not write test cases yet. Questions first — they are cheaper now than in production.
- If an AC is testable as written, say so and move on. Do not manufacture doubt.
