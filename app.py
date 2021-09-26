from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import tempfile
import os.path

from werkzeug.utils import redirect

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    tempfile.gettempdir(), "todos.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    desc = db.Column(db.String(120), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno}-{self.title}"


@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        todo = Todo(title=request.form["title"], desc=request.form["desc"])
        db.session.add(todo)
        db.session.commit()

    allTodos = Todo.query.all()
    return render_template("index.html", allTodos=allTodos)


@app.route("/edit/<int:sno>", methods=["GET", "POST"])
def edit(sno):
    if request.method == "POST":
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = request.form["title"]
        todo.desc = request.form["desc"]
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("edit.html", todo=todo)


@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
