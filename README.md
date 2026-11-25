# Technical Test: Todo App

A simple todo list manager with a FastAPI backend and a Vite + React + TypeScript frontend.
Users can add tasks with an optional description, mark them as completed, mark them as
favorite and delete them.

## Tech stack

- **Backend:** Python, FastAPI, Pydantic, Uvicorn. Data is stored in a JSON file
  (`backend/app/todos.json`).
- **Frontend:** React 19, TypeScript, Vite, Tailwind CSS 4.

## Requirements

- **Python 3.10 – 3.13.** Python 3.14 is not supported: the pinned `pydantic_core==2.33.2`
  has no prebuilt wheels for it, so `pip install` tries to build it from source (which needs
  a Rust toolchain) and usually fails.
- **Node.js 18 or newer**, with npm.

## Setup

1. Create a virtual environment and install the backend dependencies:

   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate      # Windows (PowerShell): .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. Install the frontend dependencies:

   ```bash
   cd frontend
   npm install
   ```

## Running the app

With the backend virtual environment **activated**:

```bash
cd frontend
npm run dev
```

This starts both servers at once:

- Frontend: <http://localhost:5173>
- Backend API: <http://localhost:8000> (interactive docs at <http://localhost:8000/docs>)

The backend reloads automatically when a `.py` file changes. Stop both servers with `Ctrl+C`.

Other frontend scripts: `npm run build` (type-check and production build) and
`npm run lint`.

## API

| Method   | Path               | Body                                                       | Response                                   |
| -------- | ------------------ | ---------------------------------------------------------- | ------------------------------------------ |
| `GET`    | `/todos`           | –                                                          | `200` list of todos                        |
| `POST`   | `/todos`           | `title` (required), `description`, `completed`, `favorite` | `200` the created todo                     |
| `PATCH`  | `/todos/{todo_id}` | Any of `description`, `completed`, `favorite`              | `200` the updated todo, `404` if not found |
| `DELETE` | `/todos/{todo_id}` | –                                                          | `204`, `404` if not found                  |

A todo looks like this:

```json
{
  "id": 1,
  "title": "Learn React",
  "description": "",
  "completed": true,
  "favorite": false
}
```

Invalid bodies (for example a missing `title`) return `422`.

## Project structure

```text
backend/app/
├── main.py         # Creates the FastAPI app, configures CORS and includes the router
├── router.py       # /todos endpoints
├── repository.py   # Reads and writes todos.json
├── schemas.py      # Pydantic models: Todo, TodoCreate, TodoUpdate
└── todos.json      # Data

frontend/src/
├── App.tsx         # State and handlers; splits favorites from the other tasks
├── api/todo.ts     # Calls to the backend API
├── components/     # TodoForm, TodoList, TodoItem
└── types/todo.d.ts # Todo type
```

## Design decisions

- **Server-generated ids.** The client never sends an id: `POST /todos` assigns
  `max(id) + 1`. As a consequence, if the todo with the highest id is deleted, the next new
  todo reuses that id.
- **Separate request models.** `TodoCreate` has no `id`, and `TodoUpdate` has only optional
  fields, so `PATCH` changes just the fields sent. A single `PATCH` endpoint handles
  completing, marking as favorite and editing the description.
- **Defaults for new fields.** `description` defaults to `""` and `favorite` to `false`, so
  older data without these fields still loads.
- **Repository pattern.** The backend is split into schemas, repository and router, as
  suggested in the instructions. Only `repository.py` knows the data lives in a JSON file.
- **Auto-loading.** The list loads on page load and reloads after every change. The
  original "Load Tasks" button is kept as "Refresh Tasks", to re-fetch data changed elsewhere.
- **Favorites section.** A favorite task is shown only in the "Favorites" section, not
  duplicated in the main list.
- **Dev script.** `nodemon` was replaced with Uvicorn's `--reload`: nodemon watched the
  wrong directory and only `.js`/`.json` files, so Python changes never reloaded the API.
  `concurrently -k` stops both servers if one of them exits.

## Possible improvements

- Show errors in the UI when an API call fails (it currently fails silently), plus a loading
  state.
- Backend tests with pytest and FastAPI's `TestClient`.
- A real database, such as SQLite, instead of the JSON file, which is not safe for concurrent
  writes.
- Editing a task's title and description from the UI.
