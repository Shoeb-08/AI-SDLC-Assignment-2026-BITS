# Tasks: Proserve Client Task Inventory Management

**Project**: Proserve Client Task Inventory Management  
**Assignment**: AI-Augmented SDLC, Part 1A  
**Date**: 2026-11-21  
**Status**: Complete  
**Input**: `constitution.md`, `Feature.md`, `clarification.md`, `technical_plan.md`

## Format

`[x] Tnnn [P] [Story] Description`

- `[x]` means the task is done in the current tree
- `[P]` means the task could be done in parallel with other `[P]` tasks in the same phase
- `[Storyn]` is the user story in `Feature.md`

The tasks below are the work that produced the accepted Part 1A project. They are listed in the order the design depends on them.

## Phase 1 — Setup

**Goal**: A folder a reviewer can run from `Part-1A`.

- [x] T001 Create `requirements.txt` with `pytest>=7.0` and ignore `__pycache__/`, `.pytest_cache/`, `tasks.json`, and `*.tmp`
- [x] T002 [P] Add `README.md` with setup, `python main.py`, `--file`, and `python harness/run_all.py`
- [x] T003 [P] Add `main.py` and `todo/__main__.py` so the menu starts with `python main.py` or `python -m todo`

## Phase 2 — Foundations

**Goal**: Shared errors, field rules, and JSON storage before any user story.

- [x] T004 Add `TodoError` in `todo/exceptions.py`
- [x] T005 Implement validation and `Task.to_dict` / `Task.from_dict` in `todo/task.py` for id, title, description, priority, tags, and status
- [x] T006 Implement `JsonStorage.load` and `JsonStorage.save` in `todo/storage.py`, including empty-file startup, corrupt-JSON errors, next-id repair, and temp-file replace
- [x] T007 [P] Add `tests/conftest.py` with a temporary `TaskAnalyst` fixture and the project root on `sys.path`

**Checkpoint**: A task can be validated and written to a temporary JSON file without a menu.

## Phase 3 — User Story 1: Create and list

**Goal**: FR-001 and the list half of FR-010.

**Independent test**: `test_create_list_and_ids`, `test_create_rejects_blank_title`

- [x] T008 [Story1] Implement `TaskAnalyst.create_task` and `list_tasks` in `todo/analyst.py`, assigning ids only after validation and saving status `pending`
- [x] T009 [P] [Story1] Add create and list tests in `tests/test_manager.py` for ids 1 and 2, default pending status, comma-separated tags, and a blank title

## Phase 4 — User Story 2: Update

**Goal**: FR-002 and the "invalid update changes nothing" rule from clarification Q7.

**Independent test**: `test_update_task`, `test_invalid_priority_does_not_change_task`

- [x] T010 [Story2] Implement `get_task` and `update_task` so all new fields are checked before assignment
- [x] T011 [P] [Story2] Test a successful field change and a rejected priority that leaves title and priority untouched

## Phase 5 — User Story 3: Delete

**Goal**: FR-003.

**Independent test**: `test_delete_task`, `test_delete_missing_task`

- [x] T012 [Story3] Implement `delete_task` without reusing the deleted id
- [x] T013 [P] [Story3] Test removal of an existing task and the not-found error for a missing id

## Phase 6 — User Story 4: Mark completed

**Goal**: FR-004.

**Independent test**: `test_mark_completed`

- [x] T014 [Story4] Implement `mark_completed` as a status update to `completed`, including a repeated call
- [x] T015 [P] [Story4] Test the first completion and the second call that stays completed

## Phase 7 — User Story 5: Filter by tag

**Goal**: FR-005 and clarification Q5.

**Independent test**: `test_filter_by_tag_is_case_insensitive`, `test_filter_requires_a_tag`

- [x] T016 [Story5] Implement `filter_by_tag` with trimmed, case-insensitive matching and a required tag
- [x] T017 [P] [Story5] Test that `uni` matches a task tagged `Uni` and that a blank tag is rejected

## Phase 8 — User Story 6: Sort by priority

**Goal**: FR-006 and clarification Q2.

**Independent test**: `test_sort_by_priority`, `test_sort_can_be_saved`

- [x] T018 [Story6] Implement `sort_by_priority` ordered high, medium, low, then task id, with `save=False` by default
- [x] T019 [P] [Story6] Test the four-task order and a saved sort that changes `list_tasks`

## Phase 9 — User Story 7: JSON persistence

**Goal**: FR-007, FR-008, and clarification Q4, Q8, and Q9.

**Independent test**: storage tests plus `test_tasks_are_reloaded_from_json`

- [x] T020 [Story7] Reload a completed task in a new `TaskAnalyst` and confirm the following create receives id 2
- [x] T021 [P] [Story7] Test a missing file, a whitespace file, a save/load round trip, invalid JSON, a missing task field, and a `Client id` that must move past id 4
- [x] T022 [P] [Story7] Test tag de-duplication, rejected status, and a non-numeric task id in `tests/test_task.py`

## Phase 10 — Menu

**Goal**: FR-010 and clarification Q10.

**Independent test**: `test_cli_create_complete_and_list`

- [x] T023 [Story1] Implement the eight-option menu in `todo/cli.py`, including defaults, blank-keeps-current update, delete confirmation, and `--file`
- [x] T024 [Story4] Add a scripted CLI test that creates "Submit report", marks task 1 completed, lists it, and exits 0

## Phase 11 — Harness and evidence

**Goal**: FR-011, FR-012, and clarification Q12.

**Independent test**: `python harness/run_all.py` exits 0.

- [x] T025 [P] Implement `harness/lint_check.py` and write `evidence/lint_report.txt`
- [x] T026 [P] Implement `harness/security_check.py` for the six agreed patterns and write `evidence/security_report.txt`
- [x] T027 [P] Implement `harness/run_tests.py` and write `evidence/test_report.txt`
- [x] T028 Implement `harness/run_all.py` and write `evidence/harness_summary.txt`
- [x] T029 Run the harness and keep the passing reports in `evidence/`

## Phase 12 — Review

**Goal**: Constitution gate 8.

- [x] T030 Confirm the run used for acceptance: lint PASS (17 files), security PASS (12 files), tests PASS (64)
- [x] T031 Record the human review decision ACCEPT and the single-user JSON limit in `evidence/harness-log.md`
- [x] T032 Confirm each functional requirement has a row in the specification verification map

## Dependencies

```text
T001–T003  setup
    ->
T004–T007  foundations
    ->
T008–T009  Story1 create/list
    ->
T010–T022  Story2 through Story7 can proceed after create exists
    ->
T023–T024  menu, after the Analyst methods exist
    ->
T025–T029  harness, after tests exist
    ->
T030–T032  review
```

Story2, Story3, Story4, Story5, and Story6 touch different methods and different tests, so their test tasks were safe to write alongside one another once `create_task` existed. Storage edge cases in Story7 depend on T006.

## Parallel Groups

| Group | Tasks | Why they do not block each other |
| --- | --- | --- |
| Docs and entry points | T002, T003 | README text and startup scripts |
| Story tests after create | T011, T013, T015, T017, T019 | Separate test functions |
| Persistence tests | T021, T022 | Storage tests and task-rule tests |
| Harness scripts | T025, T026, T027 | Three different evidence files |

## Acceptance Checklist

| Story | Demo path | Done when |
| --- | --- | --- |
| Story1 | Menu options 1 and 2 | New task appears with a new id and status pending |
| Story2 | Menu option 3 | Changed fields persist; an illegal priority does not |
| Story3 | Menu option 4 | `y` removes the task; any other answer does not |
| Story4 | Menu option 5 | Status prints `completed` and survives a restart |
| Story5 | Menu option 6 | One tag, ignoring case, returns the matching tasks |
| Story6 | Menu option 7 | Order is high, medium, low, and the file keeps that order |
| Story7 | Stop and run `python main.py` again | The same tasks load; a bad file exits with an error |

## Completion Record

| Item | Result |
| --- | --- |
| Tasks T001–T032 | Complete |
| Pytest | 64 passed |
| Lint | PASS, 0 issues |
| Security | PASS, 0 issues |
| Harness | PASS |
| Human review | ACCEPT |
| Open tasks | None |
