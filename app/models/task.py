from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from ..db import db

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str]
    is_complete: Mapped[bool] = mapped_column(default=False)
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)
    
    def to_dict(self):
        return {
            "id": getattr(self, "id", None),
            "title": getattr(self, "title", None),
            "description": getattr(self, "description", None),
            "is_complete": (self.completed_at is not None),
        }

    @classmethod
    def from_dict(cls, dict):
        task = cls()
        task.title = dict["title"]
        task.description = dict["description"]
        task.completed_at = dict.get("completed_at", None)
        task.is_complete = task.completed_at is not None
        return task