import jwt
import os
from dotenv import load_dotenv


load_dotenv(".env")


jwt_secret = os.environ.get("SECRET")


def encode_jwt(data):
    return jwt.encode(data, jwt_secret, algorithm="HS256")


def decode_jwt(token):
    return jwt.decode(token, jwt_secret, algorithms="HS256", audience="fastapi-users:auth")
