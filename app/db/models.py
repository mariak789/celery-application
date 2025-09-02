from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    ext_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)  # id from external API 
    name: Mapped[str] = mapped_column(String(120))
    username: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(120))

    addresses: Mapped[list["Address"]] = relationship(back_populates="user", cascade="all,delete-orphan")
    cards: Mapped[list["CreditCard"]] = relationship(back_populates="user", cascade="all,delete-orphan")

class Address(Base):
    __tablename__ = "addresses"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    street: Mapped[str] = mapped_column(String(160))
    city: Mapped[str] = mapped_column(String(80))
    country: Mapped[str] = mapped_column(String(80))

    user: Mapped["User"] = relationship(back_populates="addresses")

class CreditCard(Base):
    __tablename__ = "credit_cards"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    number: Mapped[str] = mapped_column(String(32))
    type: Mapped[str] = mapped_column(String(32))

    user: Mapped["User"] = relationship(back_populates="cards")