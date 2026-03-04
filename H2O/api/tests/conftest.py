import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture(autouse=True)
def admin_auth_env(monkeypatch):
    monkeypatch.setenv("H2O_ADMIN_USER", "admin_user")
    monkeypatch.setenv("H2O_ADMIN_PASS", "admin_pass")
    monkeypatch.setenv("H2O_REVIEW_USER", "review_user")
    monkeypatch.setenv("H2O_REVIEW_PASS", "review_pass")
