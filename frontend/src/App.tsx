// src/App.tsx
import { useState, useCallback, useEffect } from "react";
import type { Todo } from "./types/todo";
import {
  getTodos,
  createTodo,
  toggleTodoStatus,
  toggleTodoFavorite,
  deleteTodo,
} from "./api/todo";
import TodoForm from "./components/TodoForm";
import TodoList from "./components/TodoList";

function App() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  const loadTodos = useCallback(() => {
    getTodos().then((data) => {
      setTodos(data);
    });
  }, []);

  useEffect(() => {
    loadTodos();
  }, [loadTodos]);

  const addTodo = () => {
    if (!title.trim()) return;
    createTodo(title, description).then(() => {
      setTitle("");
      setDescription("");
      loadTodos();
    });
  };

  const toggleTodo = (id: number) => {
    const todo = todos.find((t) => t.id === id);
    if (!todo) return;

    toggleTodoStatus(id, todo.completed).then(() => loadTodos());
  };

  const toggleFavorite = (id: number) => {
    const todo = todos.find((t) => t.id === id);
    if (!todo) return;

    toggleTodoFavorite(id, todo.favorite).then(() => loadTodos());
  };

  const removeTodo = (id: number) => {
    deleteTodo(id).then(() => loadTodos());
  };

  const favoriteTodos = todos.filter((t) => t.favorite);
  const otherTodos = todos.filter((t) => !t.favorite);

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-xl p-6 w-full max-w-2xl">
        <div className="flex items-center justify-between gap-2 mb-4">
          <h1 className="text-2xl font-bold text-gray-800">ToDo List</h1>
          <button
            onClick={loadTodos}
            className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg transition cursor-pointer"
          >
            Refresh Tasks
          </button>
        </div>

        <TodoForm
          title={title}
          setTitle={setTitle}
          description={description}
          setDescription={setDescription}
          addTodo={addTodo}
        />

        <section className="mb-8">
          <h2 className="text-lg font-semibold mb-2 text-gray-700">Favorites</h2>
          <TodoList
            todos={favoriteTodos}
            emptyMessage="No favorite tasks yet."
            toggleTodo={toggleTodo}
            toggleFavorite={toggleFavorite}
            removeTodo={removeTodo}
          />
        </section>

        <section>
          <h2 className="text-lg font-semibold mb-2 text-gray-700">Tasks</h2>
          <TodoList
            todos={otherTodos}
            emptyMessage="No tasks."
            toggleTodo={toggleTodo}
            toggleFavorite={toggleFavorite}
            removeTodo={removeTodo}
          />
        </section>
      </div>
    </div>
  );
}

export default App;
