# Natural Language Reminder Agent

A Python starter implementation that converts reminder requests into structured JSON and evaluates the result against structural, behavioral, and semantic requirements.

## Setup

```bash
python -m pip install -r requirements.txt
```

## Run the Agent

```bash
python src/reminder_agent.py "Remind me to schedule meeting with client_xyz tomorrow at 10 AM EST"
python src/reminder_agent.py
```

Interactive mode reads a request from standard input.

## Run Tests

```bash
python -m pytest -q
python .harness/evaluation_runner.py
```

## Project Layout

- `src/reminder_agent.py`: parser and JSON CLI
- `prompts/`: prompts for optional future model integrations
- `tests/`: focused unit tests
- `evals/dataset.json`: evaluation cases
- `.harness/`: three-layer evaluation harness
- `evidence/`: generated evaluation results
