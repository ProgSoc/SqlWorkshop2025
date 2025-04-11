import app.service_sql as service_sql
from app.service_sql.sql_exec import sql_exec

from app.common.Result import Result, Ok, Err
from app.type_defs import SubTodo

class _QueryParams:
  subtodo: SubTodo

def sql_subtodo_upd(
  params: _QueryParams
) -> Result[None, str]:
  """Execute a SQL query to update a subtodo."""
  subtodo = params['subtodo']
  conn = service_sql.get_db()
  
  # TODO: Write the SQL query to update a subtodo by id.
  # Make sure to update the updated_at field to CURRENT_TIMESTAMP.
  # CURRENT_TIMESTAMP is a SQL function that returns the current date and time.
  cursor_res = sql_exec(
    conn,
    """
    UPDATE subtodo
    SET title = ?, desc = ?, completed = ?, due_date = ?, updated_at = CURRENT_TIMESTAMP
    WHERE id = ?;
    """,
    (subtodo['title'], subtodo['desc'], subtodo['completed'], subtodo['due_date'], subtodo['id'])
  )
  if cursor_res.is_err():
    err = cursor_res.unwrap_err()
    print(f"❌ sql_subtodo_upd: {err}")
    return Err(err)

  cursor = cursor_res.unwrap()

  if cursor.rowcount == 0:
    return Err(f"SubTodo {subtodo['id']} not found")

  conn.commit()
  
  return Ok(None)
