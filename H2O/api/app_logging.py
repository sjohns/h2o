from __future__ import annotations

import sys
from multiprocessing import SimpleQueue
from pathlib import Path

from loguru import logger


def setup_logging() -> None:
    logger.remove()
    logger.add(sys.stdout, level="INFO")

    logs_dir = Path(__file__).resolve().parents[1] / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    sink = str(logs_dir / "api.log")
    enqueue_supported = True
    try:
        _ = SimpleQueue()
    except PermissionError:
        enqueue_supported = False

    logger.add(
        sink,
        rotation="10 MB",
        retention="7 days",
        enqueue=enqueue_supported,
        backtrace=True,
        diagnose=False,
    )
