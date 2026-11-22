# Implementation Plan

1. Implement a small rule-based Python parser as the starter implementation.
2. Normalize input and identify create, reschedule, snooze, and clarification intents.
3. Extract a task and resolve relative or explicit dates/times safely.
4. Reject empty, nonsensical, contradictory, malformed, and impossible expressions.
5. Expose `ReminderAgent.process(text, reference_datetime=None)` and a JSON-producing CLI.
6. Add JSON Schema-based structural validation.
7. Add behavioral property checks for intent, clarification, dates, and guardrails.
8. Add semantic task, intent, and usefulness scoring.
9. Provide an evaluation dataset with normal, boundary, ambiguous, malformed, and adversarial cases.
10. Run the aggregate harness and retain evidence in `evidence/`.

## Starter Architecture

The implementation deliberately uses inspectable parsing rules rather than opaque model calls. This keeps offline runs deterministic while allowing future integration with an LLM or nondeterministic service behind the same response contract.
