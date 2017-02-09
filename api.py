from flask import Blueprint, jsonify, request
from lib.db import connect, r # rethink stuff
from passlib.hash import bcrypt
from functools import wraps
import jwt
import os

api = Blueprint("api", __name__, static_folder=None, template_folder=None)

SECRET = os.getenv("SECRET")
if SECRET == "":
    raise Exception("No secret.")

class ERRORS():
    BAD_CREDS =   ('{"error":"Bad credentials"}',    400)
    BAD_REQUEST = ('{"error":"Bad request"})',       400)
    BAD_AUTH =    ('{"error":"Bad authentication"}', 400)

def _user_jwt(userid):
    return jwt.encode({"id": userid}, SECRET).decode("utf-8")

@api.route("/login", methods=["POST"])
def login(req=None):
    if req is None: req = request.json

    # Get user from db, comparing pw
    with connect() as cn:
        user = r.table("users").get_all(req["username"].strip().lower(), index="username")[0].run(cn)
    # Validate pw
    if bcrypt.verify(req["password"], user["password"]):
        return jsonify({"jwt":_user_jwt(user["id"])})
    else:
        return ERRORS.BAD_CREDS


@api.route("/register", methods=["POST"])
def register(req=None):
    if req is None: req = request.json
    with connect() as cn:
        users = r.table("users")

        req["username"] = req["username"].lower().strip()

        # Make sure user doesn't exist already
        if users.get_all(req["username"], index="username").count().run(cn) is 0:
            # Make a new user
            inserted = users.insert({
                "username":req["username"],
                "password":bcrypt.hash(req["password"])
            }).run(cn)
            userid = inserted["generated_keys"][0]
            return jsonify({"jwt":_user_jwt(userid)})
        else:
            return jsonify({"error":"User already exists"}), 400

def authenticate(fetch_user=False):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            
            # Check if the JWT checks out
            auth_header = request.headers.get("Authorization")
            if not auth_header[0:7].lower() == "bearer ": return ERRORS.BAD_REQUEST
            jwt_str = auth_header[7:]
            
            try:
                jwt_contents = jwt.decode(jwt_str, SECRET)
            except jwt.InvalidTokenError as e:
                return ERRORS.BAD_AUTH

            if fetch_user:
                with connect() as cn:
                    kwargs[fetch_user] = r.table("users").get(jwt_contents["id"]).run(cn)
                
            return f(*args, **kwargs)
        return decorated
    return decorator

@api.route("/me")
@authenticate(fetch_user="user")
def me(user):
    return jsonify(user)

@api.route('/<path:path>')
def page_not_found(path):
    return jsonify({"error":"Not found"})
