from flask import jsonify, request
from typing import TypedDict, List, Optional
from http import HTTPStatus

from app.type_defs import BaseResBody, SubTodo
from . import service_todo_bp

from .sql.sql_subtodos_get import sql_subtodos_get

class _QueryParams(TypedDict, total=False):
  completed: Optional[bool]
  search: Optional[str]

class _ReqBody(TypedDict):
  None

class _ResBody(TypedDict):
  subtodos: List[SubTodo]

@service_todo_bp.route('/api/todos/<string:todo_id>/subtodos', methods=['GET'])
def subtodos_get(
  todo_id: str
) -> BaseResBody[_ResBody]:
  """Get all subtodos for a specific todo."""
  
  query_params: _QueryParams = request.args.to_dict()
  search_query = query_params.get('q', None)
  completed = query_params.get('completed', None)
  
  subtodos_res = sql_subtodos_get({
    'todo_id': todo_id,
    'search_query': search_query,
    'completed': completed
  })
  
  if subtodos_res.is_err():
    err = subtodos_res.unwrap_err()
    return jsonify(BaseResBody[_ResBody](
      status = HTTPStatus.INTERNAL_SERVER_ERROR,
      data = None,
      error = err
    ))
    
  subtodos = subtodos_res.unwrap()
    
  return jsonify(BaseResBody[_ResBody](
    status = HTTPStatus.OK,
    data = _ResBody(
      subtodos = subtodos
    ),
    error = None
  ))
