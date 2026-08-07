---
name: lt-sql-guard
description: Generate read-only SQL validation queries for the Lingotran PostgreSQL schema. Use for data integrity checks, cross-school isolation, orphan and soft-delete audits. Never executes against production.
---

# Read-only validation SQL for Lingotran

## Restrictions — these are not negotiable

- **SELECT only.** No INSERT, UPDATE, DELETE, TRUNCATE, DDL, or transaction control.
- **Never** reference a production connection string, host, or credential.
- Staging or a local container only.
- **Do not execute anything unless explicitly asked.** Output SQL.
- If a check would need a write to be meaningful, say so instead of writing one.

## Schema facts

- `users(id, email citext UNIQUE, role CHECK IN ('learner','teacher','admin'), school_id, deleted_at)`
- `attempts(id, user_id → users ON DELETE CASCADE, exercise_id → exercises, accuracy numeric(5,2), created_at)`
- `idx_attempts_user_ex ON attempts(user_id, exercise_id)`
- Soft delete via `deleted_at` — **every** query must filter it

## The standing checks

Always offer these before anything bespoke:

1. **Cross-school leakage** — a learner with attempts on another school's exercise.
   Must return zero rows, always. A non-zero result is contract-terminating and
   invisible from the UI.
2. **Orphans** — attempts whose exercise was hard-deleted.
3. **Soft-deleted users still reachable** through a join.
4. **Attempt-limit violations** the check-then-act race allowed through
   (`GROUP BY user_id, exercise_id HAVING count(*) > 3`).
5. **Index usage** — `EXPLAIN ANALYZE` the attempt-count query; must be Index Scan,
   not Seq Scan, at staging volumes.

## Output format

One SQL block per check, each preceded by a one-line comment naming the defect it
detects. For each, state **what a non-zero result means in product terms and who must
be told**.
