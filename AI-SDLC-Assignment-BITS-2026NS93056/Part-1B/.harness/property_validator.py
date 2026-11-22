import re


def validate_properties(case: dict, response: dict) -> list[str]:
    errors = []
    text = case["input"].lower()
    expected = case["expected_intent"]
    actual = response.get("intent")

    if actual != expected:
        errors.append(f"Expected intent {expected}, got {actual}")

    if "reschedule" in text or re.search(r"\b(move|change)\b", text):
        if actual != "reschedule_reminder":
            errors.append("Reschedule request was not classified correctly")
    if re.search(r"\bsnooze\b", text):
        if actual != "snooze_reminder" and not (actual == "clarification_required" and response.get("datetime") is None):
            errors.append("Snooze request violated intent or clarification rules")

    if actual == "clarification_required":
        if response.get("needs_clarification") is not True:
            errors.append("Clarification response must set needs_clarification true")
        if response.get("datetime") is not None:
            errors.append("Clarification response must not contain a date")

    if response.get("needs_clarification") is False:
        if not isinstance(response.get("datetime"), str):
            errors.append("Scheduled responses require a datetime")

    if not text.strip():
        if actual != "clarification_required":
            errors.append("Empty input must require clarification")

    if re.search(r"\bfebruary\s+30|2026-02-30|30-02|\b25:00\b|\btomorrow and\b", text):
        if actual != "clarification_required":
            errors.append("Invalid or contradictory date was not rejected")

    if re.search(r"\b(qwerty|nonsense|asdf|blahblah)\b", text):
        if actual != "clarification_required":
            errors.append("Nonsensical input must require clarification")

    if re.search(r"\bremind me\b", text) and "tomorrow" not in text and "today" not in text:
        if not re.search(r"\b\d{4}-\d{2}-\d{2}\b|\b(january|february|march|april|may|june|july|august|september|october|november|december)\b|\b(next\s+)?(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b|\bin\s+\d+\s+(minutes?|hours?|days?|weeks?)\b", text):
            if actual != "clarification_required":
                errors.append("Missing date must trigger clarification")
    return errors
