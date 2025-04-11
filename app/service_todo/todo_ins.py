from flask import jsonify, request
from typing import TypedDict
from http import HTTPStatus
from datetime import datetime

from app.type_defs import BaseResBody, Todo
from .sql.sql_todo_ins import sql_todo_ins
from . import service_todo_bp

class _ReqBody(TypedDict):
  todo: Todo

class _ResBody(TypedDict):
  None

@service_todo_bp.route('/api/todos', methods=['POST'])
def todo_ins(
) -> BaseResBody[_ResBody]:
  """Insert a new todo."""
  
  data: _ReqBody = request.get_json()
  data['todo']['due_date'] = datetime.fromisoformat(data['todo']['due_date'])
  
  ins_res = sql_todo_ins(data)
  if ins_res.is_err():
    err = ins_res.unwrap_err()
    return jsonify(BaseResBody[_ResBody](
      status = HTTPStatus.INTERNAL_SERVER_ERROR,
      data = None,
      error = err
    ))

  return jsonify(BaseResBody[_ResBody](
    status = HTTPStatus.CREATED,
    data = None,
    error = None
  ))
