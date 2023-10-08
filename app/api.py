import time
import random

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db import SessionLocal
import crud, schemas

user_router = APIRouter()
app_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user_router.post("/", summary="Create user")
def create_user(user_dto: schemas.CreateUserDto, db: Session = Depends(get_db)):
    """
    Создание пользователя:

    - **username**: логин
    - **firstName**: имя
    - **lastName**: фамилия
    - **email**: email
    - **phone**: Телефон
    """
    time.sleep(random.randint(1, 10))
    if random.choice([True, False]):
        raise Exception("test exception")
    return crud.create_user(db, user_dto)


@user_router.get("/{userId}/", summary="ID of user")
def get_user(userId: int, db: Session = Depends(get_db)):
    """
    Информация о пользователе по id:

    - **id**: идентификатор пользователя
    """
    time.sleep(random.randint(1, 10))
    if random.choice([True, False]):
        raise Exception("test exception")
    return crud.get_user_by_id(db, userId)


@user_router.delete("/{userId}/", summary="delete user")
def delete_user(userId: int, db: Session = Depends(get_db)):
    """
    Удаление пользователя по id:

    - **id**: идентификатор пользователя
    """
    time.sleep(random.randint(1, 10))
    if random.choice([True, False]):
        raise Exception("test exception")
    return crud.delete_user_by_id(db, userId)


@user_router.put("/{userId}/", summary="update user")
def update_user(userId: int, user_dto: schemas.UpdateUserDto, db: Session = Depends(get_db)):
    """
    Обновление пользователя по id:

    - **id**: идентификатор пользователя
    - **firstName**: имя
    - **lastName**: фамилия
    - **email**: email
    - **phone**: Телефон
    """
    time.sleep(random.randint(1, 10))
    if random.choice([True, False]):
        raise Exception("test exception")
    return crud.update_user_by_id(db, userId, user_dto)


api_router = APIRouter()

api_router.include_router(user_router, prefix="/user", tags=["user"])
api_router.include_router(app_router, prefix="/app", tags=["app"])
