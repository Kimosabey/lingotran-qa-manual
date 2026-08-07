---
name: lt-testgen
description: Generate Lingotran test cases from a story or acceptance criteria, as a table with layers assigned. Use after the story has been interrogated and the ACs are agreed.
---

# Test cases from a story

Run `lt-story-interrogate` first. If the ACs still contain an ambiguity, **stop and say
so** rather than generating cases against a guess.

## Context you must assume

- Lingotran serves **schools and individuals**. A class is ~30 learners behind one NAT
  IP on shared iPads; B2C learners are on personal phones, more of them iOS.
- Many learners are **minors**.
- Speech is the **browser Web Speech API** — a transcript, not a pronunciation score.
  It needs a secure context, so it does not work on HTTP dev or UAT.

## Output

A table: `ID | Case | Expected | Layer (unit / api / e2e / manual)`.

IDs follow `LT-F01` frontend, `LT-A01` api, `LT-D01` database.

## Mandatory rows — a plan without these is incomplete

| Must include | Why |
|---|---|
| Boundaries, one either side | Bugs cluster at the edge, never the middle |
| At least three negatives | The happy path is the easy third of the work |
| One **concurrency** case | Check-then-act is invisible to sequential testing |
| One **whole-class** case | Thirty learners at once is the shape that breaks Lingotran |
| One **accessibility** case | Keyboard or screen reader, not just contrast |
| One **non-Latin text** case | `str.length` counts UTF-16 units, so limits fire early |
| One case on a **real device** | iPad Safari is where speech is weakest |

## Never

- Never invent an acceptance criterion. Flag the gap.
- Never mark a case automated that needs a real microphone.
- Never assert an exact transcript — recognition is not deterministic.
