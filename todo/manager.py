from .task import Task, PRIORITY_ORDER


class TaskNotFoundError(Exception):
    """按 ID 找不到任务时抛出。"""


class TaskManager:
    def __init__(self, storage):
        self.storage = storage
        raw = storage.load()
        self.tasks = [Task.from_dict(d) for d in raw]
        # 自增 ID：取现有最大 ID + 1
        self._next_id = max((t.id for t in self.tasks), default=0) + 1

    # ---------- 增 ----------
    def add(self, title, priority="medium"):
        title = (title or "").strip()
        if not title:
            raise ValueError("任务标题不能为空")
        priority = (priority or "medium").strip().lower()
        if priority not in PRIORITY_ORDER:
            raise ValueError("优先级只能是 high / medium / low")

        task = Task(self._next_id, title, priority)
        self._next_id += 1
        self.tasks.append(task)
        self._persist()
        return task

    # ---------- 查 ----------
    def list(self, status="all", keyword=None):
        result = self.tasks
        if status == "todo":
            result = [t for t in result if not t.done]
        elif status == "done":
            result = [t for t in result if t.done]
        elif status != "all":
            raise ValueError("筛选条件只能是 all / todo / done")

        if keyword:
            kw = keyword.lower()
            result = [t for t in result if kw in t.title.lower()]

        # 未完成在前，再按优先级，再按 ID
        return sorted(result, key=lambda t: (t.done, t.priority_rank, t.id))

    # ---------- 改 ----------
    def complete(self, task_id):
        task = self._find(task_id)
        if task.done:
            raise ValueError(f"任务 {task_id} 已经是完成状态")
        task.done = True
        self._persist()
        return task

    # ---------- 删 ----------
    def delete(self, task_id):
        task = self._find(task_id)
        self.tasks.remove(task)
        self._persist()
        return task

    def clear_done(self):
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if not t.done]
        removed = before - len(self.tasks)
        self._persist()
        return removed

    # ---------- 内部 ----------
    def _find(self, task_id):
        for t in self.tasks:
            if t.id == task_id:
                return t
        raise TaskNotFoundError(f"任务 {task_id} 不存在")

    def _persist(self):
        self.storage.save([t.to_dict() for t in self.tasks])