from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_user_repository
from app.api.schemas import (
    AddressOut,
    CreditCardOut,
    HealthResponse,
    UserDetailsResponse,
    UserListItem,
)
from app.db.base import get_session
from app.repositories.users import UserRepository

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health(db: Session = Depends(get_session)) -> HealthResponse:
    try:
        db.execute(select(1))
        return HealthResponse(status="ok", db="available")
    except Exception:
        return HealthResponse(status="error", db="unavailable")


@router.get("/users", response_model=List[UserListItem])
def users(repo: UserRepository = Depends(get_user_repository)) -> List[UserListItem]:
    rows = repo.list_users()
    return [UserListItem.model_validate(u) for u in rows]


@router.get("/users/{user_id}", response_model=UserDetailsResponse)
def user_details(
    user_id: int, repo: UserRepository = Depends(get_user_repository)
) -> UserDetailsResponse:
    user = repo.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    addresses = repo.get_addresses(user_id)
    cards = repo.get_cards(user_id)

    return UserDetailsResponse(
        id=user.id,
        ext_id=user.ext_id,
        name=user.name,
        username=user.username,
        email=user.email,
        addresses=[AddressOut.model_validate(a) for a in addresses],
        cards=[CreditCardOut.model_validate(c) for c in cards],
    )
