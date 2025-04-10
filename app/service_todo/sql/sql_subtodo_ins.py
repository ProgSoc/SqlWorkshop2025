import app.service_sql as service_sql
from app.service_sql.sql_exec import sql_exec

from app.common.Result import Result, Ok, Err
from app.type_defs import SubTodo

class _QueryParams:
  subtodo: SubTodo

def sql_subtodo_ins(
  params: _QueryParams
) -> Result[None, str]:
  """Execute a SQL query to insert a subtodo."""
  subtodo = params['subtodo']

  conn = service_sql.get_db()

  # TODO: Write the SQL query to insert a subtodo.
  cursor_res = sql_exec(
    conn,
    """
    INSERT INTO subtodo (id, todo_id, title, desc, completed)
    VALUES (?, ?, ?, ?, ?);
    """,
    (subtodo['id'], subtodo['todo_id'], subtodo['title'], subtodo['desc'], subtodo['completed'])
  )  
  if cursor_res.is_err():
    err = cursor_res.unwrap_err()
    print(f"❌ sql_subtodo_ins: {err}")
    return Err(err)
  
  conn.commit()
  
  return Ok(None)
