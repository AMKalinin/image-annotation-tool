from sqlalchemy import ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class Mask(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    project_name: Mapped[str] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column()
    class_code: Mapped[int] = mapped_column()
    points: Mapped[str] = mapped_column()

    __table_args__ = (
        ForeignKeyConstraint(
            ['project_name', 'task_id'],
            ['task.project_name', 'task.id']
        ),
    )