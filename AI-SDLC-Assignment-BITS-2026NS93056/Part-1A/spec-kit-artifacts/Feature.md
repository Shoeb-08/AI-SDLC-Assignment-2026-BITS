# Feature Specification: Proserve Client Task Inventory Management

**Project**: Proserve Client Task Inventory Management  
**Assignment**: AI-Augmented SDLC, Part 1A  
**Created**: 2026-11-21  
**Status**: Accepted  
**Input**: `todo_requirements.txt`  
**Related artifacts**: `constitution.md`, `clarification.md`, `technical_plan.md`, `tasks.md`

## Summary

A student or other single user manages a personal task list from a text menu. The user can add a task, change it, delete it, mark it completed, filter by one tag, and sort by priority. Every successful change is stored in a JSON file so the list is still there the next time the program starts.

The delivery also includes pytest tests and a harness that writes lint, security, and test reports into `evidence/`.

## User Scenarios

### User Story 1 — Create and review tasks (Priority: P1)

A user starts the program, adds a task with a title and optional details, and then lists the tasks to confirm that the new item is present.

**Why this priority**: Without create and list, none of the other actions has anything to work on.

**Independent test**: Create two tasks and list them. The first id is 1, the second id is 2, and both are `pending`.

**Acceptance scenarios**:

1. **Given** an empty task file, **When** the user creates a task titled "Buy milk" with priority `high` and tag `home`, **Then** the task is stored with id 1, status `pending`, and those details.
2. **Given** a task list, **When** the user lists tasks, **Then** every saved task is shown with its id, title, description, priority, tags, and status.
3. **Given** the create prompt, **When** the user leaves the priority blank, **Then** the task is stored with priority `medium`.
4. **Given** the create prompt, **When** the title is blank, **Then** no task is stored and the user sees "Title is required."

### User Story 2 — Update a task (Priority: P1)

A user corrects the title, description, priority, tags, or status of an existing task. Blank answers keep the current value.

**Why this priority**: Tasks change after they are created. An update that applies only part of an invalid edit would leave bad data on disk.

**Independent test**: Update a low-priority draft to a high-priority final draft, and attempt a second update with priority `urgent`.

**Acceptance scenarios**:

1. **Given** task 1 exists, **When** the user supplies a new title, description, priority, and tags, **Then** those fields change and the file is saved.
2. **Given** task 1 exists, **When** the user leaves an update field blank, **Then** that field stays as it was.
3. **Given** task 1 has priority `low`, **When** the user sets priority to `urgent`, **Then** the task remains `low` and its other fields stay unchanged.
4. **Given** no task has the requested id, **When** the user tries to update it, **Then** the program reports that the task was not found.

### User Story 3 — Delete a task (Priority: P1)

A user removes a task that is no longer needed. The menu asks for confirmation before the delete is saved.

**Independent test**: Create a task, delete it, and confirm the list is empty. Request a missing id and confirm the error.

**Acceptance scenarios**:

1. **Given** a task exists, **When** the user confirms deletion, **Then** that task is removed from the JSON file.
2. **Given** the delete prompt, **When** the user answers anything other than `y`, **Then** the task remains.
3. **Given** a missing id, **When** the user requests deletion, **Then** the program reports that the task was not found and the file is unchanged.

### User Story 4 — Mark a task completed (Priority: P1)

A user finishes a task and marks it completed. Doing so again leaves it completed.

**Independent test**: Create a task, mark it completed, mark it again, and reload the file.

**Acceptance scenarios**:

1. **Given** a pending task, **When** the user marks it completed, **Then** its status is `completed` and the new status is saved.
2. **Given** a completed task, **When** the user marks it completed again, **Then** the status stays `completed`.
3. **Given** a completed task, **When** the user updates its status to `pending`, **Then** the task is open again.

### User Story 5 — Filter by tag (Priority: P2)

A user types one tag and sees only the tasks that carry that tag. `Uni` and `uni` match the same tag.

**Independent test**: Create one task tagged `Uni` and another tagged `home`, then filter by `uni`.

**Acceptance scenarios**:

1. **Given** tasks with different tags, **When** the user filters by one tag, **Then** only tasks containing that tag are returned.
2. **Given** a tag stored as `Uni`, **When** the user filters by `uni`, **Then** that task is included.
3. **Given** a blank filter, **When** the user submits it, **Then** the program reports "Tag is required." and does not list every task.

### User Story 6 — Sort by priority (Priority: P2)

A user sorts the list so high-priority work appears before medium and low. Two tasks with the same priority stay in id order.

**Independent test**: Create low, high, medium, and a second high task, then sort.

**Acceptance scenarios**:

1. **Given** tasks of mixed priority, **When** the user sorts, **Then** the order is high, then medium, then low.
2. **Given** two high-priority tasks, **When** the user sorts, **Then** the smaller task id comes first.
3. **Given** the user chooses sort from the menu, **When** the sort finishes, **Then** the new order is written to the JSON file.

### User Story 7 — Keep tasks in a JSON file (Priority: P1)

A user closes the program and starts it again. The same tasks, statuses, tags, and next id are loaded from the file.

**Independent test**: Save a completed task, construct a new Analyst with the same path, and create one more task.

**Acceptance scenarios**:

1. **Given** a saved task, **When** a new session opens that file, **Then** the title, tags, and status match what was saved.
2. **Given** the highest used id is 1, **When** the next task is created in a new session, **Then** its id is 2.
3. **Given** the file is missing or empty, **When** the program starts, **Then** the task list is empty and the next id is 1.
4. **Given** the file is not valid JSON, **When** the program starts, **Then** startup fails with an invalid-JSON error and exit code 1.
5. **Given** `Client id` in the file is lower than an existing task id, **When** the file loads, **Then** the next id moves past the highest existing id.

## Edge Cases

- A title or description with extra spaces is stored without those spaces.
- Priority and status values are accepted in any letter case and stored in lowercase.
- Tags may be entered as a list or as one comma-separated string.
- Empty tag entries are dropped. Tags that differ only by case are stored once, using the first spelling.
- A task id must be a positive whole number. Text and boolean values are rejected.
- A stored task object that lacks a required field cannot be loaded.
- Description may be empty. The menu shows `-` when description or tags are empty.
- Delete does not reuse the deleted id.
- The menu returns to the prompt after a `TodoError` instead of closing.
- End of input or Ctrl+C prints "Goodbye." and exits with code 0.

## Functional Requirements

- **FR-001**: The system must create a task with a generated id and status `pending`.
- **FR-002**: The system must update any combination of title, description, priority, tags, and status.
- **FR-003**: The system must delete a task by id after the menu user confirms.
- **FR-004**: The system must mark a task completed by id.
- **FR-005**: The system must filter tasks by one tag, ignoring case.
- **FR-006**: The system must sort tasks by priority from high to low, using task id as the tie-breaker.
- **FR-007**: The system must load and save all tasks in one JSON file.
- **FR-008**: Each task must contain task id, title, description, priority, tags, and status.
- **FR-009**: The system must reject a blank title, an unknown priority, an unknown status, a bad task id, and a blank filter tag.
- **FR-010**: The system must offer the seven task actions and Exit from a text menu.
- **FR-011**: The project must include pytest tests that cover the stories above.
- **FR-012**: The project must include harness scripts for lint, security, and tests, and those scripts must write reports under `evidence/`.

## Key Entity

**Task**

| Field | Rule |
| --- | --- |
| Task ID | Positive whole number, assigned by the system, never reused |
| Title | Required text |
| Description | Optional text |
| Priority | `low`, `medium`, or `high`; default `medium` |
| Tags | Zero or more text labels |
| Status | `pending` or `completed`; new tasks are `pending` |

The JSON document has this shape:

```json
{
  "Client id": 2,
  "Clients": [
    {
      "client_id": 1,
      "client_request": "Buy milk",
      "description": "2 litres",
      "Severity": "high",
      "tags": ["home"],
      "status": "pending"
    }
  ]
}
```

## Success Criteria

- **SC-001**: A user can complete create, list, update, delete, complete, filter, and sort from `python main.py` without editing code.
- **SC-002**: Closing and reopening the program shows the same tasks.
- **SC-003**: Invalid task data is rejected with a readable `TodoError` message.
- **SC-004**: `python harness/run_all.py` exits 0, and the evidence reports show lint PASS, security PASS, and tests PASS.
- **SC-005**: The accepted test run reports 24 passed tests.
- **SC-006**: The known limit remains visible: local JSON storage for a single user, with no concurrent-writer lock.

## Verification Map

| Requirement | Automated check |
| --- | --- |
| FR-001, FR-008 | `test_create_list_and_ids`, `test_task_round_trip_drops_duplicate_tags` |
| FR-002, FR-009 | `test_update_task`, `test_invalid_priority_does_not_change_task` |
| FR-003 | `test_delete_task`, `test_delete_missing_task` |
| FR-004 | `test_mark_completed`, `test_cli_create_complete_and_list` |
| FR-005 | `test_filter_by_tag_is_case_insensitive`, `test_filter_requires_a_tag` |
| FR-006 | `test_sort_by_priority`, `test_sort_can_be_saved` |
| FR-007 | `test_tasks_are_reloaded_from_json`, `test_save_and_load_round_trip`, `test_missing_file_starts_empty`, `test_empty_file_starts_empty`, `test_invalid_json`, `test_next_id_moves_past_existing_tasks` |
| FR-009 | `test_create_rejects_blank_title`, `test_rejects_blank_title`, `test_rejects_bad_priority`, `test_rejects_bad_status`, `test_rejects_non_numeric_task_id`, `test_from_dict_missing_field` |
| FR-010 | `test_cli_create_complete_and_list` |
| FR-011, FR-012 | `evidence/test_report.txt`, `evidence/lint_report.txt`, `evidence/security_report.txt`, `evidence/harness_summary.txt` |

## Out of Scope

- More than one user, login, or file locking
- A web or desktop graphical interface
- Due dates, reminders, search by title, and filters that combine several tags
- Cloud sync or a database server
- Reuse of deleted task ids

## Acceptance Decision

The harness log dated with this delivery records:

- Lint check: PASS
- Security check: PASS
- Tests: PASS (24)
- Final harness result: PASS
- Human review decision: ACCEPT
- Specification compliance: the acceptance scenarios above were checked by the automated tests and the harness
