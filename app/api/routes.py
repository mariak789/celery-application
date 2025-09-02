from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.base import get_session

router = APIRouter()

@router.get("/health")
def health() -> dict:
    return {"status": "ok"}

@router.get("/stats")
def stats(db: Session = Depends(get_session)) -> dict:
    return {"users": 0}