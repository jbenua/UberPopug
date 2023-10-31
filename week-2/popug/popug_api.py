from flask import Blueprint, jsonify, request
from flask_sqlalchemy_session import current_session
from models import Popugs

popug_api = Blueprint("popug", __name__, url_prefix="/popugs")


@popug_api.route("/", methods=["GET", "POST"])
def popugs():
    if request.method == "GET":
        return jsonify({"data": current_session().query(Popugs).all()})

    # todo: create popug
    return jsonify({"data": {"id": -1}, "message": "Created"})
