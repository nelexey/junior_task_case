from sqlalchemy import Float, Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from ..main import Database

class Sale(Database.BASE):
    __tablename__ = 'sales'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), index=True, nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    qty: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
