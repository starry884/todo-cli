from datetime import datetime

# 优先级排序权重：数字越小越靠前
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


class Task:
    def __init__(self, task_id, title, priority="medium", done=False, created_at=None):
        self.id = task_id
        self.title = title
        self.priority = priority
        self.done = done
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def priority_rank(self):
        return PRIORITY_ORDER.get(self.priority, 1)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority,
            "done": self.done,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            task_id=data["id"],
            title=data["title"],
            priority=data.get("priority", "medium"),
            done=data.get("done", False),
            created_at=data.get("created_at"),
        )

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title!r}, priority={self.priority}, done={self.done})"