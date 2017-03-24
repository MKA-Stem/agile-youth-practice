#!/usr/bin/env python3
from flask import Flask, send_from_directory, request, jsonify
from werkzeug.exceptions import NotFound
from lib.db import connect, r # this is rethink
import os

app = Flask(__name__, static_folder=None)


# API blueprint
from api import api as api_blueprint
app.register_blueprint(api_blueprint, url_prefix="/api")


# Serve stuff for SPA
@app.route("/", defaults={"path":"index.html"})
@app.route("/<path:path>")
def index(path):
    result = None
    try:
        result = send_from_directory("client/dist", path)
    except NotFound as e:
        if path.endswith(".js") or path.endswith(".css") or path.endswith(".svg"):
            raise NotFound
        else:
            result = send_from_directory("client/dist", "index.html")
    return result


# Don't use this, use flask-cli
# if __name__ == "__main__":
#     PORT = os.getenv("PORT")
#     DEBUG = os.getenv("DEBUG").lower().strip() in ("true", "1", "yes") \
#             or os.getenv("FLASK_DEBUG").lower().strip() in ("true", "1", "yes")
#     app.run()
