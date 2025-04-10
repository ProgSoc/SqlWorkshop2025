from flask import request, jsonify
from typing import TypedDict, List, Optional
from http import HTTPStatus

from app.type_defs import BaseResBody, Todo
from .sql.sql_todos_get import sql_todos_get
from . import service_todo_bp

class _QueryParams(TypedDict, total=False):
  search_query: Optional[str]
  completed: Optional[bool]

class _ReqBody(TypedDict):
  None

class _ResBody(TypedDict):
  todos: List[Todo]

@service_todo_bp.route('/api/todos', methods=['GET'])
def todos_get(
) -> BaseResBody[_ResBody]:
  """Get all todos with optional filters."""
  
  query_params: _QueryParams = request.args.to_dict()
  search_query = query_params.get('q', None)
  completed = query_params.get('completed', None)
  
  todos_res = sql_todos_get({
    'search_query': search_query,
    'completed': completed
  })
  
  if todos_res.is_err():
    err = todos_res.unwrap_err()
    return jsonify(BaseResBody[_ResBody](
      status = HTTPStatus.INTERNAL_SERVER_ERROR,
      data = None,
      error = err
    ))
    
  todos = todos_res.unwrap()
  
  return jsonify(BaseResBody[_ResBody](
    status = HTTPStatus.OK,
    data = _ResBody(
      todos = todos
    ),
    error = None
  ))

