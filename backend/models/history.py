from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON
from db import Base
from datetime import datetime


def get_formatted_datetime():
    """Return current datetime formatted without microseconds"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class History(Base):
    __tablename__ = "history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    country: Mapped[str] = mapped_column(nullable=True)
    data: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[str] = mapped_column(default=get_formatted_datetime)

    def __str__(self):
        return (
            f"History(id={self.id}, country={self.country}, "
            + f"data={self.data}, created_at={self.created_at})"
        )
