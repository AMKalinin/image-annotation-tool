from sqlalchemy import ForeignKey
from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column
import datetime

from app.db.base_class import Base


class Project(Base):
    name: Mapped[str] = mapped_column(primary_key=True)
    create_date: Mapped[datetime.date] = mapped_column(nullable=False)
    last_update: Mapped[datetime.date] = mapped_column(nullable=False)
    creator: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(ForeignKey('status.name'), nullable=False)
    description: Mapped[str] = mapped_column(Text)

