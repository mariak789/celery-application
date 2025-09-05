from __future__ import annotations

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Address, CreditCard, User


class UserRepository:
    """Read-only data-access for API layer (decouples routes from SQL)."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def list_users(self) -> List[User]:
        return self.db.execute(select(User).order_by(User.id)).scalars().all()

    def get_user(self, user_id: int) -> Optional[User]:
        return self.db.execute(
            select(User).where(User.id == user_id)
        ).scalar_one_or_none()

    def get_addresses(self, user_id: int) -> List[Address]:
        return (
            self.db.execute(select(Address).where(Address.user_id == user_id))
            .scalars()
            .all()
        )

    def get_cards(self, user_id: int) -> List[CreditCard]:
        return (
            self.db.execute(select(CreditCard).where(CreditCard.user_id == user_id))
            .scalars()
            .all()
        )
