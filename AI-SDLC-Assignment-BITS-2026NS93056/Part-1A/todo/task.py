"""Task data and the checks that keep each task valid."""

from typing import List, Optional

from todo.exceptions import TodoError

PRIORITIES = ("low", "medium", "high")
PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}
STATUSES = ("pending", "completed")


def validate_task_id(task_id: object) -> int:
    """Return a task id when it is a positive whole number."""
    if isinstance(task_id, bool) or not isinstance(task_id, int) or task_id < 1:
        raise TodoError("Task ID must be a positive whole number.")
    return task_id


validate_client_id = validate_task_id


def validate_title(title: object) -> str:
    """Return a cleaned title, or raise when the title is blank."""
    if not isinstance(title, str) or not title.strip():
        raise TodoError("Title is required.")
    return title.strip()


validate_client_request = validate_title


def validate_description(description: object) -> str:
    """Return a cleaned description. An empty description is allowed."""
    if description is None:
        return ""
    if not isinstance(description, str):
        raise TodoError("Description must be text.")
    return description.strip()


def validate_priority(priority: object) -> str:
    """Return a priority of low, medium, or high."""
    if not isinstance(priority, str):
        raise TodoError("Priority must be low, medium, or high.")
    cleaned = priority.strip().lower()
    if cleaned not in PRIORITIES:
        raise TodoError("Priority must be low, medium, or high.")
    return cleaned


validate_severity = validate_priority


def validate_status(status: object) -> str:
    """Return a status of pending or completed."""
    if not isinstance(status, str):
        raise TodoError("Status must be pending or completed.")
    cleaned = status.strip().lower()
    if cleaned not in STATUSES:
        raise TodoError("Status must be pending or completed.")
    return cleaned


def validate_tags(tags: Optional[object]) -> List[str]:
    """Return a list of tags.

    Tags may be given as a list or as one comma-separated string.
    Blank tags and repeated tags are removed.
    """
    if tags is None:
        return []
    if isinstance(tags, str):
        items = tags.split(",")
    elif isinstance(tags, list):
        items = tags
    else:
        raise TodoError("Tags must be a list of text values.")

    cleaned: List[str] = []
    seen = set()
    for item in items:
        if not isinstance(item, str):
            raise TodoError("Each tag must be text.")
        tag = item.strip()
        if not tag:
            continue
        key = tag.lower()
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(tag)
    return cleaned


class Task:
    """One todo item stored by the application."""

    def __init__(
        self,
        task_id: Optional[int] = None,
        title: Optional[str] = None,
        description: str = "",
        priority: str = "medium",
        tags: Optional[object] = None,
        status: str = "pending",
        client_id: Optional[int] = None,
        client_request: Optional[str] = None,
        severity: Optional[str] = None,
    ) -> None:
        actual_id = client_id if client_id is not None else task_id
        actual_title = client_request if client_request is not None else title
        actual_priority = severity if severity is not None else priority
        self.task_id = validate_task_id(actual_id)
        self.title = validate_title(actual_title)
        self.description = validate_description(description)
        self.priority = validate_priority(actual_priority)
        self.tags = validate_tags(tags)
        self.status = validate_status(status)

    @property
    def client_id(self) -> int:
        return self.task_id

    @client_id.setter
    def client_id(self, value: int) -> None:
        self.task_id = validate_task_id(value)

    @property
    def client_request(self) -> str:
        return self.title

    @client_request.setter
    def client_request(self, value: str) -> None:
        self.title = validate_title(value)

    @property
    def severity(self) -> str:
        return self.priority

    @severity.setter
    def severity(self, value: str) -> None:
        self.priority = validate_priority(value)

    def to_dict(self) -> dict:
        """Return this task as plain data that can be saved as JSON."""
        return {
            "client_id": self.task_id,
            "client_request": self.title,
            "description": self.description,
            "Severity": self.priority,
            "tags": list(self.tags),
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: object) -> "Task":
        """Build a task from data that was read from the JSON file."""
        if not isinstance(data, dict):
            raise TodoError("Each task must be a JSON object.")
        required = (
            "client_id",
            "client_request",
            "description",
            "Severity",
            "tags",
            "status",
        )
        missing = [
            field
            for field in required
            if field not in data
            and (field != "client_id" or "task_id" not in data)
            and (field != "client_request" or "title" not in data)
            and (field != "Severity" or "priority" not in data)
        ]
        if missing:
            names = ", ".join(missing)
            raise TodoError(f"Task is missing: {names}.")
        raw_id = data.get("client_id", data.get("task_id"))
        raw_request = data.get("client_request", data.get("title"))
        raw_severity = data.get("Severity", data.get("priority"))
        return cls(
            task_id=raw_id,
            title=raw_request,
            description=data["description"],
            priority=raw_severity,
            tags=data["tags"],
            status=data["status"],
        )
