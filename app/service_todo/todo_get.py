from flask import jsonify, request
from typing import TypedDict
from http import HTTPStatus

from app.type_defs import BaseResBody, Todo
from .sql.sql_todo_get import sql_todo_get
from . import service_todo_bp

class _ReqBody(TypedDict):
  None

class _ResBody(TypedDict):
  todo: Todo

@service_todo_bp.route('/api/todos/<string:id>', methods=['GET'])
def todo_get(
  id: str
) -> BaseResBody[_ResBody]:
  """Fetch a specific todo by its ID."""

  todo_res = sql_todo_get({
    'id': id
  })
  if todo_res.is_err():
    err = todo_res.unwrap_err()
    return jsonify(BaseResBody[_ResBody](
      status = HTTPStatus.INTERNAL_SERVER_ERROR,
      data = None,
      error = err
    ))
  todo = todo_res.unwrap()

  if not todo:
    return jsonify(BaseResBody[_ResBody](
      status = HTTPStatus.NOT_FOUND,
      data = None,
      error = "Todo not found"
    ))
  
  return jsonify(BaseResBody[_ResBody](
    status = HTTPStatus.OK,
    data = _ResBody(
      todo = todo
    ),
    error = None
  ))
