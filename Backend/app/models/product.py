from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Float, Text, DateTime, func, JSON
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    oldPrice: Mapped[float | None] = mapped_column(Float)
    badge: Mapped[str | None] = mapped_column(String)
    color: Mapped[str | None] = mapped_column(String)
    sizes: Mapped[list | None] = mapped_column(JSON)
    colors: Mapped[list | None] = mapped_column(JSON)
    images: Mapped[list | None] = mapped_column(JSON)
    details: Mapped[list | None] = mapped_column(JSON)
    fit: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(String, index=True)
    stock_quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())
