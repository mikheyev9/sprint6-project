import jwt

from src.core.config import settings


def encode_jwt(data):
    return jwt.encode(data, settings.secret, algorithm="HS256", audience="fastapi-users:auth")


def decode_jwt(token):
    return jwt.decode(token, settings.secret, algorithms="HS256", audience="fastapi-users:auth")
