from sqlalchemy.orm import Mapped, mapped_column
from db import BaseClass


class History(BaseClass):
    __tablename__ = "history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    country: Mapped[str] = mapped_column()
    data: Mapped[str] = mapped_column()
