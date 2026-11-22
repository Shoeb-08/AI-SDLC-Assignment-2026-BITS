"""Tests for the JSON storage file."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest

from todo.exceptions import TodoError
from todo.storage import JsonStorage
from todo.task import Task


def test_missing_file_starts_empty(tmp_path):
    tasks, next_id = JsonStorage(tmp_path / "missing.json").load()
    assert tasks == []
    assert next_id == 1


def test_empty_file_starts_empty(tmp_path):
    path = tmp_path / "tasks.json"
    path.write_text("  \n", encoding="utf-8")
    tasks, next_id = JsonStorage(path).load()
    assert tasks == []
    assert next_id == 1


def test_save_and_load_round_trip(tmp_path):
    path = tmp_path / "nested" / "tasks.json"
    storage = JsonStorage(path)
    tasks = [Task(1, "One", "desc", "medium", ["a"], "pending")]
    storage.save(tasks, 2)
    loaded, next_id = storage.load()
    assert next_id == 2
    assert loaded[0].to_dict() == tasks[0].to_dict()
    saved = json.loads(path.read_text(encoding="utf-8"))
    assert saved["Client id"] == 2
    assert saved["Clients"][0]["client_request"] == "One"


def test_invalid_json(tmp_path):
    path = tmp_path / "tasks.json"
    path.write_text("[", encoding="utf-8")
    with pytest.raises(TodoError, match="invalid JSON"):
        JsonStorage(path).load()


def test_next_id_moves_past_existing_tasks(tmp_path):
    path = tmp_path / "tasks.json"
    path.write_text(
        json.dumps(
            {
                "Client id": 1,
                "Clients": [
                    {
                        "client_id": 4,
                        "client_request": "Old",
                        "description": "",
                        "Severity": "low",
                        "tags": [],
                        "status": "pending",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    tasks, next_id = JsonStorage(path).load()
    assert tasks[0].task_id == 4
    assert next_id == 5


def test_load_non_dict_json_raises_error(tmp_path):
    path = tmp_path / "tasks.json"
    path.write_text(json.dumps([1, 2, 3]), encoding="utf-8")
    with pytest.raises(TodoError, match="JSON file must contain an object"):
        JsonStorage(path).load()


def test_load_missing_clients_field(tmp_path):
    path = tmp_path / "tasks.json"
    path.write_text(json.dumps({"Client id": 1}), encoding="utf-8")
    with pytest.raises(TodoError, match="missing the Clients list"):
        JsonStorage(path).load()


def test_load_clients_not_a_list(tmp_path):
    path = tmp_path / "tasks.json"
    path.write_text(
        json.dumps({"Client id": 1, "Clients": "not_a_list"}),
        encoding="utf-8",
    )
    with pytest.raises(TodoError, match="missing the Clients list"):
        JsonStorage(path).load()


def test_load_invalid_client_id_type_bool(tmp_path):
    path = tmp_path / "tasks.json"
    path.write_text(
        json.dumps({"Client id": True, "Clients": []}),
        encoding="utf-8",
    )
    with pytest.raises(TodoError, match="Client id must be a positive whole number"):
        JsonStorage(path).load()


def test_load_invalid_client_id_type_string(tmp_path):
    path = tmp_path / "tasks.json"
    path.write_text(
        json.dumps({"Client id": "one", "Clients": []}),
        encoding="utf-8",
    )
    with pytest.raises(TodoError, match="Client id must be a positive whole number"):
        JsonStorage(path).load()


def test_load_invalid_client_id_negative(tmp_path):
    path = tmp_path / "tasks.json"
    path.write_text(
        json.dumps({"Client id": -5, "Clients": []}),
        encoding="utf-8",
    )
    with pytest.raises(TodoError, match="Client id must be a positive whole number"):
        JsonStorage(path).load()


def test_load_invalid_client_id_zero(tmp_path):
    path = tmp_path / "tasks.json"
    path.write_text(
        json.dumps({"Client id": 0, "Clients": []}),
        encoding="utf-8",
    )
    with pytest.raises(TodoError, match="Client id must be a positive whole number"):
        JsonStorage(path).load()


def test_save_creates_parent_directory(tmp_path):
    deep_path = tmp_path / "level1" / "level2" / "tasks.json"
    storage = JsonStorage(deep_path)
    storage.save([], 1)
    assert deep_path.exists()


def test_save_cleans_up_temporary_file(tmp_path):
    path = tmp_path / "tasks.json"
    storage = JsonStorage(path)
    storage.save([], 1)
    temp_file = path.with_suffix(".tmp")
    assert not temp_file.exists()
    assert path.exists()


def test_load_backward_compatible_with_legacy_tokens(tmp_path):
    path = tmp_path / "legacy.json"
    path.write_text(
        json.dumps(
            {
                "next_id": 3,
                "tasks": [
                    {
                        "task_id": 1,
                        "title": "Legacy Item",
                        "description": "legacy desc",
                        "priority": "high",
                        "tags": ["old"],
                        "status": "pending",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    tasks, next_id = JsonStorage(path).load()
    assert next_id == 3
    assert len(tasks) == 1
    assert tasks[0].task_id == 1
    assert tasks[0].title == "Legacy Item"
    assert tasks[0].priority == "high"
