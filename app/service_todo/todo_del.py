from flask import jsonify, request
from typing import TypedDict
from http import HTTPStatus

from app.type_defs import BaseResBody
from .sql.sql_todo_del import sql_todo_del
from . import service_todo_bp

class _ReqBody(TypedDict):
  None

class _ResBody(TypedDict):
  None

@service_todo_bp.route('/api/todos/<string:id>', methods=['DELETE'])
def todo_del(
  id: str
) -> BaseResBody[_ResBody]:
  """Delete a todo."""
  
  del_res = sql_todo_del({
    'id': id
  })
  if del_res.is_err():
    err = del_res.unwrap_err()
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
