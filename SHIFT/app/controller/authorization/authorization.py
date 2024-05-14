import datetime

from fastapi import HTTPException
from jose import jwt, JWTError

from SHIFT.app.model import DatabaseUserGateway, DecodeToken
from SHIFT.config import config


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=config.EXPIRE_MINUTES)
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


async def check_token(database: DatabaseUserGateway, token: str) -> DecodeToken:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        id_, username = payload.get("id_"), payload.get("username")
        if id_ is None or username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await database.get_user_by_id_and_email(id_, username)
    if user is None:
        raise credentials_exception
    return DecodeToken(id=id_, username=username)

