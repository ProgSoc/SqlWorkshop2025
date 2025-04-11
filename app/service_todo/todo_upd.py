from flask import jsonify, request
from typing import TypedDict
from http import HTTPStatus

from app.type_defs import BaseResBody, Todo
from .sql.sql_todo_upd import sql_todo_upd
from .sql.sql_subtodos_get import sql_subtodos_get
from .sql.sql_subtodo_upd import sql_subtodo_upd
from . import service_todo_bp

class _ReqBody(TypedDict):
  todo: Todo

class _ResBody(TypedDict):
  None

@service_todo_bp.route('/api/todos/<string:id>', methods=['PUT'])
def todo_upd(
  id: str
) -> BaseResBody[_ResBody]:
  """Update a todo."""
  
  data: _ReqBody = request.get_json()
  
  upd_res = sql_todo_upd(data)
  if upd_res.is_err():
    err = upd_res.unwrap_err()
    return jsonify(BaseResBody[_ResBody](
      status = HTTPStatus.INTERNAL_SERVER_ERROR,
      data = None,
      error = err
    ))

  if data['todo']['completed'] == True:
    subtodos_res = sql_subtodos_get({
      'todo_id': id,
      'completed': None,
      'search_query': None,
    })
    if subtodos_res.is_err():
      err = subtodos_res.unwrap_err()
      return jsonify(BaseResBody[_ResBody](
        status = HTTPStatus.INTERNAL_SERVER_ERROR,
        data = None,
        error = err
      ))
    subtodos = subtodos_res.unwrap()
    
    for subtodo in subtodos:
      subtodo['completed'] = True
      subtodo_res = sql_subtodo_upd({
        'subtodo': subtodo,
      })
      if subtodo_res.is_err():
        err = subtodo_res.unwrap_err()
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
