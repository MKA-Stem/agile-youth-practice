#!/usr/bin/env python3
from flask import Flask, send_from_directory, request, jsonify

app = Flask(__name__, static_url_path="/client/dist")


@app.route("/login", methods=["POST"])
def login():
    print(request.get_json())
    return jsonify({"login":"nope"})


@app.route("/<path:path>") # For all unresolved routes, serve from client/dist
def root(path):
    return send_from_directory(path)

if __name__ == "__main__":
    app.run()
