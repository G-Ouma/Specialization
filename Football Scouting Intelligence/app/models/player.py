from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    position: Mapped[str | None] = mapped_column(String(50), nullable=True)

    statistics: Mapped[list["PlayerStatistics"]] = relationship(back_populates="player")