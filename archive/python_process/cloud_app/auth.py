from fastapi import Header, HTTPException

from .config import ADMIN_ID, ADMIN_PASSWORD


def verify_admin_credentials(
    x_admin_id: str | None = Header(default=None),
    x_admin_password: str | None = Header(default=None),
) -> str:
    if not ADMIN_ID:
        raise HTTPException(status_code=500, detail="H2O_ADMIN_ID is not configured")
    if not ADMIN_PASSWORD:
        raise HTTPException(status_code=500, detail="H2O_ADMIN_PASSWORD is not configured")
    if x_admin_id != ADMIN_ID:
        raise HTTPException(status_code=401, detail="Invalid admin id")
    if x_admin_password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid admin password")
    return ADMIN_ID


def verify_admin_credentials_from_body(admin_id: str, admin_password: str) -> None:
    if not ADMIN_ID:
        raise HTTPException(status_code=500, detail="H2O_ADMIN_ID is not configured")
    if not ADMIN_PASSWORD:
        raise HTTPException(status_code=500, detail="H2O_ADMIN_PASSWORD is not configured")
    if admin_id != ADMIN_ID:
        raise HTTPException(status_code=401, detail="Invalid admin id")
    if admin_password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid admin password")
