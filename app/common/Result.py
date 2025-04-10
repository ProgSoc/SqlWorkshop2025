from typing import Callable, Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E")

class Result(Generic[T, E]):
  def map(self, func: Callable[[T], U]) -> "Result[U, E]":
    """Transforms the value if Ok; passes Err unchanged."""
    if isinstance(self, Ok):
      return Ok(func(self.value))
    return self  # type: ignore

  def bind(self, func: Callable[[T], "Result[U, E]"]) -> "Result[U, E]":
    """Chains a function that returns a Result, flattening the result."""
    if isinstance(self, Ok):
      return func(self.value)
    return self  # type: ignore
  
  def is_ok(self) -> bool:
    return isinstance(self, Ok)

  def is_err(self) -> bool:
    return isinstance(self, Err)

  def unwrap(self) -> T:
    if self.is_ok():
      return self.value
    raise Exception(f"Called unwrap() on an Err: {self.error}")

  def unwrap_err(self) -> E:
    if self.is_err():
      return self.error
    raise Exception(f"Called unwrap_err() on an Ok: {self.value}")

  def unwrap_or(self, default: T) -> T:
    return self.value if self.is_ok() else default

class Ok(Result[T, E]):
  def __init__(self, value: T):
    self.value = value

  def __repr__(self) -> str:
    return f"Ok({self.value})"

class Err(Result[T, E]):
  def __init__(self, error: E):
    self.error = error

  def __repr__(self) -> str:
    return f"Err({self.error})"
