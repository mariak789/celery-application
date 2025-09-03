from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.base import get_session
from app.db.models import Address, CreditCard, User
from app.db.repositories import list_users

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.get("/users")
def users(db: Session = Depends(get_session)) -> list[dict]:
    """Shallow list of users to quickly verify ingestion."""
    rows = list_users(db)
    return [
        {
            "id": u.id,
            "ext_id": u.ext_id,
            "name": u.name,
            "username": u.username,
            "email": u.email,
        }
        for u in rows
    ]


@router.get("/users/{user_id}")
def user_details(user_id: int, db: Session = Depends(get_session)) -> dict:
    """
    Return a user with linked addresses and credit cards.
    Useful for manual verification during review.
    """
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    addresses = (
        db.execute(select(Address).where(Address.user_id == user_id)).scalars().all()
    )
    cards = (
        db.execute(select(CreditCard).where(CreditCard.user_id == user_id))
        .scalars()
        .all()
    )

    return {
        "id": user.id,
        "ext_id": user.ext_id,
        "name": user.name,
        "username": user.username,
        "email": user.email,
        "addresses": [
            {"street": a.street, "city": a.city, "country": a.country}
            for a in addresses
        ],
        "cards": [{"number": c.number, "type": c.type} for c in cards],
    }
