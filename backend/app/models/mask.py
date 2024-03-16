from sqlalchemy import ForeignKeyConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Mask(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_name: Mapped[str] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column()
    group_code: Mapped[int] = mapped_column(ForeignKey('group.code'), nullable=False)
    points: Mapped[str] = mapped_column()

    group = relationship("Group")

    __table_args__ = (
        ForeignKeyConstraint(
            ['project_name', 'task_id'],
            ['task.project_name', 'task.id']
        ),
    )