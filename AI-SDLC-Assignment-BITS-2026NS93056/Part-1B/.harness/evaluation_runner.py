import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from reminder_agent import ReminderAgent

sys.path.insert(0, str(ROOT / ".harness"))
from schema_validator import validate_schema
from property_validator import validate_properties
from semantic_evaluator import evaluate_semantics


def run_evaluation(reference: datetime = None) -> dict:
    reference = reference or datetime(2026, 10, 11, 12, 0)
    dataset_path = ROOT / "evals" / "dataset.json"
    with dataset_path.open("r", encoding="utf-8") as handle:
        cases = json.load(handle)

    agent = ReminderAgent()
    results = []
    structural_passes = 0
    property_passes = 0
    semantic_total = 0.0

    for case in cases:
        response = agent.process(case["input"], reference)
        schema_errors = validate_schema(response)
        property_errors = validate_properties(case, response)
        semantic = evaluate_semantics(case, response)

        if not schema_errors:
            structural_passes += 1
        if not property_errors:
            property_passes += 1
        semantic_total += semantic["score"]

        results.append({
            "id": case["id"],
            "category": case["category"],
            "input": case["input"],
            "response": response,
            "schema_errors": schema_errors,
            "property_errors": property_errors,
            "semantic": semantic,
        })

    count = len(cases)
    structural_score = structural_passes / count if count else 0.0
    property_score = property_passes / count if count else 0.0
    semantic_score = semantic_total / count if count else 0.0
    aggregate_score = (0.30 * structural_score) + (0.40 * property_score) + (0.30 * semantic_score)
    aggregate_percent = round(aggregate_score * 100, 2)

    report = {
        "reference_datetime": reference.isoformat(),
        "case_count": count,
        "structural_score": round(structural_score * 100, 2),
        "property_score": round(property_score * 100, 2),
        "semantic_score": round(semantic_score * 100, 2),
        "aggregate_score": aggregate_percent,
        "result": "PASS" if aggregate_percent >= 80.0 else "FAIL",
        "results": results,
    }
    return report


def main() -> None:
    report = run_evaluation()
    evidence_dir = ROOT / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    evidence_path = evidence_dir / "evaluation_report.json"
    evidence_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "results"}, indent=2))


if __name__ == "__main__":
    main()
