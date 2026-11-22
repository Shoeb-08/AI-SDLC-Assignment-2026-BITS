"""Tests for task validation and JSON conversion."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest

from todo.exceptions import TodoError
from todo.task import (
    Task,
    validate_description,
    validate_tags,
)


def test_task_round_trip_drops_duplicate_tags():
    task = Task(1, " Read ", " Chapter 2 ", "HIGH", ["study", "Study"], "pending")
    copy = Task.from_dict(task.to_dict())
    assert copy.to_dict() == task.to_dict()
    assert task.title == "Read"
    assert task.priority == "high"
    assert task.tags == ["study"]
    assert copy.to_dict()["client_request"] == "Read"
    assert copy.to_dict()["Severity"] == "high"
    assert copy.to_dict()["client_id"] == 1


def test_rejects_blank_title():
    with pytest.raises(TodoError, match="Title is required"):
        Task(1, "   ")


def test_rejects_bad_priority():
    with pytest.raises(TodoError, match="Priority"):
        Task(1, "Read", priority="urgent")


def test_rejects_bad_status():
    with pytest.raises(TodoError, match="Status"):
        Task(1, "Read", status="done")


def test_from_dict_missing_field():
    with pytest.raises(TodoError, match="client_request"):
        Task.from_dict({"client_id": 1})


def test_rejects_non_numeric_task_id():
    with pytest.raises(TodoError, match="Task ID"):
        Task("1", "Read")


def test_validate_description_none_returns_empty_string():
    assert validate_description(None) == ""


def test_validate_description_non_string_raises():
    with pytest.raises(TodoError, match="Description must be text"):
        validate_description(123)


def test_validate_tags_from_comma_string():
    tags = validate_tags("alpha, beta, gamma")
    assert tags == ["alpha", "beta", "gamma"]


def test_validate_tags_none_returns_empty_list():
    assert validate_tags(None) == []


def test_validate_tags_invalid_type_raises():
    with pytest.raises(TodoError, match="Tags must be a list of text values"):
        validate_tags(42)


def test_validate_tags_non_string_element_raises():
    with pytest.raises(TodoError, match="Each tag must be text"):
        validate_tags(["valid", 123])


def test_rejects_negative_task_id():
    with pytest.raises(TodoError, match="Task ID must be a positive whole number"):
        Task(-1, "Title")


def test_rejects_zero_task_id():
    with pytest.raises(TodoError, match="Task ID must be a positive whole number"):
        Task(0, "Title")


def test_task_property_aliases():
    task = Task(client_id=10, client_request="Request", severity="high")
    assert task.client_id == 10
    assert task.client_request == "Request"
    assert task.severity == "high"
    task.client_request = "Updated"
    assert task.title == "Updated"


def test_from_dict_non_dict_raises():
    with pytest.raises(TodoError, match="Each task must be a JSON object"):
        Task.from_dict("not_a_dict")
