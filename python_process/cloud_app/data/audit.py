from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..config import AUDIT_LOG_PATH


def append_audit_event(event_type: str, payload: dict[str, Any]) -> None:
    event_record = {
        "event_type": event_type,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "payload": payload,
    }
    audit_log_path: Path = AUDIT_LOG_PATH
    audit_log_path.parent.mkdir(parents=True, exist_ok=True)
    with audit_log_path.open("a", encoding="utf-8") as audit_file_handle:
        audit_file_handle.write(json.dumps(event_record, ensure_ascii=True))
        audit_file_handle.write("\n")
