from pathlib import Path

from python_process.cloud_app.data.importer import import_from_load_js_file
from python_process.cloud_app.config import DEFAULT_JS_SOURCE


def main() -> None:
    source = Path(DEFAULT_JS_SOURCE)
    result = import_from_load_js_file(source_path=str(source))
    print(result)


if __name__ == "__main__":
    main()
