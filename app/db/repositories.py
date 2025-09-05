from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Address, CreditCard, User


def upsert_user(
    db: Session, *, ext_id: int, name: str, username: str, email: str
) -> User:
    """Insert-or-update a user by external id (idempotent for periodic runs)."""
    user = db.execute(select(User).where(User.ext_id == ext_id)).scalar_one_or_none()
    if user is None:
        user = User(ext_id=ext_id, name=name, username=username, email=email)
        db.add(user)
    else:
        user.name = name
        user.username = username
        user.email = email
    db.commit()
    db.refresh(user)
    return user


def get_users_count(db: Session) -> int:
    """Return total number of users stored."""
    return db.query(User).count()


def list_users(db: Session) -> list[User]:
    """Return users ordered by local id."""
    return db.execute(select(User).order_by(User.id)).scalars().all()


def create_address_for_user(
    db: Session, *, user_id: int, street: str, city: str, country: str
) -> Address:
    """Create a new address record linked to a user."""
    addr = Address(user_id=user_id, street=street, city=city, country=country)
    db.add(addr)
    db.commit()
    db.refresh(addr)
    return addr


def create_card_for_user(db, user_id: int, number: str, type_: str):
    card = CreditCard(
        user_id=user_id,
        number=number,
        type=type_,
    )
    db.add(card)
    db.commit()
    db.refresh(card)
    return card
