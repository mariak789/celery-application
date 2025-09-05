from typing import List, Literal

from pydantic import BaseModel, ConfigDict, EmailStr


class HealthResponse(BaseModel):
    status: Literal["ok", "error"]
    db: Literal["available", "unavailable"] | None = None


OrmConfig = ConfigDict(from_attributes=True)


class UserListItem(BaseModel):
    model_config = OrmConfig

    id: int
    ext_id: int
    name: str
    username: str
    email: EmailStr


class AddressOut(BaseModel):
    model_config = OrmConfig

    street: str
    city: str
    country: str


class CreditCardOut(BaseModel):
    model_config = OrmConfig

    number: str
    type: str


class UserDetailsResponse(BaseModel):
    model_config = OrmConfig

    id: int
    ext_id: int
    name: str
    username: str
    email: EmailStr
    addresses: List[AddressOut]
    cards: List[CreditCardOut]
