from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON
from db import Base
from datetime import datetime


class History(Base):
    __tablename__ = "history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    country: Mapped[str] = mapped_column(nullable=True)
    data: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[str] = mapped_column(default=datetime.now)

    def __str__(self):
        return (
            f"History(id={self.id}, country={self.country}, "
            + f"data={self.data}, created_at={self.created_at})"
        )
