import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

DATA_FILE = Path(__file__).parent / "todos.json"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Todo(BaseModel):
    """A stored todo, as returned by the API."""

    id: int
    title: str
    completed: bool = False


class TodoCreate(BaseModel):
    """Payload to create a todo. The id is assigned by the server."""

    title: str
    completed: bool = False


class TodoUpdate(BaseModel):
    """Partial update payload. Only the fields sent by the client are applied."""

    completed: bool | None = None


def load_todos() -> list[Todo]:
    """Load todos from the JSON file."""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return [Todo(**todo) for todo in json.load(f)]


def save_todos(todos: list[Todo]) -> None:
    """
    Save todos to the JSON file.

    Args:
        todos (list[Todo]): List of Todo objects to save.
    """
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([todo.model_dump() for todo in todos], f, indent=2)


@app.get("/todos", response_model=list[Todo])
def get_todos() -> list[Todo]:
    """Get all todos."""
    return load_todos()


@app.post("/todos", response_model=Todo)
def add_todo(payload: TodoCreate) -> Todo:
    """
    Add a new todo with a server-generated id.

    Args:
        payload (TodoCreate): Title and completion status of the new todo.

    Returns:
        Todo: The created todo, including its id.
    """
    todos = load_todos()
    next_id = max((todo.id for todo in todos), default=0) + 1
    todo = Todo(id=next_id, title=payload.title, completed=payload.completed)
    todos.append(todo)
    save_todos(todos)
    return todo


@app.patch("/todos/{todo_id}", response_model=Todo)
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


@app.delete("/todos/{todo_id}", status_code=204)
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
