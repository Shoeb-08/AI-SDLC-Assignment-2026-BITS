# Clarification Record: Proserve Client Task Inventory Management

**Project**: Proserve Client Task Inventory Management  
**Assignment**: AI-Augmented SDLC, Part 1A  
**Session date**: 2026-11-21  
**Status**: Closed  
**Source brief**: `todo_requirements.txt`  
**Applies to**: `Feature.md` version accepted on 2026-11-22

## Why this record exists

The brief names the required actions and the six task fields. It does not define allowed values, sort order, id rules, tag matching, file format, or what should happen when input is wrong. The questions below were resolved before the behaviour was treated as accepted. Each answer matches the code in `todo/` and the tests in `tests/`.

No question was left open. No answer removed a feature from the brief.

## Session 2026-11-21

### Q1. Which priority values are allowed?

**Answer**: The only priorities are `low`, `medium`, and `high`. Values are stored in lowercase, so `HIGH` is accepted and saved as `high`. When the user leaves priority blank on create, the value is `medium`. Any other value raises `TodoError` with "Priority must be low, medium, or high."

**Reason**: The brief says "priority" but does not give a scale. Three named levels are enough for a student project and are easy to test.

**Specification impact**: FR-008, FR-009, User Story 1 scenario 3, User Story 2 scenario 3.

### Q2. What order does "sort by priority" use?

**Answer**: High comes first, then medium, then low. If two tasks share a priority, the smaller task id comes first. Calling `sort_by_priority()` only returns the ordered list. The menu uses `sort_by_priority(save=True)`, so the JSON file keeps that order.

**Reason**: "High priority" is the usual meaning of sorting by priority. Saving from the menu makes the result visible after a restart. The library method can still sort for display without rewriting the file.

**Specification impact**: FR-006, User Story 6.

### Q3. What are the status values, and can a task be reopened?

**Answer**: Status is `pending` or `completed`. Every new task is `pending`. Mark completed sets the status to `completed` and is safe to repeat. Update may set the status back to `pending`.

**Reason**: The brief asks for both update and mark-completed. Mark-completed is the direct action. Update covers the less common case of reopening a task.

**Specification impact**: FR-001, FR-004, User Story 4.

### Q4. How is the task id chosen?

**Answer**: Ids are positive whole numbers starting at 1. The file stores `Client id`. Creating a task uses the current next id and then adds one. Deleted ids are not reused. If a file says `Client id` is less than or equal to an existing id, load moves `Client id` to one past the highest id.

**Reason**: Stable ids keep update, delete, and complete unambiguous. Repairing a low `Client id` avoids two tasks with the same id after a hand-edited file.

**Specification impact**: FR-007, FR-008, User Story 7 scenario 5.

### Q5. How do tags work?

**Answer**: A task may have many tags. The caller may pass a list or a comma-separated string. Surrounding spaces are removed. Empty pieces are ignored. Two tags that match except for case are stored once, keeping the first spelling. Filter takes one tag and matches it without caring about case. A blank filter raises "Tag is required."

**Reason**: The brief says "filter tasks using tags" but not whether matching is case-sensitive or whether several tags are combined. One tag, compared without case, matches the menu prompt and is covered directly by tests.

**Specification impact**: FR-005, FR-008, User Story 5.

### Q6. Which fields are required?

**Answer**: Title is required after trimming. Description may be empty. Tags may be empty. Priority and status always have a valid value because defaults and checks fill them.

**Reason**: A task with no title cannot be recognised in a list. The other fields have sensible empty or default states.

**Specification impact**: FR-009, User Story 1 scenario 4.

### Q7. What happens when an update is partly invalid?

**Answer**: All new values are checked before any field on the task changes. If priority, status, title, description, or tags is invalid, the saved task stays as it was.

**Reason**: A partial write would make it unclear which fields the user successfully changed.

**Specification impact**: FR-002, FR-009, User Story 2 scenario 3. Covered by `test_invalid_priority_does_not_change_task`.

### Q8. What if the JSON file is missing, empty, or corrupt?

**Answer**: A missing file or a file that is only whitespace starts an empty list with `Client id` 1. A file that is not valid JSON raises `TodoError` mentioning "invalid JSON". The menu prints that error and exits with code 1. The program does not replace a corrupt file with an empty one during startup.

**Reason**: A new user should be able to start with no file. A damaged file should be visible, not silently erased.

**Specification impact**: FR-007, User Story 7 scenarios 3 and 4.

### Q9. What does the JSON document contain?

**Answer**: One object with `Client id` and `Clients`. Each task object has `client_id`, `client_request`, `description`, `Severity`, `tags`, and `status`. Extra missing fields on a task raise `TodoError`. The file is written as indented UTF-8 JSON. The write uses a temporary file in the same folder and then replaces the real file.

**Reason**: The brief requires JSON storage and names the task fields. An explicit document shape makes the tests and a hand inspection of `tasks.json` agree.

**Specification impact**: FR-007, FR-008.

### Q10. How does the user operate the program?

**Answer**: The interface is a numbered menu:

1. Create a task
2. List tasks
3. Update a task
4. Delete a task
5. Mark a task as completed
6. Filter tasks by tag
7. Sort tasks by priority
8. Exit

A blank answer during update keeps the current field. Delete asks `y/n` and deletes only on `y`. The default storage path is `tasks.json`. `python main.py --file <path>` selects another file. `python -m todo` starts the same menu.

**Reason**: The brief asks for an application, not only a library. A menu is enough for a demonstration and for the CLI test.

**Specification impact**: FR-010, SC-001.

### Q11. Who is the user, and is sharing in scope?

**Answer**: There is one local user. There is no login, no network API, and no lock for two programs writing the same file. That limit is accepted and is recorded in the harness log.

**Reason**: The assignment asks for a simple beginner-friendly Python program. Concurrent use would need rules the brief does not mention.

**Specification impact**: Known limit in the constitution, specification, and plan. SC-006.

### Q12. What must the harness check?

**Answer**: Three scripts, plus one script that runs all of them.

- `harness/lint_check.py` compiles every project Python file and reports tabs, trailing spaces, and lines longer than 100 characters. It writes `evidence/lint_report.txt`.
- `harness/security_check.py` scans `todo/` and `tests/` for `eval`, `exec`, `pickle`, `os.system`, `shell=True`, and hardcoded secret assignments. It writes `evidence/security_report.txt`. It does not scan `harness/`, because those pattern strings are the search terms.
- `harness/run_tests.py` runs pytest and writes `evidence/test_report.txt`.
- `harness/run_all.py` runs the three checks and writes `evidence/harness_summary.txt`.

The accepted run checked 17 Python files for lint and 12 files for security, with 0 issues, and recorded 24 passed tests.

**Reason**: The brief asks for lint, security, test execution, and an evidence folder. A small scanner that runs without extra tools satisfies that request for this assignment. It is not a substitute for a full security product.

**Specification impact**: FR-011, FR-012, SC-004, SC-005.

### Q13. Which dependency is allowed?

**Answer**: Application code uses only the Python standard library. `requirements.txt` lists `pytest>=7.0`. The verified environment is Python 3.12.7 and pytest 7.4.4.

**Reason**: The constitution limits third-party code so the project stays easy to run in a teaching lab.

**Specification impact**: Constitution principle 1 and the plan’s technical context.

## Decisions that were considered and not taken

| Alternative | Why it was not used |
| --- | --- |
| Numeric priority such as 1–5 | The three named levels are easier to type in the menu and match the tests that already describe high, medium, and low. |
| Reusing deleted ids | Reuse would let a later task be confused with a deleted one in notes or screenshots. |
| Filtering by several tags with AND or OR | The brief is satisfied by one tag. A combined filter was not specified and has no test. |
| A database or web API | The brief requires a JSON file and a simple Python structure. |
| Scanning the harness folder for the security patterns | The scanner would report its own search strings. The application and tests are the code under review. |

## Trace to the accepted build

| Decision | Where it lives in code | Test that locks it in |
| --- | --- | --- |
| Q1 Priority set and default | `todo/task.py` | `test_rejects_bad_priority`, `test_create_list_and_ids` |
| Q2 Sort order and save | `todo/analyst.py`, `todo/cli.py` | `test_sort_by_priority`, `test_sort_can_be_saved` |
| Q3 Status and reopen | `todo/analyst.py` | `test_mark_completed` |
| Q4 Ids | `todo/storage.py`, `todo/analyst.py` | `test_next_id_moves_past_existing_tasks`, `test_tasks_are_reloaded_from_json` |
| Q5 Tags | `todo/task.py`, `todo/analyst.py` | `test_filter_by_tag_is_case_insensitive`, `test_task_round_trip_drops_duplicate_tags` |
| Q6 Required title | `todo/task.py` | `test_create_rejects_blank_title`, `test_rejects_blank_title` |
| Q7 Atomic field update | `todo/analyst.py` | `test_invalid_priority_does_not_change_task` |
| Q8 File recovery rules | `todo/storage.py`, `todo/cli.py` | `test_missing_file_starts_empty`, `test_empty_file_starts_empty`, `test_invalid_json` |
| Q9 JSON shape | `todo/storage.py` | `test_save_and_load_round_trip`, `test_from_dict_missing_field` |
| Q10 Menu | `todo/cli.py` | `test_cli_create_complete_and_list` |
| Q12 Harness | `harness/` | `evidence/harness_summary.txt` |

## Closure

All clarifications are reflected in the accepted specification. Further product changes need a new clarification session and a matching test before they replace any answer in this record.
