"""Shared test setup."""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from todo.analyst import TaskAnalyst, TodoManager  # noqa: E402


@pytest.fixture
def Analyst(tmp_path):
    """Return an Analyst that stores tasks in a temporary file."""
    return TaskAnalyst(tmp_path / "tasks.json")


@pytest.fixture
def analyst(Analyst):
    """Alias for Analyst fixture."""
    return Analyst


@pytest.fixture
def manager(Analyst):
    """Backward compatibility fixture alias for Analyst."""
    return Analyst
