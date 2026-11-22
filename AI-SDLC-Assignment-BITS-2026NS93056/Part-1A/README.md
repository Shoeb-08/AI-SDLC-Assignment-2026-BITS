# Proserve Client Task Inventory Management

A small Python application for the AI-Augmented SDLC assignment. Tasks are stored in a JSON file.

## Features

- Create, update, and delete tasks
- Mark a task as completed
- Filter tasks by tag
- Sort tasks by priority (high, medium, then low)
- Save all tasks in a JSON file

Each task has an id, title, description, priority, tags, and status.

## Setup

From the `Part-1A` folder:

```text
python -m pip install -r requirements.txt
```

## Run the application

```text
python main.py
```

You can choose a different JSON file:

```text
python main.py --file my_tasks.json
```

## Run the checks

```text
python harness/run_all.py
```

This writes four files in `evidence/`:

- `lint_report.txt`
- `security_report.txt`
- `test_report.txt`
- `harness_summary.txt`

You can also run one check at a time:

```text
python harness/lint_check.py
python harness/security_check.py
python harness/run_tests.py
```

## Project layout

```text
Part-1A/
  main.py
  todo/            application source
  tests/           pytest tests
  harness/         lint, security, and test scripts
  evidence/        reports produced by the harness
```
