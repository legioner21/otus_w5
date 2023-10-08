from sqlalchemy.orm import Session

import models, schemas


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user_dto: schemas.CreateUserDto):
    db_user = models.User(
        username=user_dto.username,
        firstName=user_dto.firstName,
        lastName=user_dto.lastName,
        email=user_dto.email,
        phone=user_dto.phone,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user_by_id(db: Session, user_id: int) -> bool:
    user_i = get_user_by_id(db, user_id)
    if user_i:
        db.query(models.User).filter(models.User.id == user_id).delete()
        db.commit()
        return True
    return False


def update_user_by_id(db: Session, user_id: int, user_dto: schemas.UpdateUserDto):
    db.query(models.User). \
        filter(models.User.id == user_id). \
        update(
        {
            'firstName': user_dto.firstName,
            'lastName': user_dto.lastName,
            'email': user_dto.email,
            'phone': user_dto.phone,
        })
    db.commit()
    return get_user_by_id(db, user_id)
