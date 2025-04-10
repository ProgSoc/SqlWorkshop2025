from flask import jsonify, request
from typing import TypedDict
from http import HTTPStatus

from app.type_defs import BaseResBody, Todo
from .sql.sql_todo_upd import sql_todo_upd
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

  return jsonify(BaseResBody[_ResBody](
    status = HTTPStatus.NO_CONTENT,
    data = None,
    error = None
  ))
