import json

import flask
from flask import Flask, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from zxcvbn import zxcvbn

from chatroom.db.session import get_session
from chatroom.db.tables import Account
from chatroom.db.tables import Token

import secrets
from datetime import datetime
from datetime import timedelta
import base64

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

@app.route('/login', methods=["OPTIONS", "POST"])
def login():
    if flask.request.method == 'OPTIONS':
        print("Getting OPTIONS")
        response = create_options_response()

    elif flask.request.method == 'POST':
        print("Login Attempt")
        json_data = flask.request.json
        print("Data: {}".format(json_data))
        useremail = json_data.get('email')
        password = json_data.get('password')

        db_session = get_session()
        error_messages = []
        found_email = db_session.query(Account).filter_by(email=useremail).first()

        if found_email:
            password_hash = db_session.query(Account).filter_by(email=useremail).first().password_hash
            flag = check_password_hash(password_hash, password)
            user_id = db_session.query(Account).filter_by(email=useremail).first().id

            if flag:
                create_time = datetime.utcnow()
                token = secrets.token_bytes()
                str_token = base64.b64encode(token).decode('utf-8')

                new_token = Token(
                    user_id=user_id,
                    create_time=create_time,
                    token=str_token,
                    expire_time=create_time + timedelta(hours=24)
                )

                db_session.add(new_token)
                db_session.commit()

                response = create_response(
                    data={ "success": True, "token": str_token},
                    status=200
                )
                print("Login Succeeded")

            else:
                db_session.rollback()
                token = ''
                error_messages.append("Password is Wrong")
                response = create_response(
                    data={
                        "success": False,
                        "message": "Login failed: " + ", ".join(error_messages)
                    }, status=403)  # 403 == Forbidden)
                print("Password Failed")

        else:
            error_messages.append("User Email Not Found")
            response = create_response(
                    data={
                        "success": False,
                        "message": "Login failed: " + ", ".join(error_messages)
                    }, status=403)  # 403 == Forbidden)
            print("Email not Found")

        db_session.close()

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

    else:
        response = create_response(
            data={
                "success": False
            },
            status=400,  # 400: client error
        )
        print("Auth Failed")

    return response


@app.route('/check_username', methods=["OPTIONS", "POST"])
def check_username():
    if flask.request.method == 'OPTIONS':
        print("Getting OPTIONS")
        response = create_options_response()

    elif flask.request.method == 'POST':
        print("Checking username")
        json_data = flask.request.json
        print("Data: {}".format(json_data))
        new_username = json_data.get('newUsername')

        db_session = get_session()
        found_user = db_session.query(Account).filter_by(
            username=new_username).first()

        if found_user is None:
            response = create_response(data={
                "success": True,
                "available": True,
            })
            print("Username is available")
        else:
            response = create_response(
                data={
                    "success": False,
                    "available": False,
                }
            )
            print("Username is not available")

    return response


@app.route('/check_login_emil', methods=["OPTIONS", "POST"])
def check_loginEmail():
    if flask.request.method == 'OPTIONS':
        print("Getting OPTIONS")
        response = create_options_response()

    elif flask.request.method == 'POST':
        print("Checking Login user email")
        json_data = flask.request.json
        print("Data: {}".format(json_data))
        new_email = json_data.get('newEmail')

        db_session = get_session()
        found_user = db_session.query(Account).filter_by(
            email=new_email).first()

        if found_user is None:
            response = create_response(data={
                "success": False,
                "available": False,
            })
            print("User Email Not Found")
        else:
            response = create_response(
                data={
                    "success": True,
                    "available": True,
                }
            )
            print("User Email Found")

    return response


@app.route('/check_email', methods=["OPTIONS", "POST"])
def check_email():
    if flask.request.method == 'OPTIONS':
        print("Getting OPTIONS")
        response = create_options_response()

    elif flask.request.method == 'POST':
        print("Checking email")
        json_data = flask.request.json
        print("Data: {}".format(json_data))
        new_email = json_data.get('newEmail')

        db_session = get_session()
        found_email = db_session.query(
            Account).filter_by(email=new_email).first()

        if found_email is None:
            response = create_response(data={
                "success": True,
                "available": True,
            })
            print("Email address is available")
        else:
            response = create_response(
                data={
                    "success": False,
                    "available": False,
                }
            )
            print("Email address is being taken")

    return response

def format_password_message(password_check):
    message_tokens = []
    if 'warning' in password_check:
        warning_message = "Warning: {}".format(password_check['warning'])
        message_tokens.append(warning_message)

    if 'suggestions' in password_check:
        suggestion_message = "Suggestions: " + \
            ' '.join(password_check['suggestions'])
        message_tokens.append(suggestion_message)

    return ' '.join(message_tokens)

@app.route('/register_submit', methods=["OPTIONS", "POST"])
def register_submit():
    if flask.request.method == 'OPTIONS':
        print("Getting OPTIONS")
        response = create_options_response()

    elif flask.request.method == 'POST':
        print("Register submit handling")
        json_data = flask.request.json
        print("Data: {}".format(json_data))

        new_email = json_data.get('newEmail')
        new_username = json_data.get('newUsername')
        new_password = json_data.get('newPassword')

        password_check = zxcvbn(new_password, user_inputs=[
                                new_email, new_username])
        score = password_check['score']

        password_message = format_password_message(password_check)

        if len(new_password) < 8 or password_check.get('warning'):
            print("Too weak: Score `{}` password_message `{}`".format(
                score, password_message))
            response = create_response(
                data={
                    "success": False,
                    "message": "Password too weak. " + password_message
                }
            )
            return response

        db_session = get_session()

        try:
            hash_method = 'pbkdf2:sha256:50000'
            password_hash = generate_password_hash(
                new_password, method=hash_method, salt_length=8)
            new_user = Account(
                username=new_username,
                password_hash=password_hash,
                email=new_email,
            )
            print('Creating new user')
            db_session.add(new_user)
            db_session.commit()
            print("Succeeded")

            response = create_response(data={"success": True}, status=200)

        except IntegrityError:
            db_session.rollback()

            print("IntegrityError")
            error_messages = []

            found_email = db_session.query(
                Account).filter_by(email=new_email).first()
            if found_email:
                error_messages.append("Email in use")

            found_name = db_session.query(Account).filter_by(
                username=new_username).first()
            if found_name:
                error_messages.append("Username in use")

            response = create_response(data={
                "success": False,
                "message": "Account creation failed: " + ", ".join(error_messages)
            })

        db_session.close()

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
