from __future__ import annotations

import os

from fastapi.testclient import TestClient
from rich.console import Console
from rich.table import Table

from ..main import app


def main() -> None:
    admin_id = os.getenv("H2O_ADMIN_ID", "")
    admin_password = os.getenv("H2O_ADMIN_PASSWORD", "")

    client = TestClient(app)

    checks: list[tuple[str, int, int]] = []
    checks.append(("GET /health", client.get("/health").status_code, 200))
    checks.append(("GET /client-ui", client.get("/client-ui").status_code, 200))
    checks.append(("GET /api/skus", client.get("/api/skus").status_code, 200))

    if admin_id and admin_password:
        admin_headers = {"x-admin-id": admin_id, "x-admin-password": admin_password}
        checks.append(("GET /admin/dataset", client.get("/admin/dataset", headers=admin_headers).status_code, 200))
        checks.append(("GET /admin/storage/status", client.get("/admin/storage/status", headers=admin_headers).status_code, 200))
    else:
        checks.append(("GET /admin/dataset (without creds)", client.get("/admin/dataset").status_code, 401))

    table = Table(title="Predeploy Smoke Checks")
    table.add_column("Check")
    table.add_column("Status")
    table.add_column("Expected")
    table.add_column("Pass")

    all_passed = True
    for check_name, status_code, expected_code in checks:
        passed = status_code == expected_code
        if not passed:
            all_passed = False
        table.add_row(check_name, str(status_code), str(expected_code), "yes" if passed else "no")

    console = Console()
    console.print(table)
    if not all_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
