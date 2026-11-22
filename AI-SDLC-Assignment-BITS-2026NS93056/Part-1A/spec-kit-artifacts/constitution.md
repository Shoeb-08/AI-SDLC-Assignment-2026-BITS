# Proserve Client Task Inventory Management Constitution

**Project**: Proserve Client Task Inventory Management  
**Assignment**: AI-Augmented SDLC Assignment, Part 1A  
**Version**: 1.0  
**Date**: 2026-11-22 
**Status**: Accepted

## Purpose

This constitution records the rules that govern the Proserve Client Task Inventory Management. The original brief asked for a small Python application that can create, update, delete, complete, filter, and sort tasks, and that stores those tasks in a JSON file. It also asked for pytest tests, a harness, and an evidence folder.

Every later artifact — specification, clarification, plan, and task list — follows these rules. The delivered code in `todo/`, `tests/`, and `harness/` is the implementation of this constitution.

## Scope

The product is a local, single-user command-line application. One person runs it on their own machine and keeps their tasks in one JSON file.

The product includes:

- A task model with id, title, description, priority, tags, and status
- Commands to create, update, delete, complete, list, filter, and sort tasks
- JSON persistence
- Automated unit tests
- Harness scripts for lint, security, and test execution
- Written evidence of those checks

The product does not include accounts, sharing, a network service, a graphical interface, reminders, or due dates.

## Core Principles

### 1. Stay small and readable

The implementation uses plain Python modules, clear names, and short functions. A reader should be able to follow a task from the menu, through `TaskAnalyst`, into `JsonStorage`, and back out again without a framework.

Third-party code is limited to pytest. The application itself uses the Python standard library.

### 2. Trace every feature to a requirement

Each behaviour in the brief maps to a functional requirement in `Feature.md`, a decision in `clarification.md` where the brief was open, a design note in `technical_plan.md`, and at least one pytest test. Harness evidence shows that those tests passed.

### 3. Check values before changing a task

Title, description, priority, tags, status, and task id are validated before they are stored. An update that contains an invalid value leaves the saved task unchanged. New tasks always start as `pending`.

### 4. Keep data in one local JSON file

Tasks live in a JSON object with `Client id` and `Clients`. The default file is `tasks.json`. The user may choose another file with `--file`. A missing or empty file starts an empty list. Invalid JSON is reported and is not overwritten by a silent recovery.

### 5. Prove behaviour with automated tests

Pytest is the acceptance check for application behaviour. Tests use temporary files so they do not depend on a developer’s personal `tasks.json`. A change to task rules is not complete until the related test exists and passes.

### 6. Record quality evidence

`python harness/run_all.py` runs three checks and writes reports into `evidence/`:

- Lint: syntax, tab characters, trailing spaces, and a 100-character line limit
- Security: `eval`, `exec`, `pickle`, `os.system`, `shell=True`, and hardcoded secrets
- Tests: the full pytest suite

A run is acceptable only when all three checks pass and `evidence/harness_summary.txt` records `RESULT: PASS`.

### 7. Prefer safe, local code

Application and test code does not call `eval` or `exec`, does not use `pickle`, does not start a shell, and does not embed passwords or API keys. The security script scans `todo/` and `tests/`. The harness folder is excluded from that scan because the pattern text appears there as search data.

### 8. A person accepts the result

Automated checks are necessary, and they are not the final decision. A human review reads the specification, the harness reports, and the known limits, then records Accept or Reject. For this delivery the recorded decision is **Accept**.

## Quality Gates

| Gate | Pass condition | Evidence |
| --- | --- | --- |
| Requirements | Every brief item has a functional requirement and an acceptance scenario | `Feature.md` |
| Clarifications | Open points in the brief have a recorded decision | `clarification.md` |
| Tests | Pytest exits with code 0 | `evidence/test_report.txt` |
| Lint | 17 Python files checked, 0 issues | `evidence/lint_report.txt` |
| Security | 12 application and test files scanned, 0 issues | `evidence/security_report.txt` |
| Harness | Lint, security, and tests all pass | `evidence/harness_summary.txt` |
| Review | A person accepts the build and its known limit | `evidence/harness-log.md` |

The accepted run on 2026-11-21 reported 24 passed tests, a passing lint check, a passing security check, and a final harness result of PASS.

## Design Constraints

- Language: Python 3.9 or newer. The verified environment is Python 3.12.7.
- Test tool: pytest 7 or newer. The verified run used pytest 7.4.4.
- Interface: a numbered text menu started with `python main.py` or `python -m todo`.
- Storage: one JSON file on the local disk. Writes go to a temporary file and then replace the real file.
- Identifiers: positive whole numbers. Deleted ids are not reused.
- Priority: `low`, `medium`, or `high`. The default is `medium`. Sort order is high, then medium, then low. Equal priorities are ordered by ascending task id.
- Status: `pending` or `completed`.
- Tags: zero or more text labels. Matching ignores case.
- Errors: expected failures raise `TodoError` with a short message. The menu prints that message and continues. A corrupt storage file stops startup with exit code 1.

## Known Limit

The application is for one person on one computer. The JSON file is not locked for concurrent writers, and there is no account or permission model. This limit is accepted for Part 1A and is stated in the harness log.

## Governance

- This file wins when a later note disagrees with a principle.
- A new feature that needs a network, a database, or a second user requires a constitution change before implementation.
- Clarifications may tighten the brief. They may not drop a required feature or weaken a quality gate.
- The task list is finished only when the harness passes and the human review decision is Accept.

## Amendment Record

| Version | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-11-21 | Initial constitution for the accepted Part 1A delivery. |
