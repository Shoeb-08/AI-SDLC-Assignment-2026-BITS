"""A menu test suite using scripted answers."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from todo.cli import main
from todo.storage import JsonStorage
from todo.task import Task


def test_cli_create_complete_and_list(tmp_path, monkeypatch, capsys):
    answers = iter(
        [
            "1",
            "Submit report",
            "Part 1A",
            "high",
            "uni, assignment",
            "5",
            "1",
            "2",
            "8",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))
    path = tmp_path / "tasks.json"

    exit_code = main(["--file", str(path)])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Created task 1." in output
    assert "Submit report" in output
    assert "Task 1 marked as completed." in output
    assert "Status:      completed" in output
    assert path.exists()


def test_cli_exit_immediately(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _prompt: "8")
    path = tmp_path / "tasks.json"
    exit_code = main(["--file", str(path)])
    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Goodbye." in output


def test_cli_invalid_menu_choice(tmp_path, monkeypatch, capsys):
    answers = iter(["99", "abc", "8"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))
    path = tmp_path / "tasks.json"
    exit_code = main(["--file", str(path)])
    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Please choose a number from 1 to 8." in output


def test_cli_list_empty_tasks(tmp_path, monkeypatch, capsys):
    answers = iter(["2", "8"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))
    path = tmp_path / "tasks.json"
    exit_code = main(["--file", str(path)])
    output = capsys.readouterr().out
    assert exit_code == 0
    assert "No tasks found." in output


def test_cli_delete_cancelled(tmp_path, monkeypatch, capsys):
    path = tmp_path / "tasks.json"
    storage = JsonStorage(path)
    storage.save([Task(1, "Keep me", "desc", "low", ["a"], "pending")], 2)

    answers = iter(["4", "1", "n", "2", "8"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))
    exit_code = main(["--file", str(path)])
    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Delete cancelled." in output
    assert "Keep me" in output


def test_cli_delete_confirmed(tmp_path, monkeypatch, capsys):
    path = tmp_path / "tasks.json"
    storage = JsonStorage(path)
    storage.save([Task(1, "Remove me", "desc", "low", ["a"], "pending")], 2)

    answers = iter(["4", "1", "y", "2", "8"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))
    exit_code = main(["--file", str(path)])
    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Deleted task 1." in output
    assert "No tasks found." in output


def test_cli_filter_by_tag(tmp_path, monkeypatch, capsys):
    path = tmp_path / "tasks.json"
    storage = JsonStorage(path)
    storage.save(
        [
            Task(1, "Study Python", "desc", "medium", ["education"], "pending"),
            Task(2, "Buy groceries", "desc", "low", ["home"], "pending"),
        ],
        3,
    )

    answers = iter(["6", "education", "8"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))
    exit_code = main(["--file", str(path)])
    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Study Python" in output
    assert "Buy groceries" not in output


def test_cli_sort_tasks(tmp_path, monkeypatch, capsys):
    path = tmp_path / "tasks.json"
    storage = JsonStorage(path)
    storage.save(
        [
            Task(1, "Low item", "desc", "low", [], "pending"),
            Task(2, "High item", "desc", "high", [], "pending"),
        ],
        3,
    )

    answers = iter(["7", "8"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))
    exit_code = main(["--file", str(path)])
    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Tasks sorted by priority (high, medium, then low)." in output
    assert output.find("High item") < output.find("Low item")


def test_cli_update_task_fields(tmp_path, monkeypatch, capsys):
    path = tmp_path / "tasks.json"
    storage = JsonStorage(path)
    storage.save([Task(1, "Old Title", "Old Desc", "low", ["t1"], "pending")], 2)

    answers = iter(["3", "1", "New Title", "", "", "", "", "2", "8"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))
    exit_code = main(["--file", str(path)])
    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Updated task 1." in output
    assert "New Title" in output


def test_cli_invalid_task_id_format(tmp_path, monkeypatch, capsys):
    answers = iter(["3", "not_a_number", "8"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))
    path = tmp_path / "tasks.json"
    exit_code = main(["--file", str(path)])
    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Error: Task ID must be a positive whole number." in output


def test_cli_corrupt_file_startup(tmp_path, capsys):
    path = tmp_path / "corrupt.json"
    path.write_text("{broken json", encoding="utf-8")
    exit_code = main(["--file", str(path)])
    output = capsys.readouterr().out
    assert exit_code == 1
    assert "Error: Could not read corrupt.json: invalid JSON." in output
