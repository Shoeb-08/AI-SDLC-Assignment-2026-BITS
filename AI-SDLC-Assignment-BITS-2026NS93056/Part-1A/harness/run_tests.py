"""Run pytest and save the output in the evidence folder.

Run from the Part-1A folder:

    python harness/run_tests.py
"""

import importlib.util
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
REPORT = EVIDENCE / "test_report.txt"


def main() -> int:
    """Run the unit tests and write evidence/test_report.txt."""
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    if importlib.util.find_spec("pytest") is None:
        message = (
            "pytest is not installed.\n"
            "Run: python -m pip install -r requirements.txt\n"
        )
        REPORT.write_text(message, encoding="utf-8")
        print(message, end="")
        return 1

    completed = subprocess.run(
        [sys.executable, "-m", "pytest", "-v"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    output = completed.stdout + completed.stderr
    if output and not output.endswith("\n"):
        output += "\n"

    report = (
        "Test run\n"
        "========\n"
        f"Time: {datetime.now().isoformat(timespec='seconds')}\n\n"
        f"{output}\n"
        f"Exit code: {completed.returncode}\n"
    )
    REPORT.write_text(report, encoding="utf-8")
    print(output, end="" if output.endswith("\n") else "\n")
    print(f"Exit code: {completed.returncode}")
    return completed.returncode


if __name__ == "__main__":
    sys.exit(main())
