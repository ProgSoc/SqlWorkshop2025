from typing import Optional

import app.service_sql as service_sql
from app.service_sql.sql_exec import sql_exec

from app.common.Result import Result, Ok, Err
from app.type_defs import SubTodo

class _QueryParams:
  id: str

def sql_subtodo_get(
  params: _QueryParams
) -> Result[Optional[SubTodo], str]:
  """Execute a SQL query to get a subtodo."""
  subtodo_id = params['id']
  
  conn = service_sql.get_db()
  
  # TODO: Write the SQL query to fetch a subtodo by id.
  cursor_res = sql_exec(
    conn,
    """
    YOUR_SQL_QUERY_HERE
    """,
    (subtodo_id, )
  )
  if cursor_res.is_err():
    err = cursor_res.unwrap_err()
    print(f"❌ sql_subtodo_get: {err}")
    return Err(err)

  cursor = cursor_res.unwrap()
  subtodo: Optional[SubTodo] = cursor.fetchone() 
  
  if subtodo is None:
    return Ok(None)
  
  return Ok(SubTodo(
    id = subtodo['id'],
    title = subtodo['title'],
    desc = subtodo['desc'],
    completed = bool(subtodo['completed'])
  ))
