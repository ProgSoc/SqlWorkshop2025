from typing import Optional, List, TypedDict

import app.service_sql as service_sql
from app.service_sql.sql_exec import sql_exec

from app.common.Result import Result, Ok, Err
from app.type_defs import Todo

class _QueryParams(TypedDict):
  search_query: Optional[str]
  completed: Optional[bool]

def sql_todos_get(
  params: _QueryParams
) -> Result[List[Todo], str]:
  """Execute a SQL query to get a todo."""
  search_query = params['search_query']
  completed = params['completed']
  
  # TODO: Write the SQL query to fetch all todos that *contain* the search term in the 
  # title or desc. The todos that are created_at most recently should be returned first.
  # Bonus: Use the search term to filter subtodos as well.
  
  if search_query is None:
    like_param = f'YOUR_LIKE_PARAM_HERE'
  else:
    like_param = f'YOUR_LIKE_PARAM_HERE'
  
  if completed is None:
    sql_query = """
      YOUR_SQL_QUERY_HERE
      """
    params = (like_param, like_param, like_param, like_param)
  else:
    # Add the completed filter to the SQL query
    sql_query = """
      YOUR_SQL_QUERY_HERE
      """
    params = (like_param, like_param, like_param, like_param, completed)
  
  conn = service_sql.get_db()

  cursor_res = sql_exec(
    conn,
    sql_query,
    params
  )
  if cursor_res.is_err():
    err = cursor_res.unwrap_err()
    print(f"❌ sql_todos_get: {err}")
    return Err(err)

  cursor = cursor_res.unwrap()
  
  todo_rows: List[Todo] = cursor.fetchall()
  
  if len(todo_rows) == 0:
    return Ok([])
  
  todos = [
    Todo(
      id = row['id'],
      title = row['title'],
      desc = row['desc'],
      completed = bool(row['completed'])
    ) for row in todo_rows
  ]
  
  return Ok(todos)
