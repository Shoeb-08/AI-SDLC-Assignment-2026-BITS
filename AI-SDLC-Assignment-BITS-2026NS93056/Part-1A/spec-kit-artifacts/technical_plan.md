# Implementation Plan: Proserve Client Task Inventory Management

**Project**: Proserve Client Task Inventory Management  
**Assignment**: AI-Augmented SDLC, Part 1A  
**Date**: 2026-11-21  
**Status**: Implemented and accepted  
**Spec**: `spec-kit-artifacts/Feature.md`  
**Clarifications**: `spec-kit-artifacts/clarification.md`  
**Constitution**: `spec-kit-artifacts/constitution.md`

## Summary

The application is a small Python package with a text menu. `TaskAnalyst` owns the task list and calls `JsonStorage` after every successful change. `Task` and the validate functions in `todo/task.py` enforce the field rules from the clarification record. Pytest covers the Analyst, storage, task rules, and one scripted menu flow. The harness runs lint, a pattern security scan, and pytest, then stores the output in `evidence/`.

This plan describes the design that was built. It is not a proposal for a different architecture.

## Technical Context

| Item | Choice |
| --- | --- |
| Language | Python 3.9+ (verified on Python 3.12.7) |
| Dependencies | pytest 7 or newer only (`requirements.txt`) |
| Interface | Numbered CLI menu in `todo/cli.py` |
| Entry points | `python main.py`, `python -m todo` |
| Storage | UTF-8 JSON file, default `tasks.json`, override with `--file` |
| Testing | pytest, temporary files through `tmp_path` |
| Platform | Local Windows, macOS, or Linux terminal |
| Performance goal | Correctness for a personal list of ordinary size; no throughput target |
| Scale | One user, one process, one file |
| Security approach | Input validation, no dynamic code execution, harness pattern scan |

## Constitution Check

Checked before implementation and again against the accepted tree.

| Principle | Result | How the design meets it |
| --- | --- | --- |
| Stay small and readable | Pass | Six application modules, no web framework, no database driver |
| Trace every feature | Pass | FR-001 to FR-012 map to modules and to the verification table in the specification |
| Check values before changing a task | Pass | `update_task` validates every new field, then assigns |
| One local JSON file | Pass | `JsonStorage` reads and writes a single document |
| Automated tests | Pass | 24 pytest tests, isolated from the developer’s real task file |
| Record quality evidence | Pass | `harness/run_all.py` writes four evidence files |
| Safe local code | Pass | Security scan of `todo/` and `tests/` reported 0 issues |
| Human acceptance | Pass | Harness log decision is ACCEPT, with the single-user limit stated |

No constitution exception was required. The complexity table at the end of this plan is empty.

## Architecture

```text
main.py / python -m todo
        |
        v
   todo/cli.py          menu, prompts, printing
        |
        v
 todo/analyst.py        create, update, delete, complete, filter, sort
        |                    |
        |                    v
        |              todo/task.py
        |              Task, validation, priority order
        v
  todo/storage.py       load and save JSON
        |
        v
   tasks.json

todo/exceptions.py      TodoError, used by every layer
```

The menu depends on the Analyst. The Analyst depends on storage and task rules. Storage depends on `Task`. Nothing in `task.py` or `exceptions.py` imports the Analyst or the menu, so the rules can be tested without a terminal.

### Module responsibilities

| Module | Responsibility |
| --- | --- |
| `todo/exceptions.py` | `TodoError` for expected failures |
| `todo/task.py` | Field checks, `Task.to_dict`, `Task.from_dict`, priority rank |
| `todo/storage.py` | `JsonStorage.load` and `JsonStorage.save` |
| `todo/analyst.py` | `TaskAnalyst` use cases and when to save |
| `todo/manager.py` | Compatibility re-export of `TaskAnalyst` as `TodoManager` |
| `todo/cli.py` | Argument parsing, menu loop, confirmation, messages |
| `todo/__main__.py` | `python -m todo` |
| `main.py` | Assignment-friendly startup script |
| `tests/` | Unit and one CLI flow test |
| `harness/` | Lint, security, pytest, and the combined runner |
| `evidence/` | Reports produced by the harness |

## Behaviour Design

### Create

`create_task` builds a `Task` with the current next id and status `pending`. The id increments only after construction succeeds, so a rejected title does not consume an id. The new task is appended and the file is saved.

### Update and complete

`update_task` loads the task, computes the next value of each field, and assigns those values only after every check has passed. `None` means "leave this field alone", which is how the menu represents a blank answer. `mark_completed` is an update that sets status to `completed`.

### Delete

`delete_task` removes the matching id and saves. It does not change `Client id`. The menu calls this only after the user types `y`.

### Filter and sort

`filter_by_tag` returns a new list and does not save. Comparison is the tag in lowercase. `sort_by_priority` sorts by `(priority rank, task id)`. The menu passes `save=True` so the displayed order and the file order match.

### Storage

`load` returns `([], 1)` when the file is absent or blank. Otherwise it requires a JSON object with a `Clients` list. Each item goes through `Task.from_dict`. `save` writes `*.tmp` beside the target and replaces the target. Parent folders are created when a nested path is used.

Startup does not catch `TodoError` inside the Analyst. The menu catches it, prints `Error: ...`, and returns exit code 1 when the file cannot be loaded. Later menu errors are printed and the loop continues.

## Data Model

```text
Task
  client_id: int >= 1
  client_request: non-empty str
  description: str
  Severity: low | medium | high
  tags: list[str]
  status: pending | completed

Document
  Client id: int >= 1
  Clients: list[Task]
```

Priority rank used only for sorting: high = 0, medium = 1, low = 2.

## Project Layout

```text
Part-1A/
  main.py
  requirements.txt
  README.md
  todo_requirements.txt
  todo/
    __init__.py
    __main__.py
    exceptions.py
    task.py
    storage.py
    analyst.py
    manager.py
    cli.py
  tests/
    conftest.py
    test_task.py
    test_storage.py
    test_manager.py
    test_cli.py
  harness/
    lint_check.py
    security_check.py
    run_tests.py
    run_all.py
  evidence/
    lint_report.txt
    security_report.txt
    test_report.txt
    harness_summary.txt
    harness-log.md
  spec-kit-artifacts/
    constitution.md
    Feature.md
    clarification.md
    technical_plan.md
    tasks.md
```

## Test Plan

Tests import the package from the `Part-1A` folder. `conftest.py` gives each Analyst test its own temporary JSON file.

| Area | File | Intent |
| --- | --- | --- |
| Field rules | `tests/test_task.py` | Title, priority, status, id, tags, missing JSON fields |
| File rules | `tests/test_storage.py` | Missing, empty, round trip, corrupt JSON, next-id repair |
| Use cases | `tests/test_manager.py` | Create, update, delete, complete, filter, sort, reload |
| Menu | `tests/test_cli.py` | Scripted create, complete, list, and exit |

The CLI test replaces `input` and checks the printed confirmation lines, including `Task 1 marked as completed.` and `Status:      completed`. It also checks that the chosen file was created.

Harness execution is the integration check for FR-012. It is run with `python harness/run_all.py` from `Part-1A`.

## Error Handling

| Situation | Result |
| --- | --- |
| Blank title | `TodoError`: Title is required. |
| Bad priority or status | `TodoError` naming the allowed values |
| Bad or missing task id | `TodoError`: task id rule, or task was not found |
| Blank tag filter | `TodoError`: Tag is required. |
| Invalid JSON | `TodoError`: invalid JSON; menu exit code 1 |
| Task object is not a JSON object, or a field is missing | `TodoError` during load |
| Unknown menu number | Message asking for a number from 1 to 8; program stays open |
| EOF or keyboard interrupt | "Goodbye." and exit code 0 |

## Harness Design

Lint walks the project for `*.py`, skips `__pycache__`, `.pytest_cache`, and `evidence`, compiles each file, and checks line length 100.

Security reads Python files under `todo/` and `tests/` and looks for six patterns: `eval(`, `exec(`, `pickle`, `os.system(`, `shell=True`, and an assignment that looks like a password, API key, or secret.

Test execution uses `python -m pytest -v` with the working directory set to `Part-1A`. If pytest is missing, the script writes a short install message and exits 1.

`run_all.py` runs the three scripts in order and records each exit code. The summary result is PASS only when every code is 0.

## Accepted Run

Recorded in `evidence/harness_summary.txt` and `evidence/harness-log.md`:

| Check | Result |
| --- | --- |
| Lint | PASS, 17 files, 0 issues |
| Security | PASS, 12 files, 0 issues |
| Tests | PASS, 24 passed |
| Human review | ACCEPT |

## Risks and Accepted Limits

| Limit | Effect | Accepted because |
| --- | --- | --- |
| No file lock | Two running copies can overwrite each other | Single-user assignment scope |
| Security scan is textual | It will not find every unsafe pattern | The brief asks for a harness suitable for the assignment, and the application code is small enough to read |
| Menu confirmation is not unit-tested for the "n" path | Cancel is a few lines in `delete_task` in the CLI | The Analyst delete path is tested; the prompt is straightforward |
| Sort from library code does not save unless asked | A caller can forget `save=True` | The menu, which is the user-facing path, saves |

## Complexity Tracking

No constitution violations and no extra projects, services, or storage engines were added.

| Violation | Why needed | Simpler alternative rejected |
| --- | --- | --- |
| None | — | — |
