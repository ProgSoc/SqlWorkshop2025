import os
from flask import Flask

import app.service_sql as service_sql

############################################
######## THIS IS THE WEB APP CODE  #########
############################################

# Create a Flask application
def create_app():
  app = Flask(__name__)
  
  # Make sure the instance folder exists
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass
  
  # Load the app configuration
  app.config.from_mapping(
    DATABASE=os.path.join(app.instance_path, 'todo.db'),
  )
  
  # Register teardown callback
  app.teardown_appcontext(service_sql.close_db)

  # Register API blueprints
  from app.service_todo import service_todo_bp
  app.register_blueprint(service_todo_bp)
  
  # Register page blueprints
  from app.pages import page_bp
  app.register_blueprint(page_bp)
  
  # Initialize the database
  with app.app_context():
    service_sql.init_db()
  
  return app

if __name__ == '__main__':
  app = create_app()
  app.run(debug=True)
