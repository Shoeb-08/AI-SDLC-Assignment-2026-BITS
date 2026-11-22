import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from reminder_agent import ReminderAgent


REFERENCE = datetime(2026, 11, 21, 12, 0, 0)


def test_create_reminder():
    response = ReminderAgent().process("Remind me to call client_xyz tomorrow at 5 PM", REFERENCE)
    assert response["intent"] == "create_reminder"
    assert response["task"] == "call client_xyz"
    assert response["datetime"] == "2026-11-22T17:00:00"
    assert response["needs_clarification"] is False


def test_missing_time_requires_clarification():
    response = ReminderAgent().process("Remind me about the meeting", REFERENCE)
    assert response["intent"] == "clarification_required"
    assert response["datetime"] is None
    assert response["needs_clarification"] is True


def test_invalid_date_requires_clarification():
    response = ReminderAgent().process("Remind me to file taxes on February 30 at 9 AM", REFERENCE)
    assert response["intent"] == "clarification_required"
    assert response["datetime"] is None


def test_empty_input_requires_clarification():
    response = ReminderAgent().process("", REFERENCE)
    assert response["intent"] == "clarification_required"


def test_create_reminder_with_specific_calendar_date():
    response = ReminderAgent().process(
        "Please remind me to submit report on 2026-12-01 at 09:30",
        REFERENCE,
    )
    assert response["intent"] == "create_reminder"
    assert "submit report" in response["task"]
    assert response["datetime"] == "2026-12-01T09:30:00"
    assert response["needs_clarification"] is False


def test_create_reminder_today():
    response = ReminderAgent().process(
        "Remind me about team standup today at 9 AM",
        REFERENCE,
    )
    assert response["intent"] == "create_reminder"
    assert response["task"] == "team standup"
    assert response["datetime"] == "2026-11-21T09:00:00"
    assert response["needs_clarification"] is False


def test_create_reminder_future_year():
    response = ReminderAgent().process(
        "Remind me to renew passport on January 15, 2027 at 10 AM",
        REFERENCE,
    )
    assert response["intent"] == "create_reminder"
    assert response["task"] == "renew passport"
    assert response["datetime"] == "2027-01-15T10:00:00"
    assert response["needs_clarification"] is False


def test_create_reminder_time_format_with_minutes():
    response = ReminderAgent().process(
        "Reminder: pay internet bill on 2026-12-10 at 18:45",
        REFERENCE,
    )
    assert response["intent"] == "create_reminder"
    assert "pay internet bill" in response["task"]
    assert response["datetime"] == "2026-12-10T18:45:00"
    assert response["needs_clarification"] is False


def test_create_reminder_relative_minutes():
    response = ReminderAgent().process(
        "Remind me to drink water in 45 minutes",
        REFERENCE,
    )
    assert response["intent"] == "create_reminder"
    assert response["task"] == "drink water"
    assert response["datetime"] == "2026-11-21T12:45:00"
    assert response["needs_clarification"] is False


def test_create_reminder_next_weekday():
    response = ReminderAgent().process(
        "Remind me to attend yoga next Friday at 7 PM",
        REFERENCE,
    )
    assert response["intent"] == "create_reminder"
    assert response["task"] == "attend yoga"
    assert response["datetime"] == "2026-11-27T19:00:00"
    assert response["needs_clarification"] is False


def test_snooze_reminder_minutes():
    response = ReminderAgent().process(
        "Snooze meeting for 30 minutes",
        REFERENCE,
    )
    assert response["intent"] == "snooze_reminder"
    assert response["task"] == "meeting"
    assert response["datetime"] == "2026-11-21T12:30:00"
    assert response["needs_clarification"] is False


def test_snooze_reminder_hours():
    response = ReminderAgent().process(
        "Snooze bill payment for 2 hours",
        REFERENCE,
    )
    assert response["intent"] == "snooze_reminder"
    assert response["task"] == "bill payment"
    assert response["datetime"] == "2026-11-21T14:00:00"
    assert response["needs_clarification"] is False


def test_nonsense_input_requires_clarification():
    response = ReminderAgent().process("asdf qwerty blahblah", REFERENCE)
    assert response["intent"] == "clarification_required"
    assert response["datetime"] is None
    assert response["needs_clarification"] is True


def test_contradictory_date_instructions_require_clarification():
    response = ReminderAgent().process(
        "Remind me to meet Sam tomorrow and Friday at 3 PM",
        REFERENCE,
    )
    assert response["intent"] == "clarification_required"
    assert response["datetime"] is None
    assert response["needs_clarification"] is True
