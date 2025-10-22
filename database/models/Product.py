from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ..main import Database


class Product(Database.BASE):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    category: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
