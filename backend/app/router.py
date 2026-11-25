from fastapi import APIRouter, HTTPException

from .repository import load_todos, save_todos
from .schemas import Todo, TodoCreate, TodoUpdate

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("", response_model=list[Todo])
def get_todos() -> list[Todo]:
    """Get all todos."""
    return load_todos()


@router.post("", response_model=Todo)
def add_todo(payload: TodoCreate) -> Todo:
    """
    Add a new todo with a server-generated id.

    Args:
        payload (TodoCreate): Fields of the new todo.

    Returns:
        Todo: The created todo, including its id.
    """
    todos = load_todos()
    next_id = max((todo.id for todo in todos), default=0) + 1
    todo = Todo(
        id=next_id,
        title=payload.title,
        completed=payload.completed,
        description=payload.description,
        favorite=payload.favorite,
    )
    todos.append(todo)
    save_todos(todos)
    return todo


@router.patch("/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, changes: TodoUpdate) -> Todo:
    """
    Partially update a todo.

    Args:
        todo_id (int): Id of the todo to update.
        changes (TodoUpdate): Fields to change. Omitted or null fields are left as they are.

    Returns:
        Todo: The updated todo.

    Raises:
        HTTPException: 404 if no todo has the given id.
    """
    todos = load_todos()
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            updated = todo.model_copy(
                update=changes.model_dump(exclude_unset=True, exclude_none=True)
            )
            todos[index] = updated
            save_todos(todos)
            return updated
    raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")


@router.delete("/{todo_id}", status_code=204)
def delete_todo(todo_id: int) -> None:
    """
    Delete a todo.

    Args:
        todo_id (int): Id of the todo to delete.

    Raises:
        HTTPException: 404 if no todo has the given id.
    """
    todos = load_todos()
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            del todos[index]
            save_todos(todos)
            return
    raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")
