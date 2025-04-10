from flask import Blueprint, send_from_directory

page_bp = Blueprint('page_bp', __name__)

@page_bp.route('/', methods=['GET'])
def index():
  return send_from_directory('static', 'index.html')
