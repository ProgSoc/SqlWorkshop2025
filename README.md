# Intro to SQL Workshop

This workshop is designed for people who have little or no experience with SQL.  Python is used for the examples and exercises, but the concepts are applicable to other languages as well. SQLite3 is used as the database engine, which is a lightweight, serverless SQL database engine that is included with Python.

Activities include:

- Creating a SQLite3 database and tables
- Inserting data into tables
- Querying data from tables
- Updating data in tables
- Deleting data from tables
- Using SQL in Python Flask web app

## Prerequisites

- [Python 3.7 or later](https://www.python.org/downloads/)

> Start by using the file `workshop.ipynb` for the workshop instructions.

## Todo App

This repository includes a Python Flask web site, made for demonstration purposes only.

### Directory structure

```plain
SqlWorkshop2025/
├── README.md                           # This file
└── app
    ├── __init__.py                     # The main entry point for the Flask app
    ├── schema.sql                      # SQL schema for the database
    ├── service_todo
    │   ├── __init__.py                 # Register and combine all service_todo blueprints
    │   │   ├── sql_subtodos_get.py             # TODO
    │   │   ├── sql_subtodo_get.py              # TODO
    │   │   ├── sql_subtodo_ins.py              # TODO
    │   │   ├── sql_subtodo_upd.py              # TODO
    │   │   ├── sql_subtodo_del.py              # TODO
    │   │   └── sql_todos_get.py                # TODO
    │   │   ├── sql_todo_get.py                 # TODO
    │   │   ├── sql_todo_get_subtodo_stats.py   # TODO
    │   │   ├── sql_todo_ins.py                 # TODO
    │   │   ├── sql_todo_upd.py                 # TODO
    │   │   ├── sql_todo_del.py                 # TODO
    │   ├── subtodos_get.py          # GET      /api/todos/<todo_id>/subtodos
    │   ├── subtodo_ins.py           # POST     /api/todos/<todo_id>/subtodos
    │   ├── subtodo_get.py           # GET      /api/todos/<todo_id>/subtodos/<id>
    │   ├── subtodo_upd.py           # PUT      /api/todos/<todo_id>/subtodos/<id>
    │   ├── subtodo_del.py           # DELETE   /api/todos/<todo_id>/subtodos/<id>
    │   ├── todos_get.py             # GET      /api/todos
    │   ├── todo_ins.py              # POST     /api/todos
    │   ├── todo_get.py              # GET      /api/todos/<id>
    │   ├── todo_upd.py              # PUT      /api/todos/<id>
    │   └── todo_del.py              # DELETE   /api/todos/<id>
    ├── ...
    └── type_defs.py                # Type definitions for the application
```

### Opening the project

This project has [Dev Container support](https://code.visualstudio.com/docs/devcontainers/containers), so it will be be setup automatically if you open it in Github Codespaces or in local VS Code with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).

If you're not using one of those options for opening the project, then you'll need to:

1. Create a [Python virtual environment](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments) and activate it.

2. Install requirements:

    ```shell
    python3 -m pip install -r requirements.txt
    ```

### Local development

1. Run the server:

    ```console
    python3 -m flask run --port 5000 --debug
    ```

2. Click '<http://127.0.0.1:5000>' in the terminal, which should open the website in a new tab.
3. Try the index page, try '/hello?name=yourname', and try other paths.
