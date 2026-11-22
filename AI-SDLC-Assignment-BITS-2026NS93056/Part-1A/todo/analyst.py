"""Create, update, filter, and sort tasks."""

from typing import List, Optional

from todo.exceptions import TodoError
from todo.storage import JsonStorage
from todo.task import (
    PRIORITY_RANK,
    Task,
    validate_description,
    validate_priority,
    validate_status,
    validate_tags,
    validate_task_id,
    validate_title,
)


class TaskAnalyst:
    """The main application service for the Proserve Client Task Inventory Management."""

    def __init__(self, file_path: str = "tasks.json") -> None:
        self.storage = JsonStorage(file_path)
        self._tasks, self._next_id = self.storage.load()

    def create_task(
        self,
        title: str,
        description: str = "",
        priority: str = "medium",
        tags: Optional[object] = None,
    ) -> Task:
        """Add a new pending task and save it."""
        task = Task(
            task_id=self._next_id,
            title=title,
            description=description,
            priority=priority,
            tags=tags,
            status="pending",
        )
        self._next_id += 1
        self._tasks.append(task)
        self._save()
        return task

    def list_tasks(self) -> List[Task]:
        """Return the tasks in their current saved order."""
        return list(self._tasks)

    def get_task(self, task_id: int) -> Task:
        """Return one task, or raise when the id does not exist."""
        task_id = validate_task_id(task_id)
        for task in self._tasks:
            if task.task_id == task_id:
                return task
        raise TodoError(f"Task {task_id} was not found.")

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[str] = None,
        tags: Optional[object] = None,
        status: Optional[str] = None,
    ) -> Task:
        """Change the given fields of a task and save it.

        Fields left as None stay as they are. All new values are checked
        before the task is changed.
        """
        task = self.get_task(task_id)
        new_title = task.title if title is None else validate_title(title)
        if description is None:
            new_description = task.description
        else:
            new_description = validate_description(description)
        if priority is None:
            new_priority = task.priority
        else:
            new_priority = validate_priority(priority)
        new_tags = task.tags if tags is None else validate_tags(tags)
        new_status = task.status if status is None else validate_status(status)

        task.title = new_title
        task.description = new_description
        task.priority = new_priority
        task.tags = new_tags
        task.status = new_status
        self._save()
        return task

    def delete_task(self, task_id: int) -> Task:
        """Remove a task and save the remaining list."""
        task = self.get_task(task_id)
        self._tasks = [
            item for item in self._tasks if item.task_id != task.task_id
        ]
        self._save()
        return task

    def mark_completed(self, task_id: int) -> Task:
        """Set a task's status to completed and save it."""
        return self.update_task(task_id, status="completed")

    def filter_by_tag(self, tag: str) -> List[Task]:
        """Return tasks that include the given tag."""
        if not isinstance(tag, str) or not tag.strip():
            raise TodoError("Tag is required.")
        needle = tag.strip().lower()
        return [
            task
            for task in self._tasks
            if any(existing.lower() == needle for existing in task.tags)
        ]

    def sort_by_priority(self, save: bool = False) -> List[Task]:
        """Return tasks from high priority to low priority.

        When two tasks have the same priority, the smaller task id comes
        first. Pass save=True to store this order in the JSON file.
        """
        ordered = sorted(
            self._tasks,
            key=lambda task: (PRIORITY_RANK[task.priority], task.task_id),
        )
        if save:
            self._tasks = ordered
            self._save()
        return list(ordered)

    def _save(self) -> None:
        self.storage.save(self._tasks, self._next_id)


TodoManager = TaskAnalyst

