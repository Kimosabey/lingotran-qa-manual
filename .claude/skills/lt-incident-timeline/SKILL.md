---
name: lt-incident-timeline
description: Reconstruct a Lingotran incident timeline from Application Insights entries and a correlation ID, then rank hypotheses. Use during or just after a production incident.
---

# Incident timeline

**Mitigate first.** If service is still degraded, this can wait — a rolled-back deploy
costs pride, a long investigation while schools cannot teach costs a renewal.

## Inputs

A correlation ID, and log entries around the incident window. The correlation ID joins
frontend, API, database and speech in one trace.

## Produce, in this order

1. **Timeline** — one line per hop, with timestamps, across all four layers.
2. **First anomalous event** — quote the exact log line. Do not paraphrase it.
3. **Up to three hypotheses**, each with the specific evidence that would confirm or kill
   it, and which is cheapest to check first.
4. **What changed** — deploy, migration, flag flip, config edit. Almost every incident
   traces to one of those four.

## Lingotran-specific patterns worth checking early

| Symptom | Look at first |
|---|---|
| Many users, one school, sudden | Per-IP rate limiting. A school is one NAT address |
| Limit behaving as double | In-process state across 2 App Service instances |
| Speech failing for everyone | Secure context, network, or the browser API itself — not our API |
| Counts wrong, no errors | Check-then-act race under concurrent load |
| One school seeing another's data | **Stop. Safeguarding. Escalate same day** |

## Hard rules

- **Mark clearly anything you inferred** rather than read directly in the log.
- Never state a root cause the evidence does not support. "Consistent with" is not "caused by".
- Never paste learner audio, names or credentials into a prompt. IDs only.
- The five-whys RCA is written the **next day**, not during the incident.
