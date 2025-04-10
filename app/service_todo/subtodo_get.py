from flask import jsonify
from typing import TypedDict
from http import HTTPStatus

from app.type_defs import BaseResBody, SubTodo
from .sql.sql_subtodo_get import sql_subtodo_get
from . import service_todo_bp

class _ReqBody(TypedDict):
  None

class _ResBody(TypedDict):
  subtodo: SubTodo

@service_todo_bp.route('/api/todos/<string:todo_id>/subtodos/<string:id>', methods=['GET'])
def subtodo_get(
  todo_id: str, 
  id: str
) -> BaseResBody[_ResBody]:
  """Fetch a specific subtodo by its ID."""

  subtodo_res = sql_subtodo_get({
    'id': id
  })
  if subtodo_res.is_err():
    err = subtodo_res.unwrap_err()
    return jsonify(BaseResBody[_ResBody](
      status = HTTPStatus.INTERNAL_SERVER_ERROR,
      data = None,
      error = err
    ))
  subtodo = subtodo_res.unwrap()
  
  if not subtodo:
    return jsonify(BaseResBody[_ResBody](
      status = HTTPStatus.NOT_FOUND,
      data = None,
      error = "Subtodo not found"
    ))
  
  return jsonify(BaseResBody[_ResBody](
    status = HTTPStatus.OK,
    data = _ResBody(
      subtodo = subtodo
    ),
    error = None
  ))
