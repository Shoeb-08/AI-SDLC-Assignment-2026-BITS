"""Tests for creating, changing, filtering, and sorting tasks."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest

from todo.analyst import TaskAnalyst
from todo.exceptions import TodoError


def test_create_list_and_ids(Analyst):
    first = Analyst.create_task("Buy milk", "2 litres", "high", ["home"])
    second = Analyst.create_task("Read chapter", priority="low", tags="study, uni")
    assert first.task_id == 1
    assert first.status == "pending"
    assert second.task_id == 2
    assert second.tags == ["study", "uni"]
    assert [task.task_id for task in Analyst.list_tasks()] == [1, 2]


def test_create_rejects_blank_title(Analyst):
    with pytest.raises(TodoError, match="Title is required"):
        Analyst.create_task("   ")


def test_update_task(Analyst):
    task = Analyst.create_task("Draft", priority="low")
    updated = Analyst.update_task(
        task.task_id,
        title="Final draft",
        description="Add tests",
        priority="high",
        tags=["uni"],
    )
    assert updated.title == "Final draft"
    assert updated.description == "Add tests"
    assert updated.priority == "high"
    assert updated.tags == ["uni"]


def test_invalid_priority_does_not_change_task(Analyst):
    task = Analyst.create_task("Draft", priority="low")
    with pytest.raises(TodoError, match="Priority"):
        Analyst.update_task(task.task_id, priority="urgent")
    saved = Analyst.get_task(task.task_id)
    assert saved.priority == "low"
    assert saved.title == "Draft"


def test_delete_task(Analyst):
    task = Analyst.create_task("Temp")
    deleted = Analyst.delete_task(task.task_id)
    assert deleted.title == "Temp"
    assert Analyst.list_tasks() == []


def test_delete_missing_task(Analyst):
    with pytest.raises(TodoError, match="not found"):
        Analyst.delete_task(5)


def test_mark_completed(Analyst):
    task = Analyst.create_task("Lab report")
    done = Analyst.mark_completed(task.task_id)
    assert done.status == "completed"
    again = Analyst.mark_completed(task.task_id)
    assert again.status == "completed"


def test_filter_by_tag_is_case_insensitive(Analyst):
    Analyst.create_task("Essay", tags=["Uni", "writing"])
    Analyst.create_task("Shop", tags=["home"])
    found = Analyst.filter_by_tag(" uni ")
    assert [task.title for task in found] == ["Essay"]


def test_filter_requires_a_tag(Analyst):
    with pytest.raises(TodoError, match="Tag is required"):
        Analyst.filter_by_tag("   ")


def test_sort_by_priority(Analyst):
    Analyst.create_task("Low one", priority="low")
    Analyst.create_task("High one", priority="high")
    Analyst.create_task("Medium one", priority="medium")
    Analyst.create_task("High two", priority="high")
    ordered = Analyst.sort_by_priority()
    assert [task.title for task in ordered] == [
        "High one",
        "High two",
        "Medium one",
        "Low one",
    ]


def test_sort_can_be_saved(Analyst):
    Analyst.create_task("Low one", priority="low")
    Analyst.create_task("High one", priority="high")
    Analyst.sort_by_priority(save=True)
    assert [task.title for task in Analyst.list_tasks()] == [
        "High one",
        "Low one",
    ]


def test_tasks_are_reloaded_from_json(tmp_path):
    path = tmp_path / "tasks.json"
    original = TaskAnalyst(path)
    original.create_task("Persist me", tags=["save"])
    original.mark_completed(1)

    reloaded = TaskAnalyst(path)
    task = reloaded.get_task(1)
    assert task.title == "Persist me"
    assert task.status == "completed"
    assert task.tags == ["save"]
    assert reloaded.create_task("Next").task_id == 2


def test_create_task_default_priority(Analyst):
    task = Analyst.create_task("Item with default priority")
    assert task.priority == "medium"
    assert task.severity == "medium"


def test_create_task_empty_description_and_tags(Analyst):
    task = Analyst.create_task("Clean task", description=None, tags=None)
    assert task.description == ""
    assert task.tags == []


def test_get_task_success(Analyst):
    created = Analyst.create_task("Fetch target", description="detail", priority="high")
    fetched = Analyst.get_task(created.task_id)
    assert fetched.task_id == created.task_id
    assert fetched.title == "Fetch target"
    assert fetched.description == "detail"


def test_get_task_missing_raises_error(Analyst):
    with pytest.raises(TodoError, match="was not found"):
        Analyst.get_task(999)


def test_get_task_invalid_id_type(Analyst):
    with pytest.raises(TodoError, match="Task ID must be a positive whole number"):
        Analyst.get_task("invalid")


def test_update_task_reopen_status(Analyst):
    task = Analyst.create_task("Task to reopen")
    Analyst.mark_completed(task.task_id)
    reopened = Analyst.update_task(task.task_id, status="pending")
    assert reopened.status == "pending"


def test_update_task_invalid_status_does_not_change_task(Analyst):
    task = Analyst.create_task("Task status check")
    with pytest.raises(TodoError, match="Status must be pending or completed"):
        Analyst.update_task(task.task_id, status="archived")
    unchanged = Analyst.get_task(task.task_id)
    assert unchanged.status == "pending"


def test_filter_by_tag_no_match(Analyst):
    Analyst.create_task("Work item", tags=["work"])
    results = Analyst.filter_by_tag("personal")
    assert results == []


def test_sort_by_priority_tie_breaking(Analyst):
    first = Analyst.create_task("First medium", priority="medium")
    second = Analyst.create_task("Second medium", priority="medium")
    ordered = Analyst.sort_by_priority()
    assert [t.task_id for t in ordered] == [first.task_id, second.task_id]


def test_delete_only_target_task(Analyst):
    t1 = Analyst.create_task("First")
    t2 = Analyst.create_task("Second")
    t3 = Analyst.create_task("Third")
    Analyst.delete_task(t2.task_id)
    remaining_ids = [t.task_id for t in Analyst.list_tasks()]
    assert remaining_ids == [t1.task_id, t3.task_id]
