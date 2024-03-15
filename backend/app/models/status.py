from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text

from app.db.base_class import Base


class Status(Base):
    name: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(Text)