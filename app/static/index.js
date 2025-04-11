// @ts-nocheck
// Render the list of subtodos for a given todo
async function renderSubtodos(todoId, subtodoListEl) {
  try {
    const response = await fetch(`/api/todos/${todoId}/subtodos`);
    const result = await response.json();
    if (!response.ok) {
      throw new Error(result.message || 'Failed to fetch subtodos');
    }
    const subtodos = result.data.subtodos || [];
    subtodoListEl.innerHTML = '';
    subtodos.forEach(subtodo => {
      const subLi = document.createElement('li');
      subLi.dataset.subtodoId = subtodo.id;
      subLi.innerHTML = `
        <div class="subtodo-item" style="display: flex; gap: 4px; padding: 5px 0 10px 0;">
          <input type="text" class="edit-subtodo-title" value="${subtodo.title}">
          <input type="text" class="edit-subtodo-desc" value="${subtodo.desc || ''}">
          <label>
            Completed?
            <input type="checkbox" class="edit-subtodo-completed" ${subtodo.completed ? 'checked' : ''}>
          </label>
          <!-- TODO: Add edit subtodo due date input below -->
          <button class="update-subtodo-btn">Update Subtodo</button>
          <button class="delete-subtodo-btn">Delete Subtodo</button>
        </div>
      `;
      subtodoListEl.appendChild(subLi);
    });
  } catch (error) {
    console.error('Error fetching subtodos:', error);
  }
}

// Render the list of todos and for each todo attach its subtodos UI
async function renderTodos() {
  // Get the filter status (for completed)
  const status = document.getElementById('filter').value;
  let completedParam = null;
  if (status === 'completed') {
    completedParam = true;
  } else if (status === 'pending') {
    completedParam = false;
  }
  
  // Get the search query value from the search input (using the actual value, not templates)
  const searchQuery = document.getElementById('search').value;
  
  // Build URL query parameters
  const params = new URLSearchParams();
  if (searchQuery) {
    params.append('q', searchQuery);
  }
  if (completedParam) {
    params.append('completed', completedParam);
  }

  let url = '/api/todos';
  if (params.toString()) {
    url += `?${params.toString()}`;
  }

  try {
    const response = await fetch(url);
    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.message || 'Failed to fetch todos');
    }
    const todos = result.data.todos || [];
    const list = document.getElementById('todo-list');
    list.innerHTML = '';

    todos.forEach(todo => {
      const li = document.createElement('li');
      li.dataset.id = todo.id;
      li.innerHTML = `
        <div class="todo-item" style="display: flex; gap: 4px; padding: 10px 0 5px 0; width: 100%;">
          <input type="text" class="edit-title" value="${todo.title}">
          <input type="text" class="edit-desc" value="${todo.desc || ''}">
          <label>
            Completed?
            <input type="checkbox" class="edit-completed" ${todo.completed ? 'checked' : ''}>
          </label>
          <!-- TODO: Add edit todo due date input below -->
          <button class="update-btn">Update</button>
          <button class="delete-btn">Delete</button>
        </div>
        <div class="subtodos" style="display: flex; flex-direction: column; gap: 10px;">
          <ul class="subtodo-list"></ul>
          <form class="add-subtodo-form" style="display: flex; gap: 4px; margin-left: 24px;">
            <span style="font-weight: bold; padding-right: 2px">Add a new Subtodo:</span>
            <input type="text" class="new-subtodo-title" placeholder="Subtodo Title" required>
            <input type="text" class="new-subtodo-desc" placeholder="Subtodo Description">
            <label>
              Completed?
              <input type="checkbox" class="new-subtodo-completed">
            </label>
            <!-- TODO: Add new subtodo due date input below -->
            <button type="submit">Add Subtodo</button>
          </form>
          <hr style="margin: 10px 0; border: 0.5px solid #ccc; width: 100%;">
        </div>
      `;
      list.appendChild(li);
      const subtodoListEl = li.querySelector('.subtodo-list');
      renderSubtodos(todo.id, subtodoListEl);
    });
  } catch (error) {
    console.error('Error fetching todos:', error);
  }
}

function formatDateToDatetimeLocal(date) {
  return date.toISOString().replace('T', ' ').substring(0, 19);
}

function formatDateToSQLite(date) {
  const pad = n => n < 10 ? '0' + n : n;
  const year  = date.getFullYear();
  const month = pad(date.getMonth() + 1);  // Months are 0-indexed
  const day   = pad(date.getDate());
  const hours = pad(date.getHours());
  const minutes = pad(date.getMinutes());
  const seconds = pad(date.getSeconds());
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

// Handle search todos (GET /api/todos)
document.getElementById('search-todos').addEventListener('submit', async (e) => {
  e.preventDefault();
  renderTodos();
});

// Handle add todo form (POST /api/todos)
document.getElementById('add-todo-form').addEventListener('submit', async (e) => {
  e.preventDefault();

  // TODO: Add new todo due date field below

  const reqBody = {
    todo: {
      id: crypto.randomUUID(),
      title: document.getElementById('new-todo-title').value,
      desc: document.getElementById('new-todo-desc').value,
      completed: document.getElementById('new-todo-completed').checked,
      // TODO: Add the todo due date to the request body
    }
  };

  try {
    const response = await fetch('/api/todos', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(reqBody)
    });
    if (response.ok) {
      document.getElementById('new-todo-title').value = '';
      document.getElementById('new-todo-desc').value = '';
      document.getElementById('new-todo-completed').checked = false;
      // TODO: Reset the new todo due date field
      renderTodos();
    }
  } catch (error) {
    console.error('Error adding todo:', error);
  }
});

// Delegate click events for todo and subtodo updates/deletes
document.getElementById('todo-list').addEventListener('click', async (e) => {
  // The closest outer todo <li>
  const todoLI = e.target.closest('li[data-id]');
  if (!todoLI) return;
  const todoId = todoLI.dataset.id;

  // TODO: Add edit todo due date field below

  // Todo update
  if (e.target.classList.contains('update-btn')) {
    const reqBody = {
      todo: {
        id: todoId,
        title: todoLI.querySelector('.edit-title').value,
        desc: todoLI.querySelector('.edit-desc').value,
        completed: todoLI.querySelector('.edit-completed').checked,
        // TODO: Add the todo due date to the request body
      }
    };
    try {
      const response = await fetch(`/api/todos/${todoId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(reqBody)
      });
      if (response.ok) renderTodos();
    } catch (error) {
      console.error('Error updating todo:', error);
    }
  }
  // Todo delete
  else if (e.target.classList.contains('delete-btn')) {
    try {
      const response = await fetch(`/api/todos/${todoId}`, { method: 'DELETE' });
      if (response.ok) renderTodos();
    } catch (error) {
      console.error('Error deleting todo:', error);
    }
  }
  // Subtodo update
  else if (e.target.classList.contains('update-subtodo-btn')) {
    const subtodoLI = e.target.closest('li');
    const subtodoId = subtodoLI.dataset.subtodoId;

    // TODO: Add edit subtodo due date field below

    const reqBody = {
      todo: {
        id: todoId,
        title: todoLI.querySelector('.edit-title').value,
        desc: todoLI.querySelector('.edit-desc').value,
        completed: todoLI.querySelector('.edit-completed').checked,
        // TODO: Add the todo due date to the request body
      },
      subtodo: {
        id: subtodoId,
        todo_id: todoId,
        title: subtodoLI.querySelector('.edit-subtodo-title').value,
        desc: subtodoLI.querySelector('.edit-subtodo-desc').value,
        completed: subtodoLI.querySelector('.edit-subtodo-completed').checked,
        // TODO: Add the subtodo due date to the request body
      }
    };
    try {
      const response = await fetch(`/api/todos/${todoId}/subtodos/${subtodoId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(reqBody)
      });
      if (response.ok) {
        const subtodoListEl = todoLI.querySelector('.subtodo-list');
        renderTodos();
      }
    } catch (error) {
      console.error('Error updating subtodo:', error);
    }
  }
  // Subtodo delete
  else if (e.target.classList.contains('delete-subtodo-btn')) {
    const subtodoLI = e.target.closest('li');
    const subtodoId = subtodoLI.dataset.subtodoId;

    const reqBody = {
      todo: {
        id: todoId,
        title: todoLI.querySelector('.edit-title').value,
        desc: todoLI.querySelector('.edit-desc').value,
        completed: todoLI.querySelector('.edit-completed').checked,
        // TODO: Add the todo due date to the request body
      }
    }
    try {
      const response = await fetch(`/api/todos/${todoId}/subtodos/${subtodoId}`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(reqBody)
      });
      if (response.ok) {
        const subtodoListEl = todoLI.querySelector('.subtodo-list');
        renderTodos();
      }
    } catch (error) {
      console.error('Error deleting subtodo:', error);
    }
  }
});

// Delegate form submission for adding a subtodo
document.getElementById('todo-list').addEventListener('submit', async (e) => {
  if (!e.target.classList.contains('add-subtodo-form')) return;
  e.preventDefault();
  const form = e.target;
  const todoLI = form.closest('li[data-id]');
  const todoId = todoLI.dataset.id;

  // TODO: Add new todo and subtodo due date field below

  const reqBody = {
    todo: {
      id: todoId,
      title: todoLI.querySelector('.edit-title').value,
      desc: todoLI.querySelector('.edit-desc').value,
      completed: todoLI.querySelector('.edit-completed').checked,
      // TODO: Add the todo due date to the request body
    },
    subtodo: {
      id: crypto.randomUUID(),
      todo_id: todoId,
      title: form.querySelector('.new-subtodo-title').value,
      desc: form.querySelector('.new-subtodo-desc').value,
      completed: form.querySelector('.new-subtodo-completed').checked,
      // TODO: Add the subtodo due date to the request body
    }
  };

  try {
    const response = await fetch(`/api/todos/${todoId}/subtodos`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(reqBody)
    });
    if (response.ok) {
      form.reset();
      const subtodoListEl = todoLI.querySelector('.subtodo-list');
      renderTodos();
    }
  } catch (error) {
    console.error('Error adding subtodo:', error);
  }
});

// Initial load of todos
renderTodos();
