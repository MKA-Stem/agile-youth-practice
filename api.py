from flask import Blueprint, jsonify, request
from lib.db import connect, r # rethink stuff

api = Blueprint("api", __name__, static_folder=None, template_folder=None)

@api.route("/login", methods=["POST"])
def login():
    print(request.get_json())
    return jsonify({"login":"nope"})


@api.route('/<path:path>')
def page_not_found(path):
    return jsonify({"error":"Not found"})
