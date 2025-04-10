from typing import Optional, List, TypedDict

import app.service_sql as service_sql
from app.service_sql.sql_exec import sql_exec

from app.common.Result import Result, Ok, Err
from app.type_defs import SubTodo

class _QueryParams(TypedDict):
  todo_id: str
  search_query: Optional[str]
  completed: Optional[bool]

def sql_subtodos_get(
  params: _QueryParams
) -> Result[List[SubTodo], str]:
  """Execute a SQL query to get a subtodo."""
  todo_id = params['todo_id']
  search_query = params['search_query']
  completed = params['completed']
  
  # TODO: Write the SQL query to fetch all subtodos that *contain* the search term in the 
  # title or desc. The subtodos that are created_at most recently should be returned first.
  
  if search_query is None:
    like_param = f'%'
  else:
    like_param = f'%{search_query}%'
  
  if completed is None:
    sql_query = """
      SELECT * FROM subtodo
      WHERE todo_id = ?
        AND (title LIKE ? OR desc LIKE ?)
      ORDER BY created_at DESC;
      """
    params = (todo_id, like_param, like_param)
  else:
    # Add the completed filter to the SQL query
    sql_query = """
      SELECT * FROM subtodo
      WHERE todo_id = ?
        AND (title LIKE ? OR desc LIKE ?)
        AND completed = ?
      ORDER BY created_at DESC;
      """
    params = (todo_id, like_param, like_param, completed)
  
  conn = service_sql.get_db()

  cursor_res = sql_exec(
    conn,
    sql_query,
    params
  )
  if cursor_res.is_err():
    err = cursor_res.unwrap_err()
    print(f"❌ sql_subtodos_get: {err}")
    return Err(err)

  cursor = cursor_res.unwrap()
  
  subtodo_rows: List[SubTodo] = cursor.fetchall()
  
  if len(subtodo_rows) == 0:
    return Ok([])
  
  subtodos = [
    SubTodo(
      id = row['id'],
      todo_id = row['todo_id'],
      title = row['title'],
      desc = row['desc'],
      completed = bool(row['completed'])
    ) for row in subtodo_rows
  ]
  
  return Ok(subtodos)
