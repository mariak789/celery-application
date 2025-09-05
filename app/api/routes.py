from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.schemas import (
    AddressOut,
    CreditCardOut,
    HealthResponse,
    UserDetailsResponse,
    UserListItem,
)
from app.db.base import get_session
from app.db.models import Address, CreditCard, User
from app.db.repositories import list_users

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health(db: Session = Depends(get_session)) -> HealthResponse:
    try:
        db.execute(select(1))
        return HealthResponse(status="ok", db="available")
    except Exception:
        return HealthResponse(status="error", db="unavailable")


@router.get("/users", response_model=List[UserListItem])
def users(db: Session = Depends(get_session)) -> List[UserListItem]:
    """Shallow list of users to quickly verify ingestion."""
    rows = list_users(db)
    return [
        UserListItem(
            id=u.id,
            ext_id=u.ext_id,
            name=u.name,
            username=u.username,
            email=u.email,
        )
        for u in rows
    ]


@router.get("/users/{user_id}", response_model=UserDetailsResponse)
def user_details(
    user_id: int, db: Session = Depends(get_session)
) -> UserDetailsResponse:
    """Return a user with linked addresses and credit cards."""
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

    return UserDetailsResponse(
        id=user.id,
        ext_id=user.ext_id,
        name=user.name,
        username=user.username,
        email=user.email,
        addresses=[AddressOut.model_validate(a) for a in addresses],
        cards=[CreditCardOut.model_validate(c) for c in cards],
    )
