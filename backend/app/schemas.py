from pydantic import BaseModel


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
