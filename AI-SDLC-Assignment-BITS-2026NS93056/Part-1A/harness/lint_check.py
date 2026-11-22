"""Simple style and syntax check for the assignment source.

This script does not need an extra lint package. It compiles every Python
file and reports long lines, tabs, and trailing spaces.

Run from the Part-1A folder:

    python harness/lint_check.py
"""

import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
REPORT = EVIDENCE / "lint_report.txt"
MAX_LINE_LENGTH = 100
SKIP_DIRS = {"__pycache__", ".pytest_cache", "evidence", ".venv", "venv", ".git"}


def python_files():
    """Yield project Python files, skipping generated folders."""
    for path in sorted(ROOT.rglob("*.py")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def check_file(path: Path):
    """Return a list of issue strings for one file."""
    relative = path.relative_to(ROOT)
    try:
        source = path.read_text(encoding="utf-8")
    except UnicodeError:
        return [f"{relative}: file is not valid UTF-8 text"]

    issues = []
    try:
        compile(source, str(relative), "exec")
    except SyntaxError as exc:
        issues.append(f"{relative}:{exc.lineno}: syntax error: {exc.msg}")
        return issues

    for number, line in enumerate(source.splitlines(), start=1):
        if "\t" in line:
            issues.append(f"{relative}:{number}: tab character found")
        if line.rstrip("\r\n") != line.rstrip():
            issues.append(f"{relative}:{number}: trailing whitespace")
        if len(line) > MAX_LINE_LENGTH:
            issues.append(
                f"{relative}:{number}: line is longer than {MAX_LINE_LENGTH} characters"
            )
    return issues


def main() -> int:
    """Check the project and write evidence/lint_report.txt."""
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    files = list(python_files())
    issues = []
    for path in files:
        issues.extend(check_file(path))

    result = "PASS" if not issues else "FAIL"
    lines = [
        "Lint check",
        "==========",
        f"Time: {datetime.now().isoformat(timespec='seconds')}",
        f"Files checked: {len(files)}",
        f"Line length limit: {MAX_LINE_LENGTH}",
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
