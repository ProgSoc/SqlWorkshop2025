from typing import Optional

import app.service_sql as service_sql
from app.service_sql.sql_exec import sql_exec

from app.common.Result import Result, Ok, Err
from app.type_defs import Todo

class _QueryParams:
  id: str

def sql_todo_get(
  params: _QueryParams
) -> Result[Optional[Todo], str]:
  """Execute a SQL query to get a todo."""
  todo_id = params['id']
  
  conn = service_sql.get_db()
  
  # TODO: Write the SQL query to fetch a todo by id.
  cursor_res = sql_exec(
    conn,
    """
    YOUR_SQL_QUERY_HERE
    """,
    (todo_id, )
  )
  if cursor_res.is_err():
    err = cursor_res.unwrap_err()
    print(f"❌ sql_todo_get: {err}")
    return Err(err)

  cursor = cursor_res.unwrap()
  todo: Optional[Todo] = cursor.fetchone() 
  
  if todo is None:
    return Ok(None)
  
  return Ok(Todo(
    id = todo['id'],
    title = todo['title'],
    desc = todo['desc'],
    completed = bool(todo['completed'])
  ))
