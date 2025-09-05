from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.base import get_session
from app.repositories.users import UserRepository


def get_user_repository(db: Session = Depends(get_session)) -> UserRepository:
    return UserRepository(db)
