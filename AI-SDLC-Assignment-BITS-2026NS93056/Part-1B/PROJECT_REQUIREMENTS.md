Part 1B - Non-Deterministic AI Application
Project Title
Natural Language Reminder Agent

Objective
Build an AI-powered Reminder Agent that accepts reminder requests from a human in natural language and converts them into structured JSON.

The application must demonstrate non-deterministic AI behaviour while remaining within clearly defined specification boundaries that can be evaluated through a harness.

Example User Requests
User:

Remind me to schedule meeting with client_xyz tomorrow at 10 AM

Expected Output:

{
  "intent": "create_reminder",
  "task": "call client_xyz",
  "datetime": "2026-11-22T17:00:00",
  "needs_clarification": false
}
User:

Remind me about the meeting

Expected Output:

{
  "intent": "clarification_required",
  "task": "meeting",
  "datetime": null,
  "needs_clarification": true
}
Supported Intents
create_reminder
reschedule_reminder
snooze_reminder
clarification_required
Output Schema Contract
Every response must follow this JSON structure:

{
  "intent": "string",
  "task": "string",
  "datetime": "ISO datetime string or null",
  "needs_clarification": "boolean"
}
Structural Invariants
The following conditions must always hold:

Response must be valid JSON.
Intent must be one of:
create_reminder
reschedule_reminder
snooze_reminder
clarification_required
Task field must exist.
needs_clarification must be boolean.
datetime must either:
be a valid ISO datetime string
or null
Behavioural Properties
A reminder request should be classified as create_reminder.
A reschedule request should be classified as reschedule_reminder.
A snooze request should be classified as snooze_reminder.
Missing mandatory information must trigger clarification_required.
Invalid date expressions must trigger clarification_required.
Empty user input must trigger clarification_required.
Safety And Guardrails
The agent must not:

create reminders using invalid dates
invent missing information
infer unknown dates without clarification
return malformed JSON
The agent must request clarification whenever mandatory information is unavailable.

Evaluation Dataset Requirements
Create:

evals/dataset.json
with a minimum of 15 evaluation cases.

The dataset must include:

Normal Cases
Standard reminder requests
Boundary Cases
Future dates
Different time formats
Ambiguous Cases
Missing time
Missing date
Malformed Inputs
Empty strings
Nonsensical inputs
Adversarial / Guardrail Cases
Invalid dates
Contradictory instructions
Required Project Structure
Part-1B/
│
├── constitution.md
├── Feature.md
├── plan.md
├── tasks.md
├── README.md
│
├── src/
│   └── reminder_agent.py
│
├── prompts/
│
├── tests/
│
├── evals/
│   └── dataset.json
│
├── .harness/
│   ├── schema_validator.py
│   ├── property_validator.py
│   ├── semantic_evaluator.py
│   └── evaluation_runner.py
│
└── evidence/
Harness Requirements
The evaluation harness must contain three layers.

Layer 1 – Structural Validation
Validate:

JSON format
Required fields
Data types
Enum values
Layer 2 – Property Validation
Validate:

Correct intent classification
Clarification requirements
Date handling rules
Guardrail compliance
Layer 3 – Semantic Evaluation
Evaluate:

Task extraction quality
Intent accuracy
Overall response usefulness
Evaluation Threshold
The aggregate evaluation score must be:

80% or higher
Final outcome:

PASS if score >= 80%
FAIL if score < 80%
Deliverables To Generate
Create:

constitution.md
Feature.md
plan.md
tasks.md
README.md
src/reminder_agent.py
evals/dataset.json (minimum 15 cases)
.harness/schema_validator.py
.harness/property_validator.py
.harness/semantic_evaluator.py
.harness/evaluation_runner.py
Use Python throughout the project.

Generate starter implementations for all files.