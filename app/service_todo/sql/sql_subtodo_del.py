import app.service_sql as service_sql
from app.service_sql.sql_exec import sql_exec

from app.common.Result import Result, Ok, Err

class _QueryParams:
  id: str

def sql_subtodo_del(
  params: _QueryParams
) -> Result[None, str]:
  """Execute a SQL query to delete a subtodo."""
  subtodo_id = params['id']
  
  conn = service_sql.get_db()

  # TODO: Write the SQL query to delete a subtodo by id.
  cursor_res = sql_exec(
    conn,
    """
    DELETE FROM subtodo
    WHERE id = ?;
    """,
    (subtodo_id, )
  )
  if cursor_res.is_err():
    err = cursor_res.unwrap_err()
    print(f"❌ sql_subtodo_del: {err}")
    return Err(err)
  cursor = cursor_res.unwrap()

  if cursor.rowcount == 0:
    return Err(f"Todo {subtodo_id} not found")

  conn.commit()
  
  return Ok(None)
