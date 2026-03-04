from __future__ import annotations

import base64
import os
import secrets
from pathlib import Path

from dotenv import load_dotenv
from fastapi import Header, HTTPException, status
from fastapi.security import HTTPBasic


ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env", override=False)

security = HTTPBasic()


def _read_credential(name: str) -> str:
    value = os.getenv(name, "")
    if not value:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Missing required credential: {name}",
        )
    return value


def _unauthorized() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Basic"},
    )


def _decode_authorization_header(authorization: str | None) -> tuple[str, str]:
    if not authorization:
        raise _unauthorized()

    scheme, _, token = authorization.partition(" ")
    if not token or scheme.lower() != "basic":
        raise _unauthorized()

    try:
        decoded = base64.b64decode(token).decode("utf-8")
    except Exception as exc:  # pragma: no cover - defensive path
        raise _unauthorized() from exc

    username, separator, password = decoded.partition(":")
    if not separator:
        raise _unauthorized()
    return username, password


def _matches(username: str, password: str, expected_username: str, expected_password: str) -> bool:
    return secrets.compare_digest(username, expected_username) and secrets.compare_digest(
        password, expected_password
    )


def require_admin(authorization: str | None = Header(default=None)) -> str:
    admin_user = _read_credential("H2O_ADMIN_USER")
    admin_pass = _read_credential("H2O_ADMIN_PASS")
    username, password = _decode_authorization_header(authorization)

    if _matches(username, password, admin_user, admin_pass):
        return username

    raise _unauthorized()


def require_review(authorization: str | None = Header(default=None)) -> str:
    admin_user = _read_credential("H2O_ADMIN_USER")
    admin_pass = _read_credential("H2O_ADMIN_PASS")
    review_user = _read_credential("H2O_REVIEW_USER")
    review_pass = _read_credential("H2O_REVIEW_PASS")
    username, password = _decode_authorization_header(authorization)

    if _matches(username, password, admin_user, admin_pass) or _matches(
        username, password, review_user, review_pass
    ):
        return username

    raise _unauthorized()
