import json

from chatroom.db.session import get_session
from chatroom.db.tables import Account

import flask
from flask import Flask, jsonify

from sqlalchemy.exc import IntegrityError
app = Flask(__name__)


client_address = "http://localhost:8080"


def create_response(data, status=200):
    allowed_methods = ["GET", "POST"]
    string_methods = ', '.join(sorted(x.upper() for x in allowed_methods))
    string_headers = ', '.join(x.upper() for x in ['Content-type'])
    headers = {
        'Access-Control-Allow-Origin': client_address,
        'Access-Control-Allow-Methods': string_methods,
        'Access-Control-Allow-Headers': string_headers,
        'Access-Control-Allow-Credentials': 'true',
        'Content-type': "application/json",
    }
    response = flask.jsonify(**data)
    response.status_code = status
    h = response.headers
    for k, v in headers.items():
        h[k] = v

    return response


def create_options_response(status=200):
    allowed_methods = ["OPTIONS"]
    string_methods = ', '.join(sorted(x.upper() for x in allowed_methods))
    string_headers = ', '.join(x.upper() for x in ['Content-type'])
    headers = {
        'Access-Control-Allow-Origin': client_address,
        'Access-Control-Allow-Methods': string_methods,
        'Access-Control-Allow-Headers': string_headers,
        'Access-Control-Allow-Credentials': 'true',
        'Content-type': "application/json",
    }
    response = flask.current_app.make_default_options_response()
    response.status_code = status
    h = response.headers
    for k, v in headers.items():
        h[k] = v

    return response


token_expiration = 10000

@app.route('/login', methods=["OPTIONS", "POST"])
def login():
    if flask.request.method == 'OPTIONS':
        print("Getting OPTIONS")
        response = create_options_response()

    elif flask.request.method == 'POST':
        print("Login Attempt")
        json_data = flask.request.json
        print("Data: {}".format(json_data))
        username = json_data.get('username')
        password = json_data.get('password')
        if username == "test@gmail.com" and password == "password":
            token = 'sample_token'
            response = create_response(data={
                "success": True,
                "token": token,
            })
            print("Login Succeeded")

        else:
            token = ''
            response = create_response(
                data={
                    "success": False,
                },
                status=403, # 403 == Forbidden
            )
            print("Login Failed")

    return response


@app.route('/friends', methods=["OPTIONS", "POST"])
def friends():
    if flask.request.method == 'OPTIONS':
        print("Getting OPTIONS")
        response = create_options_response()

    elif flask.request.method == 'POST':
        print("Loading Friend List")
        json_data = flask.request.json
        print("Data: {}".format(json_data))
        username = json_data.get('username')
        token = json_data.get('token')
        print("token: {}".format(token))

        if username == "test@gmail.com" and token == "sample_token":
            response = create_response(data={
                "success": True,
                "friends": ["colby", "furby", "topher"]
            })
            print("Returning Friends")

        else:
            response = create_response(
                data={
                    "success": False
                },
                status=400, # 400: client error
            )
            print("Auth Failed")

    return response



if __name__ == '__main__':
    app.run(debug=True)


# @app.route('/users/<command>', methods=["POST"])
# def users(command):
#     # This is how you get data from the post request body
#     json_data = flask.request.json

#     # This is how you get data from the arguments
#     args = flask.request.args

#     print("Command: {}, Args: {}, Params: {}".format(command, args, json_data))
#     if not command in {"register", "list", "remove"}:
#         raise RequestError("Invalid command: {}".format(command))

#     db_session = get_session()

#     if command == "register":
#         username = json_data.get('username')
#         if username is None:
#             raise RequestError("Username is null!")
#         try:
#             new_user = Account(
#                 username=username,
#                 description="a silly cat"
#             )
#             db_session.add(new_user)
#             db_session.commit()
#         except IntegrityError:
#             raise RequestError("Username already exists: {}".format(username))

#     elif command == "list":
#         from pprint import pprint; import pdb; pdb.set_trace()
#         raise NotImplementedError()
#     elif command == "remove":
#         username = json_data.get('username')
#         if username is None:
#             raise RequestError("Username is null!")
#         user = db_session.query(Account).filter_by(username=username).first()
#         if user is None:
#             raise RequestError("Username does not exist: {}".format(username))

#         db_session.delete(user)
#         db_session.commit()

#     return jsonify({
#         "message": "Command: {}, Success".format(command)
#     })
