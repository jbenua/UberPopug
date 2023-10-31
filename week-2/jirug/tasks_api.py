from flask import Blueprint, jsonify, request
from flask_sqlalchemy_session import current_session
from models import Tasks

tasks_api = Blueprint("tasks_api", __name__, url_prefix="/tasks")


@tasks_api.route("/", methods=["GET", "POST"])
def tasks():
    if request.method == "GET":
        # + tasks by popug
        return jsonify({"data": current_session().query(Tasks).all()})
    return jsonify({"hello": "tasks"})


@tasks_api.route("/<int:id>/done", methods=["POST"])
def task_done(id):
    return jsonify({"message": "ok"})


@tasks_api.route("/shuffle")
def shuffle_tasks():
    return jsonify({"message": "ok"})
