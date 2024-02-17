import os
from datetime import datetime, timedelta
from typing import Any

from jose import jwt
from passlib.context import CryptContext

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = "HS256"
JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", default="secret")
JWT_REFRESH_SECRET_KEY: str = os.getenv("JWT_REFRESH_SECRET_KEY", default="secret")

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_payload(subject: Any, token_expire_minutes: int, secret_key: str) -> str:
    expires_delta = datetime.utcnow() + timedelta(minutes=token_expire_minutes)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, secret_key, ALGORITHM)
    return encoded_jwt


def create_access_token(subject: Any) -> str:
    return create_payload(subject, ACCESS_TOKEN_EXPIRE_MINUTES, JWT_SECRET_KEY)


def create_refresh_token(subject: Any) -> str:
    return create_payload(subject, REFRESH_TOKEN_EXPIRE_MINUTES, JWT_REFRESH_SECRET_KEY)
