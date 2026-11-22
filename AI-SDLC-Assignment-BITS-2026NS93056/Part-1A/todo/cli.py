"""Text menu for the Proserve Client Task Inventory Management."""

import argparse
from typing import List, Optional

from todo.exceptions import TodoError
from todo.analyst import TaskAnalyst
from todo.task import Task


def prompt(text: str) -> str:
    """Read one line of input and remove extra spaces."""
    return input(text).strip()


def print_menu(file_path: str) -> None:
    """Show the main menu."""
    print()
    print("Proserve Client Task Inventory Management")
    print(f"Storage file: {file_path}")
    print("1. Create a task")
    print("2. List tasks")
    print("3. Update a task")
    print("4. Delete a task")
    print("5. Mark a task as completed")
    print("6. Filter tasks by tag")
    print("7. Sort tasks by priority")
    print("8. Exit")


def print_tasks(tasks: List[Task]) -> None:
    """Print tasks in a simple block for each task."""
    if not tasks:
        print("No tasks found.")
        return
    print(f"{len(tasks)} task(s):")
    for task in tasks:
        tag_text = ", ".join(task.tags) if task.tags else "-"
        print("-" * 40)
        print(f"ID:          {task.task_id}")
        print(f"Title:       {task.title}")
        print(f"Description: {task.description or '-'}")
        print(f"Priority:    {task.priority}")
        print(f"Tags:        {tag_text}")
        print(f"Status:      {task.status}")


def prompt_task_id() -> int:
    """Ask for a task id and check that it looks like a whole number."""
    raw = prompt("Task ID: ")
    if not raw.isdigit():
        raise TodoError("Task ID must be a positive whole number.")
    return int(raw)


def create_task(Analyst: TaskAnalyst) -> None:
    """Ask for task details and store a new task."""
    title = prompt("Title: ")
    description = prompt("Description: ")
    priority = prompt("Priority (low/medium/high) [medium]: ") or "medium"
    tags = prompt("Tags (comma separated): ")
    task = Analyst.create_task(title, description, priority, tags)
    print(f"Created task {task.task_id}.")


def update_task(Analyst: TaskAnalyst) -> None:
    """Ask which fields to change. A blank answer keeps the old value."""
    task = Analyst.get_task(prompt_task_id())
    print_tasks([task])
    title = prompt("New title [keep current]: ")
    description = prompt("New description [keep current]: ")
    priority = prompt("New priority (low/medium/high) [keep current]: ")
    tags = prompt("New tags, comma separated [keep current]: ")
    status = prompt("New status (pending/completed) [keep current]: ")
    Analyst.update_task(
        task.task_id,
        title=title or None,
        description=description or None,
        priority=priority or None,
        tags=tags or None,
        status=status or None,
    )
    print(f"Updated task {task.task_id}.")


def delete_task(Analyst: TaskAnalyst) -> None:
    """Delete a task after a yes/no check."""
    task_id = prompt_task_id()
    task = Analyst.get_task(task_id)
    confirm = prompt(f"Delete '{task.title}'? (y/n): ")
    if confirm.lower() != "y":
        print("Delete cancelled.")
        return
    Analyst.delete_task(task_id)
    print(f"Deleted task {task_id}.")


def mark_completed(Analyst: TaskAnalyst) -> None:
    """Mark one task as completed."""
    task = Analyst.mark_completed(prompt_task_id())
    print(f"Task {task.task_id} marked as completed.")


def filter_tasks(Analyst: TaskAnalyst) -> None:
    """Show tasks that have the requested tag."""
    tag = prompt("Tag: ")
    print_tasks(Analyst.filter_by_tag(tag))


def sort_tasks(Analyst: TaskAnalyst) -> None:
    """Sort saved tasks by priority and show the new order."""
    tasks = Analyst.sort_by_priority(save=True)
    print("Tasks sorted by priority (high, medium, then low).")
    print_tasks(tasks)


def list_tasks(Analyst: TaskAnalyst) -> None:
    """Show every saved task."""
    print_tasks(Analyst.list_tasks())


def main(argv: Optional[List[str]] = None) -> int:
    """Run the menu until the user exits."""
    parser = argparse.ArgumentParser(description="Proserve Client Task Inventory Management")
    parser.add_argument(
        "--file",
        default="tasks.json",
        help="Path to the JSON file used to store tasks",
    )
    args = parser.parse_args(argv)

    try:
        Analyst = TaskAnalyst(args.file)
    except TodoError as exc:
        print(f"Error: {exc}")
        return 1

    actions = {
        "1": create_task,
        "2": list_tasks,
        "3": update_task,
        "4": delete_task,
        "5": mark_completed,
        "6": filter_tasks,
        "7": sort_tasks,
    }

    while True:
        print_menu(args.file)
        try:
            choice = prompt("Choose an option: ")
            if choice == "8":
                print("Goodbye.")
                return 0
            action = actions.get(choice)
            if action is None:
                print("Please choose a number from 1 to 8.")
                continue
            action(Analyst)
        except TodoError as exc:
            print(f"Error: {exc}")
        except (EOFError, KeyboardInterrupt):
            print()
            print("Goodbye.")
            return 0
