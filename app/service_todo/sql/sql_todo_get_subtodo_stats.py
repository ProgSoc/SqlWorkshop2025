from typing import Optional

import app.service_sql as service_sql
from app.service_sql.sql_exec import sql_exec

from app.common.Result import Result, Ok, Err
from app.type_defs import Todo, TodoSubtodoStats

class _QueryParams:
  id: str

def sql_todo_get_subtodo_stats(
  params: _QueryParams
) -> Result[Optional[TodoSubtodoStats], str]:
  """Execute a SQL query to get the subtodo stats for a stats."""
  todo_id = params['id']
  
  conn = service_sql.get_db()
  
  # TODO: Write the SQL query to count total subtodos and completed subtodos for a stats.
  cursor_res = sql_exec(
    conn,
    """
    YOUR_SQL_QUERY_HERE
    """,
    (todo_id, )
  )
  if cursor_res.is_err():
    err = cursor_res.unwrap_err()
    print(f"❌ sql_todo_get_subtodo_stats: {err}")
    return Err(err)

  cursor = cursor_res.unwrap()
  stats = cursor.fetchone()
  
  if stats is None:
    return Ok(None)
  
  return Ok(TodoSubtodoStats(
    total = stats['total'],
    completed = stats['completed']
  ))
