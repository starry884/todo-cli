from pathlib import Path

from todo.manager import TaskManager, TaskNotFoundError
from todo.storage import TaskStorage

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "tasks.json"


def show_tasks(tasks):
    if not tasks:
        print("  （暂无任务）")
        return
    print(f"  {'ID':<4}{'状态':<8}{'优先级':<10}{'创建时间':<21}标题")
    print("  " + "-" * 62)
    for t in tasks:
        status = "✔ 完成" if t.done else "○ 待办"
        print(f"  {t.id:<4}{status:<8}{t.priority:<10}{t.created_at:<21}{t.title}")


def main():
    manager = TaskManager(TaskStorage(DATA_FILE))

    while True:
        print("\n===== 待办事项管理 =====")
        print("1. 添加任务   2. 查看任务   3. 标记完成")
        print("4. 删除任务   5. 清除已完成   0. 退出")
        choice = input("请选择：").strip()

        try:
            if choice == "1":
                title = input("任务标题：")
                priority = input("优先级 high/medium/low（默认 medium）：").strip() or "medium"
                task = manager.add(title, priority)
                print(f"已添加：[{task.id}] {task.title}（{task.priority}）")

            elif choice == "2":
                status = input("筛选 all/todo/done（默认 all）：").strip() or "all"
                keyword = input("关键字（可留空）：").strip() or None
                show_tasks(manager.list(status, keyword))

            elif choice == "3":
                task_id = int(input("要完成的 ID："))
                task = manager.complete(task_id)
                print(f"已标记完成：[{task.id}] {task.title}")

            elif choice == "4":
                task_id = int(input("要删除的 ID："))
                task = manager.delete(task_id)
                print(f"已删除：[{task.id}] {task.title}")

            elif choice == "5":
                n = manager.clear_done()
                print(f"已清除 {n} 条已完成任务")

            elif choice == "0":
                print("再见")
                break

            else:
                print("无效选项，请输入 0–5")

        except ValueError as e:
            print(f"[输入错误] {e}")
        except TaskNotFoundError as e:
            print(f"[未找到] {e}")
        except KeyboardInterrupt:
            print("\n已退出")
            break


if __name__ == "__main__":
    main()