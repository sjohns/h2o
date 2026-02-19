import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs):
        return False

APP_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / "python_process" / ".env")

default_data_root = PROJECT_ROOT / "python_process" / "data" / "master"
default_js_source = PROJECT_ROOT / "H2O" / "html" / "load_packing_data.js"

DATA_ROOT = Path(os.getenv("H2O_DATA_ROOT", str(default_data_root)))
CURRENT_POINTER = DATA_ROOT / "current.json"
DEFAULT_JS_SOURCE = Path(os.getenv("H2O_LOAD_JS_SOURCE", str(default_js_source)))
