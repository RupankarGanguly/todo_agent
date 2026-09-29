from langchain.tools import tool
from database import LocalSession, Todo
from datetime import datetime


@tool
def create_todo(
    title: str,
    description: str = "",
    priority: str = "medium",
    due_date: str = "",
):
    """Create and save a new todo task.
    Args:
        title: Short title for the task (required)
        description: Optional detailed note
        priority: 'low', 'medium', or 'high' (default medium)
        due_date: Optional due date e.g. '25-03-2026'
    """
    task_priority = priority.lower() if priority.lower() in ["low", "medium", "high"] else "medium"

    with LocalSession() as session:
        todo = Todo(
            title=title,
            description=description,
            priority=task_priority,
            due_date=due_date,
            created_at=datetime.now().strftime("%d-%m-%Y %H:%M"),
        )
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return f"Todo created! ID: {todo.id} | Title: {todo.title} | Priority: {todo.priority}"


@tool
def list_todos(status: str = "all", priority: str = "all"):
    """List all todos. Optionally filter by status or priority.
    Args:
        status: 'pending', 'in_progress', 'done', or 'all'
        priority: 'low', 'medium', 'high', or 'all'
    """
    with LocalSession() as session:
        query = session.query(Todo)
        if status != "all":
            query = query.filter(Todo.status == status)
        if priority != "all":
            query = query.filter(Todo.priority == priority)

        todos = query.order_by(Todo.id).all()
        if not todos:
            return "No todos found for the given filters."

        return [todo.to_dict() for todo in todos]


@tool
def update_todos(
    todo_id: int,
    title: str = "",
    description: str = "",
    status: str = "",
    priority: str = "",
    due_date: str = "",
):
    """Update an existing todo by its ID. Only provide the fields you want to change.
    Args:
        todo_id: ID of the todo to update (required)
        title: New title (leave empty to keep current)
        description: New description
        status: 'pending', 'in_progress', or 'done'
        priority: 'low', 'medium', or 'high'
        due_date: New due date e.g. '2025-12-25'
    """
    with LocalSession() as session:
        todo = session.get(Todo, todo_id)
        if not todo:
            return f"Todo with id {todo_id} not found"

        if title:
            todo.title = title
        if description:
            todo.description = description
        if status and status in ["pending", "in_progress", "done"]:
            todo.status = status
        if priority and priority in ["low", "medium", "high"]:
            todo.priority = priority
        if due_date:
            todo.due_date = due_date

        session.commit()
        session.refresh(todo)
        return f"Todo {todo.id} updated!\n{todo.to_dict()}"


@tool
def delete_todo(todo_id: int):
    """Permanently delete a todo by its ID.
    Args:
        todo_id: ID of the todo to delete (required)
    """
    with LocalSession() as session:
        todo = session.get(Todo, todo_id)
        if not todo:
            return f"Todo with id {todo_id} not found"

        title = todo.title
        session.delete(todo)
        session.commit()
        return f"Todo '{title}' (ID: {todo_id}) deleted successfully!"
