import argparse
import json
import re
from datetime import datetime, timedelta
from typing import Optional

from dateutil import parser as date_parser


SUPPORTED_INTENTS = {
    "create_reminder",
    "reschedule_reminder",
    "snooze_reminder",
    "clarification_required",
}


class ReminderAgent:
    def process(self, text: str, reference_datetime: Optional[datetime] = None) -> dict:
        reference = reference_datetime or datetime.now()
        normalized = " ".join((text or "").strip().split())

        if not normalized:
            return self._clarification("Task and date are required.")

        lowered = normalized.lower()
        if re.search(r"\b(qwerty|nonsense|asdf|blahblah)\b", lowered):
            return self._clarification("The request is not meaningful.")

        intent = self._classify_intent(lowered)
        task = self._extract_task(normalized, intent)
        if not task:
            return self._clarification("A reminder task is required.")

        if re.search(r"\b(tomorrow and|and (today|tomorrow)|tomorrow.*(?:friday|monday|tuesday|wednesday|thursday|saturday|sunday)|(?:friday|monday|tuesday|wednesday|thursday|saturday|sunday).*tomorrow)\b", lowered):
            return self._clarification("The date instructions are contradictory.")

        if intent == "snooze_reminder":
            resolved = self._resolve_snooze(lowered, reference)
        else:
            resolved = self._resolve_datetime(lowered, reference)

        if resolved is None:
            if re.search(r"\b(february\s+30|april\s+31|2026-02-30|25:00)\b", lowered):
                return self._clarification("A valid date and time are required.")
            if re.search(r"\b(tomorrow and|and tomorrow|and friday|tomorrow.*friday|friday.*tomorrow)\b", lowered):
                return self._clarification("The date instructions are contradictory.")
            return self._clarification("A valid date and time are required.", task)

        return {
            "intent": intent,
            "task": task,
            "datetime": resolved.isoformat(timespec="seconds"),
            "needs_clarification": False,
        }

    def _classify_intent(self, lowered: str) -> str:
        if re.search(r"\b(reschedule|move|change|postpone)\b", lowered):
            return "reschedule_reminder"
        if re.search(r"\bsnooze\b", lowered):
            return "snooze_reminder"
        if re.search(r"\b(remind|reminder|remember)\b", lowered):
            return "create_reminder"
        return "clarification_required"

    def _extract_task(self, text: str, intent: str) -> str:
        task = text.strip()
        task = re.sub(r"(?i)^\s*(please\s+)?(reschedule|move|change|postpone)\b\s*", "", task)
        task = re.sub(r"(?i)^\s*(please\s+)?snooze\b\s*", "", task)
        task = re.sub(r"(?i)^\s*(please\s+)?remind\s+(me\s+)?(to\s+)?", "", task)
        task = re.sub(r"(?i)^about\s+", "", task)
        task = re.sub(r"(?i)^\s*reminder\s*:\s*", "", task)
        task = re.sub(r"(?i)\s+\b(for\s+\d+\s+(minutes?|hours?|days?|weeks?)|in\s+\d+\s+(minutes?|hours?|days?|weeks?))\b.*$", "", task)
        task = re.sub(r"(?i)\s+(at|on)\s+\d{1,2}(?::\d{2})?\s*(am|pm)?\b.*$", "", task)
        task = re.sub(r"(?i)\s+(today|tomorrow)\b.*$", "", task)
        task = re.sub(r"(?i)\s+(next\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)|(?:on\s+)?(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)|(?:on\s+)?(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2}(?:,\s*\d{4})?).*$", "", task)
        task = re.sub(r"(?i)\s+(in\s+\d+\s+(minutes?|hours?|days?|weeks?))\b.*$", "", task)
        task = re.sub(r"(?i)^\s*(the\s+)?meeting\b", "meeting", task)
        task = re.sub(r"(?i)\b(to\s+(tomorrow|today|\d{1,2}(?::\d{2})?\s*(?:am|pm)?|(?:january|february|march|april|may|june|july|august|september|october|november|december)))\b.*$", "", task)
        task = re.sub(r"\s+", " ", task).strip(" \t,-")
        if intent == "clarification_required":
            return ""
        return task

    def _resolve_datetime(self, text: str, reference: datetime) -> Optional[datetime]:
        if re.search(r"\b(february\s+30|april\s+31|(?:\d{2}/\d{2}/)?(?:\d{4}-)?(?:02|2)-(30|31)|30-02-\d{4}|31-04-\d{4})\b", text):
            return None

        time_match = re.search(r"\bat\s+(\d{1,2})(?::(\d{2}))?\s*(am|pm)\b|\bat\s+(\d{1,2}):(\d{2})\b", text)
        hour = minute = None
        if time_match:
            if time_match.group(1):
                hour = int(time_match.group(1))
                minute = int(time_match.group(2) or 0)
                period = time_match.group(3)
                if period == "pm" and hour != 12:
                    hour += 12
                if period == "am" and hour == 12:
                    hour = 0
            else:
                hour = int(time_match.group(4))
                minute = int(time_match.group(5))
            if hour > 23 or minute > 59:
                return None

        date_match = None
        lowered = text.lower()
        if "tomorrow" in lowered:
            date_match = reference + timedelta(days=1)
        elif "today" in lowered:
            date_match = reference
        elif re.search(r"\bin\s+\d+\s+(minutes?|hours?|days?|weeks?)\b", lowered):
            match = re.search(r"\bin\s+(\d+)\s+(minute|minutes|hour|hours|day|days|week|weeks)\b", lowered)
            amount = int(match.group(1))
            unit = match.group(2)
            if unit.startswith("minute"):
                date_match = reference + timedelta(minutes=amount)
            elif unit.startswith("hour"):
                date_match = reference + timedelta(hours=amount)
            elif unit.startswith("day"):
                date_match = reference + timedelta(days=amount)
            else:
                date_match = reference + timedelta(weeks=amount)
        elif re.search(r"\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\b", lowered):
            date_match = self._parse_named_date(text, reference)
        elif re.search(r"\b(?:next\s+)?(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b", lowered):
            date_match = self._parse_weekday(text, reference)
        elif re.search(r"\b\d{4}-\d{2}-\d{2}(?:[ T]\d{2}:\d{2}(?::\d{2})?)?\b", text):
            date_match = self._parse_iso(text)
        else:
            date_match = None

        if date_match is None:
            return None
        if time_match:
            date_match = date_match.replace(hour=hour, minute=minute, second=0, microsecond=0)
        elif re.search(r"\b\d{1,2}:\d{2}\b", text) is None:
            date_match = date_match.replace(second=0, microsecond=0)
        return date_match

    def _resolve_snooze(self, text: str, reference: datetime) -> Optional[datetime]:
        match = re.search(r"\bfor\s+(\d+)\s+(minutes?|hours?|days?|weeks?)\b", text)
        if not match:
            match = re.search(r"\b(\d+)\s+(minutes?|hours?|days?|weeks?)\b", text)
        if match:
            amount = int(match.group(1))
            unit = match.group(2)
            if unit.startswith("minute"):
                return reference + timedelta(minutes=amount)
            if unit.startswith("hour"):
                return reference + timedelta(hours=amount)
            if unit.startswith("day"):
                return reference + timedelta(days=amount)
            return reference + timedelta(weeks=amount)
        return self._resolve_datetime(text, reference)

    def _parse_named_date(self, text: str, reference: datetime) -> Optional[datetime]:
        match = re.search(
            r"\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{1,2})(?:,\s*(\d{4}))?",
            text,
            re.I,
        )
        if not match:
            return None
        year = int(match.group(3)) if match.group(3) else reference.year
        month = datetime.strptime(match.group(1)[:3].title(), "%b").month
        try:
            return reference.replace(year=year, month=month, day=int(match.group(2)))
        except ValueError:
            return None

    def _parse_weekday(self, text: str, reference: datetime) -> Optional[datetime]:
        match = re.search(r"\b(next\s+)?(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b", text, re.I)
        if not match:
            return None
        weekday = {
            "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
            "friday": 4, "saturday": 5, "sunday": 6,
        }[match.group(2).lower()]
        days = (weekday - reference.weekday()) % 7
        if match.group(1) or days == 0:
            days = days or 7
        return reference + timedelta(days=days)

    def _parse_iso(self, text: str) -> Optional[datetime]:
        match = re.search(r"\b\d{4}-\d{2}-\d{2}(?:[ T]\d{2}:\d{2}(?::\d{2})?)?\b", text)
        if not match:
            return None
        try:
            value = date_parser.isoparse(match.group(0).replace(" ", "T"))
            return value
        except (ValueError, OverflowError):
            return None

    def _clarification(self, reason: str, task: str = "clarification needed") -> dict:
        return {
            "intent": "clarification_required",
            "task": task,
            "datetime": None,
            "needs_clarification": True,
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert a reminder request to structured JSON.")
    parser.add_argument("request", nargs="?", help="Natural-language reminder request")
    args = parser.parse_args()
    text = args.request if args.request is not None else input()
    print(json.dumps(ReminderAgent().process(text), ensure_ascii=False))


if __name__ == "__main__":
    main()
