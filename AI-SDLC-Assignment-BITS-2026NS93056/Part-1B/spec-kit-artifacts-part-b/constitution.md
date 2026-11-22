# Constitution

## Purpose

The Natural Language Reminder Agent converts human reminder requests into a single predictable JSON response while preserving useful non-deterministic language understanding as an implementation concern.

## Governing Rules

1. Every result must have exactly the four fields in the output contract: `intent`, `task`, `datetime`, and `needs_clarification`.
2. Supported intents are limited to `create_reminder`, `reschedule_reminder`, `snooze_reminder`, and `clarification_required`.
3. Invalid, missing, contradictory, or ambiguous mandatory information must trigger clarification instead of fabrication.
4. The agent must never schedule against an invalid date or a date that cannot be resolved reliably.
5. The agent must remain safe to run in offline/development environments; external AI APIs are optional.
6. Evaluations must report structural, property, semantic, and aggregate scores.
7. Aggregate pass threshold is 80 percent. A run below 80 percent fails.
8. Changes that weaken guardrails or introduce new intents without specification updates are not permitted.
