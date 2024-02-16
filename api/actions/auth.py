from typing import Union

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

import settings
from api.actions.admin import _get_admin_by_nickname
from db.session import get_db
from db.models import Admin
from hashing import Hasher

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


async def authenticate_admin(
    nickname: str, password: str, db: AsyncSession
) -> Union[Admin, None]:
    admin = await _get_admin_by_nickname(nickname=nickname, session=db)
    if admin is None:
        return
    if not Hasher.verify_password(password, admin.hashed_password):
        return
    return admin


async def get_current_admin_from_token(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        nickname: str = payload.get("sub")
        print("nickname - ", nickname)
        if nickname is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    admin = await _get_admin_by_nickname(nickname=nickname, session=db)
    if admin is None:
        raise credentials_exception
    return admin
