from datetime import datetime

SUPPORTED_INTENTS = {
    "create_reminder",
    "reschedule_reminder",
    "snooze_reminder",
    "clarification_required",
}
REQUIRED_FIELDS = {"intent", "task", "datetime", "needs_clarification"}


def validate_schema(response: dict) -> list[str]:
    errors = []
    if not isinstance(response, dict):
        return ["Response is not a JSON object"]

    missing = REQUIRED_FIELDS - set(response)
    if missing:
        errors.append("Missing fields: " + ", ".join(sorted(missing)))
    if set(response) - REQUIRED_FIELDS:
        errors.append("Unexpected fields are not allowed")

    if not isinstance(response.get("intent"), str):
        errors.append("intent must be a string")
    elif response["intent"] not in SUPPORTED_INTENTS:
        errors.append("intent is outside the supported enum")

    if not isinstance(response.get("task"), str):
        errors.append("task must be a string")
    if not isinstance(response.get("needs_clarification"), bool):
        errors.append("needs_clarification must be a boolean")

    value = response.get("datetime")
    if value is not None:
        if not isinstance(value, str):
            errors.append("datetime must be an ISO string or null")
        else:
            try:
                datetime.fromisoformat(value)
            except ValueError:
                errors.append("datetime is not a valid ISO datetime")

    if response.get("needs_clarification") is True and response.get("datetime") is not None:
        errors.append("Clarification responses must use datetime null")
    return errors
