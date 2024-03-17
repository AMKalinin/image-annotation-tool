from sqlalchemy import ForeignKey
from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class Classes(Base):
    code: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    color_code: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    project_name: Mapped[str] = mapped_column( ForeignKey('project.name'), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    project = relationship("Project")