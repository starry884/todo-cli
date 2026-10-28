# 命令行待办事项管理工具

一个基于 Python 标准库实现的命令行待办事项管理工具，支持任务的增删改查、优先级排序、完成状态标记，并使用 JSON 文件持久化数据。

## 功能

- 添加任务：标题 + 优先级（high / medium / low）
- 查看任务：支持全部 / 待办 / 已完成筛选，支持关键字搜索
- 标记完成：按任务 ID 标记为已完成
- 删除任务：按 ID 删除单条任务
- 清除已完成：批量删除所有已完成任务
- 数据持久化：任务保存到 JSON 文件，重启程序不丢失
- 异常处理：文件不存在、JSON 损坏、输入非法、ID 不存在均有提示

## 技术栈

- Python 3.10+
- 标准库：`json`、`pathlib`、`datetime`
- 面向对象：Task / TaskStorage / TaskManager 三层拆分

## 项目结构
todo-cli/
├── main.py # 程序入口：菜单循环与输入输出
├── todo/
│ ├── init.py
│ ├── task.py # Task 类：单个任务及序列化
│ ├── storage.py # TaskStorage：JSON 读写
│ └── manager.py # TaskManager：业务逻辑
├── data/ # 运行时自动创建，存放 tasks.json
└── README.md

## 运行方式

无需安装第三方依赖。

```bash
# 1. 克隆仓库
git clone https://github.com/starry884/todo-cli.git
cd todo-cli

# 2. 运行
python main.py
```

## 使用示例
===== 待办事项管理 =====
1. 添加任务   2. 查看任务   3. 标记完成
4. 删除任务   5. 清除已完成   0. 退出
请选择：1
任务标题：做作业
优先级 high/medium/low（默认 medium）：high
已添加：[1] 做作业（high）

请选择：2
  ID  状态    优先级    创建时间             标题
  --------------------------------------------------------------
  1   ○ 待办  high      2026-10-27 10:01:12  做作业