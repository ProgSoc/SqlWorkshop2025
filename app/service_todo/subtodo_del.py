from flask import jsonify, request
from typing import TypedDict
from http import HTTPStatus

from app.type_defs import BaseResBody, Todo
from . import service_todo_bp

from .sql.sql_subtodo_del import sql_subtodo_del
from .sql.sql_todo_get_subtodo_stats import sql_todo_get_subtodo_stats
from .sql.sql_todo_upd import sql_todo_upd

class _ReqBody(TypedDict):
  todo: Todo

class _ResBody(TypedDict):
  None

@service_todo_bp.route('/api/todos/<string:todo_id>/subtodos/<string:id>', methods=['DELETE'])
def subtodo_del(
  todo_id: str, 
  id: str
) -> BaseResBody[_ResBody]:
  """Delete a subtodo."""
  
  data: _ReqBody = request.get_json()
  
  del_res = sql_subtodo_del({
    'id': id
  })
  if del_res.is_err():
    err = del_res.unwrap_err()
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
