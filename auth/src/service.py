from passlib.context import CryptContext
from sqlalchemy.orm import Session

import models
import schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def register_user(db: Session, register_dto: schemas.RegisterUserDto) -> schemas.UserDto:
    db_user = models.User(
        username=register_dto.username,
        first_name=register_dto.first_name,
        last_name=register_dto.last_name,
        email=register_dto.email,
        hashed_password=pwd_context.hash(register_dto.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return schemas.UserDto(
        id=db_user.id,
        username=db_user.username,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        email=db_user.email
    )


def verify_user(db: Session, login_dto: schemas.LoginDto) -> schemas.UserDto:
    db_user = get_user_by_username(db, login_dto.username)
    if not db_user:
        raise Exception("not user")

    if not pwd_context.verify(login_dto.password, db_user.hashed_password):
        raise Exception("wrong passwd")

    return schemas.UserDto(
        id=db_user.id,
        username=db_user.username,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        email=db_user.email
    )


def get_user_by_username(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()
