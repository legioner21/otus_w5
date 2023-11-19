from fastapi import APIRouter, Depends, Request, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Annotated

import schemas
import service
from db import get_db

user_router = APIRouter()


@user_router.get(
    "/me/",
    summary="information about me",
)
def me(
        x_userid: str | None = Header(default=None),
        db: Session = Depends(get_db),
):
    """
    Информация о пользователе:
    """
    if not x_userid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return service.get_user_by_user_id(db, x_userid)



@user_router.put(
    "/me/",
    summary="update me",
)
def update_me(
        user_dto: schemas.UpdateUserDto,
        x_userid: str | None = Header(default=None),
        db: Session = Depends(get_db),
):
    """
    Обновление пользователя:
    """
    if not x_userid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = service.get_user_by_user_id(db, x_userid)
    if not user:
        return service.create_user(db, x_userid, user_dto)
    return service.update_user_by_user_id(db, x_userid, user_dto)


api_router = APIRouter()
api_router.include_router(user_router, prefix="/user", tags=["user"])
