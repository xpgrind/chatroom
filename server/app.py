import json

import flask
from flask import Flask, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from zxcvbn import zxcvbn

from chatroom.db.session import get_session
from chatroom.db.tables import Account
from chatroom.db.tables import Token
from chatroom.db.tables import Friend

import secrets
from datetime import datetime
from datetime import timedelta
import base64


from chatroom_router import ChatroomRouter, client_address

app = Flask(__name__)

chatroom = ChatroomRouter(app)

@chatroom.route('/insecure', methods=["GET", "OPTIONS", "POST"], requires_login=False)
def insecure_route():
    response = flask.jsonify({"success": True})
    return response


@chatroom.route('/secure', methods=["GET", "OPTIONS", "POST"])
def secure_route():
    response = flask.jsonify({"success": True})
    return response


@chatroom.route('/secure_needs_db', methods=["GET", "OPTIONS", "POST"], db=True)
def secure_route_with_db(db_session):
    response = flask.jsonify({"success": True})
    return response


@chatroom.route('/login', methods=["OPTIONS", "POST"], db=True, requires_login=False)
def login(db_session):
    print("Login Attempt")
    json_data = flask.request.json
    print("Data: {}".format(json_data))
    useremail = json_data.get('email')
    password = json_data.get('password')

    error_messages = []
    found_email = db_session.query(Account).filter_by(email=useremail).first()

    if found_email:
        password_hash = db_session.query(Account).filter_by(email=useremail).first().password_hash
        correct_password = check_password_hash(password_hash, password)
        user_id = db_session.query(Account).filter_by(email=useremail).first().id

        if correct_password:
            create_time = datetime.utcnow()
            token = secrets.token_bytes()
            str_token = base64.b64encode(token).decode('utf-8')

            new_token = Token(
                user_id=user_id,
                create_time=create_time,
                token_string=str_token,
                expire_time=create_time + timedelta(hours=24)
            )

            db_session.add(new_token)
            db_session.commit()

            print("Login Succeeded")
            return flask.jsonify({"success": True, "token": str_token, "user_id": user_id})
        else:
            db_session.rollback()
            token = ''
            error_messages.append("Password is Wrong")
            return flask.jsonify({
                "success": False,
                "message": "Login failed: " + ", ".join(error_messages)
            }), 403
    else:
        error_messages.append("User Email Not Found")
        print("Email not Found")
        return flask.jsonify({
            "success": False,
            "message": "Login failed: " + ", ".join(error_messages)
        }), 403


@chatroom.route('/friends/add', methods=["OPTIONS", "POST"], db=True, requires_login=True)
def addfriends(db_session):
    json_data = flask.request.json
    print("Data: {}".format(json_data))

    friend_name = json_data.get('new_friend')
    if friend_name is None:
        print("Friend Not Found")

    user_id = json_data.get('user_id')
    found_friend = db_session.query(Account).filter_by(username=friend_name).first()

    if found_friend:
        friend_id = found_friend.id

        record = Friend(user_id=user_id, friend_id=friend_id)

        print("Adding Friend Succeeds")
        db_session.add(record)
        db_session.commit()

        return flask.jsonify({
            "success": True,
            "message": "Adding Friend Succeeds"
        }), 200
    else:
        print("User not Found")
        return flask.jsonify({
            "success": False,
            "message": "Adding Friend failed: User Not Found"
        }), 400


@chatroom.route('/friends/list', methods=["OPTIONS", "POST"], db=True, requires_login=True)
def friendsList(db_session):
    json_data = flask.request.json
    print("Data: {}".format(json_data))
    user_id = json_data.get('user_id')
    records = db_session.query(Friend).filter_by(user_id=user_id).all()

    for item in records:
        friend_id = item.friend_id
        friend_name = db_session.query(Account).filter_by(id=friend_id).username
        print(friend_name)


@chatroom.route('/check_username', methods=["OPTIONS", "POST"], db=True, requires_login=False)
def check_username(db_session):
    json_data = flask.request.json
    print("Data: {}".format(json_data))
    new_username = json_data.get('newUsername')

    found_user = db_session.query(Account).filter_by(
        username=new_username).first()

    if found_user is None:
        return flask.jsonify({
            "success": True,
            "available": True
        }), 200
        print("Username is available")

    else:
        return flask.jsonify({
            "success": True,
            "available": False
        })
        print("Username is not available")


@chatroom.route('/check_email', methods=["OPTIONS", "POST"], db=True, requires_login=False)
def check_email(db_session):
    json_data = flask.request.json
    print("Data: {}".format(json_data))
    new_email = json_data.get('newEmail')
    found_email = db_session.query(Account).filter_by(email=new_email).first()

    if found_email is None:
        return flask.jsonify({
            "success": True,
            "available": True,
        })
        print("Email address Not Found")

    else:
        return flask.jsonify({
            "success": True,
            "available": False,
        })
        print("Email address Found")


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


@chatroom.route('/register_submit', methods=["OPTIONS", "POST"], db=True, requires_login=False)
def register_submit(db_session):
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
        return flask.jsonify({
        "success": False,
        "message": "Password too weak. " + password_message
    })

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

        return flask.jsonify({
        "success": True,
        }),200

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

        return flask.jsonify({
        "success": False,
        "message": "Account creation failed: " + ", ".join(error_messages)
        }),200



# @chatroom.route('/users/<command>', methods=["POST"])
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


if __name__ == '__main__':
    app.run(debug=True)
