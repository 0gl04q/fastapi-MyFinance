from uuid import UUID, uuid4
from typing import Type
from sqlalchemy.orm import Session

from apps.users import models, schemas


def get_user(db: Session, user_id: UUID) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[Type[models.User]] | None:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User | None:
    db_user = models.User(id=uuid4(), email=user.email)
    db_user.set_password(password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id, data: schemas.UserUpdate) -> None:
    db.query(models.User).filter(models.User.id == user_id).update(data.dict(exclude_unset=True))
    db.commit()

def delete_user(db: Session, user_id: UUID) -> None:
    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()
