"""A small security scan for the assignment source.

The scan looks for patterns that are risky in a student project:
eval, exec, pickle, os.system, shell=True, and hardcoded secrets.
It checks the application and tests. It does not check this harness
folder, because the pattern names appear here as search text.

Run from the Part-1A folder:

    python harness/security_check.py
"""

import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
REPORT = EVIDENCE / "security_report.txt"
SCAN_DIRS = ("todo", "tests")

PATTERNS = [
    (r"\beval\s*\(", "call to eval()"),
    (r"\bexec\s*\(", "call to exec()"),
    (r"\bpickle\b", "use of pickle"),
    (r"os\.system\s*\(", "call to os.system()"),
    (r"shell\s*=\s*True", "subprocess started with shell=True"),
    (
        r"(?i)(password|api_key|secret)\s*=\s*['\"][^'\"]+['\"]",
        "possible hardcoded secret",
    ),
]


def python_files():
    """Yield Python files in the application and test folders."""
    for folder in SCAN_DIRS:
        directory = ROOT / folder
        if not directory.exists():
            continue
        for path in sorted(directory.rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            yield path


def check_file(path: Path):
    """Return issue strings for any risky pattern in the file."""
    relative = path.relative_to(ROOT)
    source = path.read_text(encoding="utf-8")
    issues = []
    for line_number, line in enumerate(source.splitlines(), start=1):
        for pattern, message in PATTERNS:
            if re.search(pattern, line):
                issues.append(f"{relative}:{line_number}: {message}")
    return issues


def main() -> int:
    """Scan the project and write evidence/security_report.txt."""
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    files = list(python_files())
    issues = []
    for path in files:
        issues.extend(check_file(path))

    result = "PASS" if not issues else "FAIL"
    lines = [
        "Security check",
        "===============",
        f"Time: {datetime.now().isoformat(timespec='seconds')}",
        f"Files scanned: {len(files)}",
        "Checks: eval, exec, pickle, os.system, shell=True, hardcoded secrets",
        f"Issues: {len(issues)}",
        "",
    ]
    if issues:
        lines.extend(issues)
        lines.append("")
    lines.append(f"RESULT: {result}")
    report = "\n".join(lines) + "\n"
    REPORT.write_text(report, encoding="utf-8")
    print(report, end="")
    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
