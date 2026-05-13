"""JWT authentication and RBAC manager for AI backend systems."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from enum import Enum
from typing import Any

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


SECRET_KEY = "replace-with-secure-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRole(str, Enum):
    ADMIN = "admin"
    AI_ENGINEER = "ai_engineer"
    VIEWER = "viewer"


class TokenPayload(BaseModel):
    sub: str
    role: UserRole
    exp: int


class User(BaseModel):
    username: str
    role: UserRole
    disabled: bool = False


class JWTAuthManager:
    """JWT authentication and RBAC manager."""

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(
        username: str,
        role: UserRole,
        expires_delta: timedelta | None = None,
    ) -> str:
        expire = datetime.now(UTC) + (
            expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        payload = {
            "sub": username,
            "role": role.value,
            "exp": expire,
        }

        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> TokenPayload:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            return TokenPayload(
                sub=payload["sub"],
                role=payload["role"],
                exp=payload["exp"],
            )

        except JWTError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
            ) from exc

    @staticmethod
    def validate_role(
        user_role: UserRole,
        allowed_roles: list[UserRole],
    ) -> bool:
        return user_role in allowed_roles


def example_auth_flow() -> dict[str, Any]:
    """Demonstrate authentication workflow."""

    auth_manager = JWTAuthManager()

    hashed_password = auth_manager.hash_password("secure-password")

    token = auth_manager.create_access_token(
        username="ganesh",
        role=UserRole.ADMIN,
    )

    payload = auth_manager.decode_token(token)

    return {
        "hashed_password": hashed_password[:20],
        "token_created": bool(token),
        "decoded_username": payload.sub,
        "decoded_role": payload.role,
    }


if __name__ == "__main__":
    print(example_auth_flow())
