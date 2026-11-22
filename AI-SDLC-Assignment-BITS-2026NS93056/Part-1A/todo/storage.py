"""Load and save tasks in a JSON file."""

import json
from pathlib import Path
from typing import List, Tuple

from todo.exceptions import TodoError
from todo.task import Task, validate_task_id


class JsonStorage:
    """Read and write the task list for one JSON file."""

    def __init__(self, file_path: str = "tasks.json") -> None:
        self.file_path = Path(file_path)

    def load(self) -> Tuple[List[Task], int]:
        """Return the saved tasks and the next id to use.

        A missing or empty file starts a new empty list.
        """
        if not self.file_path.exists():
            return [], 1

        raw = self.file_path.read_text(encoding="utf-8").strip()
        if not raw:
            return [], 1

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise TodoError(
                f"Could not read {self.file_path.name}: invalid JSON."
            ) from exc

        if not isinstance(data, dict):
            raise TodoError("JSON file must contain an object.")

        clients_data = data.get("Clients")
        if clients_data is None:
            clients_data = data.get("tasks")
        if clients_data is None or not isinstance(clients_data, list):
            raise TodoError("JSON file is missing the Clients list.")

        tasks = [Task.from_dict(item) for item in clients_data]
        next_id = data.get("Client id")
        if next_id is None:
            next_id = data.get("next_id", 1)
        if isinstance(next_id, bool) or not isinstance(next_id, int) or next_id < 1:
            raise TodoError("Client id must be a positive whole number.")

        highest = max((task.task_id for task in tasks), default=0)
        if next_id <= highest:
            next_id = highest + 1
        return tasks, next_id

    def save(self, tasks: List[Task], next_id: int) -> None:
        """Write tasks to disk, replacing the previous file."""
        validate_task_id(next_id)
        payload = {
            "Client id": next_id,
            "Clients": [task.to_dict() for task in tasks],
        }
        text = json.dumps(payload, indent=2)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.file_path.with_suffix(".tmp")
        temporary.write_text(text + "\n", encoding="utf-8")
        temporary.replace(self.file_path)
