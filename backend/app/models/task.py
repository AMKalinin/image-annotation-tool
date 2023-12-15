from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base

class Task(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    project_name: Mapped[str] = mapped_column(ForeignKey('project.name'), primary_key=True)
    file_name: Mapped[str] = mapped_column(nullable=False)
    width: Mapped[int] = mapped_column()
    height: Mapped[int] = mapped_column()
    layers_count: Mapped[int] = mapped_column()
    status: Mapped[str] = mapped_column()

    
