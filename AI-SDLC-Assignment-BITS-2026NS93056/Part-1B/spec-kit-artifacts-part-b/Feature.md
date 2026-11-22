# Feature Specification

## Input

The agent accepts a single natural-language string and an optional reference datetime.

```text
Remind to schedule meeting with client_xyz tomorrow at 10 AM EST
```

## Output Contract

```json
{
  "intent": "create_reminder",
  "task": "call client_xyz",
  "datetime": "2026-11-22T17:00:00",
  "needs_clarification": false
}
```

## Intents

- `create_reminder`: create a new reminder with enough information.
- `reschedule_reminder`: move or change an existing reminder.
- `snooze_reminder`: postpone an existing reminder.
- `clarification_required`: stop and request missing or conflicting information.

## Resolution Rules

- Empty, whitespace-only, and nonsensical text require clarification.
- Create requests require a task and resolvable datetime.
- Reschedule requests require a reminder/task and a new resolvable datetime.
- Snooze requests require a reminder/task and a duration or new datetime.
- Missing date or time is clarified unless the specification says otherwise.
- Invalid ISO/calendar dates, invalid time expressions, and contradictory instructions are clarified.
- Relative dates are resolved against the supplied reference datetime.
- No unknown task or date may be invented.

## Structural Invariants

- `intent` is a string from the supported enum.
- `task` is a string.
- `datetime` is a valid ISO datetime string or `null`.
- `needs_clarification` is a boolean.
- Clarification responses use `datetime: null` and `needs_clarification: true`.
