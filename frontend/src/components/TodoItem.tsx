import React from "react";
import type { Todo } from "../types/todo";

interface TodoItemProps {
  todo: Todo;
  toggleTodo: (id: number) => void;
  toggleFavorite: (id: number) => void;
  removeTodo: (id: number) => void;
}

const TodoItem: React.FC<TodoItemProps> = ({
  todo,
  toggleTodo,
  toggleFavorite,
  removeTodo,
}) => {
  return (
    <li className="flex items-center gap-2 bg-gray-50 p-3 rounded-lg border border-gray-200">
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => toggleTodo(todo.id)}
        className="cursor-pointer"
      />
      <div className="flex-1 min-w-0">
        <span className={`break-words ${todo.completed ? "line-through text-gray-400" : ""}`}>
          {todo.title}
        </span>
        {todo.description && (
          <p className="text-sm text-gray-500 break-words">{todo.description}</p>
        )}
      </div>
      <button
        type="button"
        onClick={() => toggleFavorite(todo.id)}
        title={todo.favorite ? "Remove from favorites" : "Add to favorites"}
        className="text-xl text-yellow-500 hover:text-yellow-600 px-1 transition cursor-pointer"
      >
        {todo.favorite ? "★" : "☆"}
      </button>
      <button
        type="button"
        onClick={() => removeTodo(todo.id)}
        className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 text-sm rounded-lg transition cursor-pointer"
      >
        Delete
      </button>
    </li>
  );
};

export default TodoItem;
