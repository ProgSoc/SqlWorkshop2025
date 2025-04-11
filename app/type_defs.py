from typing import TypedDict, Optional, TypeVar, Generic
from http import HTTPStatus
from datetime import datetime

T = TypeVar('T')

class Todo(TypedDict):
  id: str
  title: str
  desc: Optional[str]
  completed: bool
  due_date: Optional[datetime]

class TodoSubtodoStats(TypedDict):
  total: int
  completed: int

class SubTodo(TypedDict):
  id: str
  todo_id: str
  title: str
  desc: Optional[str]
  completed: bool
  due_date: Optional[datetime]

# Response body types

class BaseResBody(TypedDict, Generic[T]):
  """Base response body for all API responses."""
  status: HTTPStatus
  data: Optional[T]
  error: Optional[str]
