import sqlite3
from app.common.Result import Result, Ok, Err

def sql_exec(
  conn: sqlite3.Connection,
  sql: str,
  params: tuple = ()
) -> Result[sqlite3.Cursor, str]:
  """Execute a SQL query and return a cursor for fetching results."""
  try:
    cursor = conn.cursor()
    cursor.execute(sql, params)

    return Ok(cursor)
  except sqlite3.Error as err:
    conn and conn.close()
    return Err(f"Database error: {str(err)}")
