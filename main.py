import json
from flask import Flask, request

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db_path = 'sqlite:////home/ubuntu/environment/todo-app-flask-sqlalchemy/todo.db'
app.config['SQLALCHEMY_DATABASE_URI'] = db_path
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    complete = db.Column(db.Boolean)


@app.route("/", methods=['GET'])
def root():
    return {"Hello": "World"}
    
@app.route("/api/v1/todos/", methods=["GET"])
def fetch_todos():
    todo_list = Todo.query.all()
    return json.dumps([
        {"id": todo.id, "title": todo.title, "complete": todo.complete}
        for todo in todo_list
    ])
    
@app.route("/api/v1/todos/<string:title>/", methods=["GET", "POST"])
def add_todo(title):
    # title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    todo = db.session.commit()
    return json.dumps({"id": todo.id, "title": todo.title, "complete": todo.complete})

@app.route("/api/v1/todos/<string:id>/", methods=["GET"])
def fetch_todo(id):
    todo = Todo.query.filter_by(id=id).first()
    return json.dumps({"id": todo.id, "title": todo.title, "complete": todo.complete})

@app.route("/api/v1/todos/<string:id>/complete/", methods=["GET"])
def complete_todo(id):
    todo = Todo.query.filter_by(id=id).first()
    todo.complete = not todo.complete
    
    db.session.commit()
    return json.dumps({"id": todo.id, "title": todo.title, "complete": todo.complete})
    
@app.route("/api/v1/todos/<string:id>/delete/", methods=["GET"])
def delete_todo(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    
    db.session.commit()
    return {"message": "Todo was deleted successfully."}

@app.route("/api/v1/todos/default/", methods=["GET"])
def add_default_todo():
    title = "New Todo"
    todo = Todo(title=title, complete=False)
    db.session.add(todo)
    db.session.commit()
    return json.dumps({"title": todo.title, "complete": todo.complete})


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=8080)
