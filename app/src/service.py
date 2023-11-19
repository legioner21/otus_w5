from typing import Optional

from passlib.context import CryptContext
from sqlalchemy.orm import Session

import models
import schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_user_id(db: Session, user_id: int) -> Optional[schemas.UserProfileDto]:
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not db_user:
        return None
    return schemas.UserProfileDto(
        id=db_user.id,
        user_id=db_user.user_id,
        avatar=db_user.avatar,
        age=db_user.age
    )


def update_user_by_user_id(db: Session, user_id: int, user_dto: schemas.UpdateUserDto):
    db.query(models.User). \
        filter(models.User.user_id == user_id). \
        update(
        {
            'avatar': user_dto.avatar,
            'age': user_dto.age,
        })
    db.commit()
    return get_user_by_user_id(db, user_id)


def create_user(db: Session, user_id: int, user_dto: schemas.UpdateUserDto):
    db_user = models.User(
        user_id=user_id,
        avatar=user_dto.avatar,
        age=user_dto.age
    )
    db.add(db_user)
    db.commit()
    return get_user_by_user_id(db, user_id)