"""Run the lint check, security check, and unit tests.

Each step writes its own file in the evidence folder. This script also
writes a short summary.

Run from the Part-1A folder:

    python harness/run_all.py
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
SUMMARY = EVIDENCE / "harness_summary.txt"

STEPS = [
    ("lint", ROOT / "harness" / "lint_check.py"),
    ("security", ROOT / "harness" / "security_check.py"),
    ("tests", ROOT / "harness" / "run_tests.py"),
]


def main() -> int:
    """Run every harness script and record which ones passed."""
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    results = []
    for name, script in STEPS:
        print(f"\n===== {name} =====\n", flush=True)
        completed = subprocess.run([sys.executable, str(script)], cwd=ROOT)
        results.append((name, completed.returncode))

    failed = [name for name, code in results if code != 0]
    result = "PASS" if not failed else "FAIL"
    lines = [
        "Harness summary",
        "===============",
        f"Time: {datetime.now().isoformat(timespec='seconds')}",
        "",
    ]
    for name, code in results:
        status = "PASS" if code == 0 else "FAIL"
        lines.append(f"{name}: {status} (exit code {code})")
    lines.extend(["", f"RESULT: {result}"])
    report = "\n".join(lines) + "\n"
    SUMMARY.write_text(report, encoding="utf-8")
    print()
    print(report, end="", flush=True)
    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
