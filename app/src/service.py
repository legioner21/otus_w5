from typing import Optional

from passlib.context import CryptContext
from sqlalchemy.orm import Session

import models
import schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_id(db: Session, id: int) -> Optional[schemas.UserProfileDto]:
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if not db_user:
        return None
    return schemas.UserProfileDto(
        id=db_user.id,
        avatar=db_user.avatar,
        age=db_user.age
    )


def update_user_by_id(db: Session, user_id: int, user_dto: schemas.UpdateUserDto):
    db.query(models.User). \
        filter(models.User.id == user_id). \
        update(
        {
            'avatar': user_dto.avatar,
            'age': user_dto.age,
        })
    db.commit()
    return get_user_by_id(db, user_id)