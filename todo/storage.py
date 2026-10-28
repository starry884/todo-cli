import json
from pathlib import Path


class TaskStorage:
    def __init__(self, path):
        self.path = Path(path)

    def load(self):
        """返回 list[dict]。文件不存在返回空列表；JSON 损坏则备份后返回空列表。"""
        if not self.path.exists():
            return []

        try:
            with self.path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            backup = self.path.with_suffix(".broken.json")
            self.path.replace(backup)
            print(f"[警告] JSON 格式损坏，已备份到 {backup.name}，本次以空列表启动。")
            return []

        if not isinstance(data, list):
            raise ValueError("数据格式错误：JSON 根节点应为列表")
        return data

    def save(self, tasks):
        """先写临时文件再原子替换，避免写一半断电导致文件损坏。"""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
        tmp.replace(self.path)