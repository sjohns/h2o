import json
from datetime import datetime, timezone
from pathlib import Path

from python_process.cloud_app.config import CURRENT_POINTER, DATA_ROOT


def ensure_data_root() -> None:
    DATA_ROOT.mkdir(parents=True, exist_ok=True)


def make_version_name(prefix: str = "v") -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    version_name = f"{prefix}{ts}"
    return version_name


def set_current_version(version: str) -> dict:
    ensure_data_root()
    payload = {
        "version": version,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    CURRENT_POINTER.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def get_current_version() -> str:
    if not CURRENT_POINTER.exists():
        message = f"Current pointer not found at {CURRENT_POINTER}."
        raise FileNotFoundError(message)

    payload = json.loads(CURRENT_POINTER.read_text(encoding="utf-8"))
    version = payload.get("version")
    if not version:
        raise ValueError("current.json is missing 'version'.")

    return version


def get_version_dir(version: str) -> Path:
    return DATA_ROOT / version
