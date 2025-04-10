import app.service_sql as service_sql
from app.service_sql.sql_exec import sql_exec

from app.common.Result import Result, Ok, Err
from app.type_defs import Todo

class _QueryParams:
  todo: Todo

def sql_todo_ins(
  params: _QueryParams
) -> Result[None, str]:
  """Execute a SQL query to insert a todo."""
  todo = params['todo']

  conn = service_sql.get_db()

  # TODO: Write the SQL query to insert a todo.
  cursor_res = sql_exec(
    conn,
    """
    INSERT INTO todo (id, title, desc, completed)
    VALUES (?, ?, ?, ?);
    """,
    (todo['id'], todo['title'], todo['desc'], todo['completed'])
  )  
  if cursor_res.is_err():
    err = cursor_res.unwrap_err()
    print(f"❌ sql_todo_ins: {err}")
    return Err(err)
  
  conn.commit()
  
  return Ok(None)
