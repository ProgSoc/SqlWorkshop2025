import sqlite3
from flask import g, current_app
from typing import TypeVar

T = TypeVar('T')

def get_db():
  if 'db' not in g:
    g.db = sqlite3.connect(
      current_app.config['DATABASE'],
      detect_types=sqlite3.PARSE_DECLTYPES,
      check_same_thread=False
    )
    g.db.row_factory = sqlite3.Row
  return g.db

def close_db(error=None):
  # Pop and close the connection if it exists
  db = g.pop('db', None)
  if db is not None:
    db.close()

def init_db():
  conn = get_db()
  
  with current_app.open_resource('schema.sql') as f:
    conn.executescript(f.read().decode('utf8'))
