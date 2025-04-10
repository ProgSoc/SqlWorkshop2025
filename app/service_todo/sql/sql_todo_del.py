import app.service_sql as service_sql
from app.service_sql.sql_exec import sql_exec

from app.common.Result import Result, Ok, Err

class _QueryParams:
  id: str

def sql_todo_del(
  params: _QueryParams
) -> Result[None, str]:
  """Execute a SQL query to delete a todo."""
  todo_id = params['id']
  
  conn = service_sql.get_db()

  # TODO: Write the SQL query to delete a todo by id.
  cursor_res = sql_exec(
    conn,
    """
    DELETE FROM todo
    WHERE id = ?;
    """,
    (todo_id, )
  )
  if cursor_res.is_err():
    err = cursor_res.unwrap_err()
    print(f"❌ sql_todo_del: {err}")
    return Err(err)
  cursor = cursor_res.unwrap()

  if cursor.rowcount == 0:
    return Err(f"Todo {todo_id} not found")

  conn.commit()
  
  return Ok(None)
