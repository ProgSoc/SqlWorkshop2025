from flask import Blueprint

service_todo_bp = Blueprint('service_todo_bp', __name__)

from . import todos_get, todo_get, todo_ins, todo_upd, todo_del
from . import subtodos_get, subtodo_get, subtodo_ins, subtodo_upd, subtodo_del