import logging
from typing import NoReturn
from fastapi import Request, status, HTTPException
from src.utils.tokeniser import decode_jwt


async def get_access_data(request: Request) -> NoReturn | dict:
    access_token_data = request.cookies.get("access_token")

    if access_token_data:
        decoded_data = decode_jwt(access_token_data)
        return decoded_data
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Access Data is Invalid"
    )

async def get_refresh_data(request: Request) -> NoReturn | dict:
    refresh_token_data = request.cookies.get("refresh_token")

    if refresh_token_data:
        decoded_data = decode_jwt(refresh_token_data)
        return decoded_data

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh Data is Invalid"
    )
