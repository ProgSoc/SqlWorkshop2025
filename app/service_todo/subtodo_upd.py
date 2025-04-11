from flask import jsonify, request
from typing import TypedDict
from http import HTTPStatus
from datetime import datetime

from app.type_defs import BaseResBody, SubTodo, Todo
from .sql.sql_subtodo_upd import sql_subtodo_upd
from .sql.sql_todo_get_subtodo_stats import sql_todo_get_subtodo_stats
from .sql.sql_todo_upd import sql_todo_upd
from . import service_todo_bp

class _ReqBody(TypedDict):
  todo: Todo
  subtodo: SubTodo

class _ResBody(TypedDict):
  None

@service_todo_bp.route('/api/todos/<string:todo_id>/subtodos/<string:id>', methods=['PUT'])
def subtodo_upd(
  todo_id: str,
  id: str
) -> BaseResBody[_ResBody]:
  """Update a subtodo."""
  
  data: _ReqBody = request.get_json()
  data['todo']['due_date'] = datetime.fromisoformat(data['todo']['due_date'])
  data['subtodo']['due_date'] = datetime.fromisoformat(data['subtodo']['due_date'])
  
  upd_res = sql_subtodo_upd({
    'subtodo': data['subtodo'],
  })
  if upd_res.is_err():
    err = upd_res.unwrap_err()
    return jsonify(BaseResBody[_ResBody](
      status = HTTPStatus.INTERNAL_SERVER_ERROR,
      data = None,
      error = err
    ))

  stats_res = sql_todo_get_subtodo_stats({
    'id': todo_id
  })
  if stats_res.is_err():
    err = stats_res.unwrap_err()
    return jsonify(BaseResBody[_ResBody](
      status = HTTPStatus.INTERNAL_SERVER_ERROR,
      data = None,
      error = err
    ))
  stats = stats_res.unwrap()

  todo = data['todo']
  # All subtodos are complete if completed count equals total.
  new_completed = True if stats['completed'] == stats['total'] else False
  
  if todo['completed'] != new_completed and stats['total'] > 0:
    todo['completed'] = new_completed
    
    todo_res = sql_todo_upd({
      'todo': todo,
    })
    if todo_res.is_err():
      err = todo_res.unwrap_err()
      return jsonify(BaseResBody[_ResBody](
        status = HTTPStatus.INTERNAL_SERVER_ERROR,
        data = None,
        error = err
      ))

  return jsonify(BaseResBody[_ResBody](
    status = HTTPStatus.NO_CONTENT,
    data = None,
    error = None
  ))
