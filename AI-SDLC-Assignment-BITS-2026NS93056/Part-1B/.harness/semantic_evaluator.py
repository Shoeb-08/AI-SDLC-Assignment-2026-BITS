import re


def _tokens(text: str) -> set[str]:
    return {word for word in re.findall(r"[a-z0-9]+", text.lower()) if len(word) > 1}


def evaluate_semantics(case: dict, response: dict) -> dict:
    intent_score = 1.0 if response.get("intent") == case["expected_intent"] else 0.0
    actual_task = (response.get("task") or "").lower()
    expected_task = (case["expected_task"] or "").lower()

    if expected_task == "clarification needed":
        task_score = 1.0 if actual_task == "clarification needed" else 0.5
    elif expected_task:
        actual_tokens = _tokens(actual_task)
        expected_tokens = _tokens(expected_task)
        overlap = len(actual_tokens & expected_tokens)
        task_score = overlap / len(expected_tokens) if expected_tokens else 0.0
    else:
        task_score = 1.0

    usefulness = 1.0
    if response.get("needs_clarification") is True:
        usefulness = 1.0 if response.get("datetime") is None else 0.0
    elif response.get("intent") == "clarification_required":
        usefulness = 0.5

    score = round((0.50 * intent_score) + (0.30 * task_score) + (0.20 * usefulness), 4)
    return {
        "score": score,
        "intent_score": intent_score,
        "task_score": round(task_score, 4),
        "usefulness_score": round(usefulness, 4),
    }
