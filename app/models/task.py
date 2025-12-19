from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)
    goal_id: Mapped[int | None] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Goal | None] = relationship(back_populates="tasks")
    
    def to_dict(self):
        task_as_dict = {
            "id": getattr(self, "id", None),
            "title": getattr(self, "title", None),
            "description": getattr(self, "description", None),
            "is_complete": (self.completed_at is not None)
        }
        if self.goal:
            task_as_dict["goal_id"] = self.goal_id
        return task_as_dict

    @classmethod
    def from_dict(cls, dict):
        return cls(
            title=dict["title"],
            description=dict["description"],
            goal_id=dict.get("goal_id")
        )