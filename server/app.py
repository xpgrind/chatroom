import secrets
from datetime import datetime, timedelta
import base64

import flask
from flask import Flask
import flask_socketio

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
from zxcvbn import zxcvbn

from chatroom.db.tables import Account, Token, Friend, ProfilePic, Message
from chatroom_router import ChatroomRouter, client_address, validate_credentials
from chatroom.db.session import get_session

app = Flask(__name__)
chatroom = ChatroomRouter(app)

socketio = flask_socketio.SocketIO(app)

# @chatroom.route('/insecure', methods=["GET", "OPTIONS", "POST"], requires_login=False)
# def insecure_route():
#     response = flask.jsonify({"success": True})
#     return response


# @chatroom.route('/secure', methods=["GET", "OPTIONS", "POST"])
# def secure_route():
#     response = flask.jsonify({"success": True})
#     return response


# @chatroom.route('/secure_needs_db', methods=["GET", "OPTIONS", "POST"], db=True)
# def secure_route_with_db(db_session):
#     response = flask.jsonify({"success": True})
#     return response


@chatroom.route('/login', methods=["OPTIONS", "POST"], db=True, requires_login=False)
def login(db_session):
    # Disabled during local testing while serving over HTTP
    secure_cookie = False

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
            response = flask.jsonify({"success": True, "token": str_token, "user_id": user_id})
            response.set_cookie('chatroom_token', str_token, secure=secure_cookie, max_age=86400)
            response.set_cookie('chatroom_user_id', str(user_id), secure=secure_cookie, max_age=86400)
            print("Set chatroom_token cookie")
            return response, 200
        else:
            db_session.rollback()
            token = ''
            error_messages.append("Password is Wrong")
            response = flask.jsonify({
                "success": False,
                "message": "Login failed: " + ", ".join(error_messages)
            })
            response.set_cookie('chatroom_token', '', secure=secure_cookie, max_age=0)
            response.set_cookie('chatroom_user_id', '', secure=secure_cookie, max_age=0)
            return response, 403
    else:
        error_messages.append("User Email Not Found")
        print("Email not Found")
        response = flask.jsonify({
            "success": False,
            "message": "Login failed: " + ", ".join(error_messages)
        })
        response.set_cookie('chatroom_token', '', secure=secure_cookie, max_age=0)
        response.set_cookie('chatroom_user_id', '', secure=secure_cookie, max_age=0)
        return response, 403


clients = {}
user_sids = {}

class ConnectedClient:
    def __init__(self, sid):
        self.sid = sid
        self.connected = True

    # Emits data to a socket's unique room
    def emit(self, event, data):
        flask_socketio.emit(event, data, room=self.sid)


@socketio.on('connect')
def handler__connect():
    print('connect: enter')
    sid = getattr(flask.request, 'sid', None)
    print('cookies:', flask.request.cookies)
    cookies = {k.strip('; '): v for k, v in (flask.request.cookies or {}).items()}
    token = cookies.get('chatroom_token')
    user_id = cookies.get('chatroom_user_id')
    db_session = get_session()
    # Verify token and user name:
    if token is not None and user_id is not None:
        validation = validate_credentials(db_session, int(user_id), token)
    else:
        validation = {"success": False, "reason": "token or user_id missing"}

    user_id = int(user_id)

    print("Connect login response: {}".format(validation))

    if validation.get('success'):
        assert sid is not None

        if user_id in user_sids:
            user_sids[user_id].add(sid)
        else:
            user_sids[user_id] = {sid}
        clients[sid] = ConnectedClient(sid)
        # Flask session can be used for storing information iirc?
        flask.session['chatroom_token'] = token
        flask.session['chatroom_user_id'] = user_id
        flask_socketio.emit('connect_info', {
            'sid': sid,
        })
        return True
    else:
        print('connect: REJECT <no token>')
        return False


@socketio.on('disconnect')
def handler__disconnect():
    print('disconnect: enter')
    sid = getattr(flask.request, 'sid', None)

    chatroom_token = flask.session.get('chatroom_token')
    chatroom_user_id = flask.session.get('chatroom_user_id')
    if chatroom_user_id is not None:
        user_id = int(chatroom_user_id)
        if user_id in user_sids:
            try:
                user_sids[user_id].remove(sid)
            except KeyError:
                # Sid already removed
                pass

    print("Disconnect user_id {} token {}".format(chatroom_user_id, chatroom_token))
    # TODO: Expire the token for this user
    print('disconnect: done')


@socketio.on('/friends/list')
def friends_list(args):
    db_session = get_session()
    chatroom_user_id = flask.session.get('chatroom_user_id')

    print("Friends list, arguments: {}, user id: {}".format(args, chatroom_user_id))

    friends = []

    prepared_statement = text('select account.username from friend inner join account on friend.friend_id = account.id where friend.user_id = :my_user_id;')
    friend_rows = db_session.execute(prepared_statement, {'my_user_id': chatroom_user_id})

    for row in friend_rows:
        username = row[0]
        friends.append(username)

    target_sids = user_sids[chatroom_user_id]
    for target_sid in target_sids:
        clients[target_sid].emit('message/new', {
            "success": True,
            "message": "This is an example of how you can emit a message to any user",
        })

    return {
        "success": True,
        "friends": friends,
    }

# @chatroom.route('/friends/list', methods=["OPTIONS", "POST"], db=True)
# def friends_list(db_session):
#     json_data = flask.request.json
#     print("Data: {}".format(json_data))
#     user_id = json_data.get('user_id')
#     friends = db_session.query(Friend).filter_by(user_id=user_id).all()
#     # friend_ids = [x.friend_id for x in friends]




@chatroom.route('/friends/add', methods=["OPTIONS", "POST"], db=True)
def add_friends(db_session):
    json_data = flask.request.json
    print("Data: {}".format(json_data))
    user_id = json_data.get('user_id')
    friend_name = json_data.get('new_friend')

    if not friend_name:
        print("You must specify friend name")
        return flask.jsonify({
            "success": False,
            "message": "You must specify friend name"
        }), 400

    found_user = db_session.query(Account).filter_by(username=friend_name).first()
    if found_user:
        friend_id = found_user.id
        if user_id == friend_id:
            print("You cannot add yourself")
            return flask.jsonify({
                "success": False,
                "message": "You cannot add yourself"
            }), 400

        friendship = db_session.query(Friend).filter_by(user_id=user_id, friend_id=friend_id).first()
        if friendship:
            print("You have already added {}".format(friend_name))
            return flask.jsonify({
                "success": False,
                "message": "You already addeded " + friend_name
            }), 400

        else:
            new_friend = Friend(
                user_id=user_id,
                friend_id=friend_id
            )
            db_session.add(new_friend)
            db_session.commit()
            print("Succeeded in adding {} as a friend of {}".format(friend_id, user_id))
            return flask.jsonify({
                "success": True,
                "message": "Adding friend succeeded",
            }), 200
    else:
        print("Friend Not Found")
        return flask.jsonify({
            "success": False,
            "message": "Friend Not Found",
        }), 400

@chatroom.route('/friends/delete', methods=["OPTIONS", "POST"], db=True)
def delete_friends(db_session):
    json_data = flask.request.json
    print("Data: {}".format(json_data))
    user_id = json_data.get('user_id')
    friend_name = json_data.get('friend')

    if not friend_name:
        print("You must specify friend name")
        return flask.jsonify({
            "success": False,
            "message": "You must specify friend name"
        }), 400

    found_user = db_session.query(Account).filter_by(username=friend_name).first()

    if found_user:
        friend_id = found_user.id
        if user_id == friend_id:
            print("You cannot delete yourself")
            return flask.jsonify({
                "success": False,
                "message": "You cannot delete yourself"
            }), 400

        friendship = db_session.query(Friend).filter_by(user_id=user_id, friend_id=friend_id).first()

        if friendship:
            db_session.query(Friend).filter_by(user_id=user_id, friend_id=friend_id).delete()
            db_session.commit()
            print("Succeeded in deleting {} as a friend of {}".format(friend_id, user_id))
            return flask.jsonify({
                "success": True,
                "message": "Deleting friend succeeded",
            }), 200

        else:
            print("Failed in deleting {} as a friend of {}".format(friend_id, user_id))
            return flask.jsonify({
                "success": False,
                "message": "This friend doesn't exist in your list",
            }), 400
    else:
        print("Friend Not Found")
        return flask.jsonify({
            "success": False,
            "message": "Friend Not Found",
        }), 400


@chatroom.route('/send_msg', methods=["OPTIONS", "POST"], db=True)
def send_msg(db_session):
    json_data = flask.request.json
    print("Data: {}".format(json_data))
    sender_id = json_data.get('user_id')
    message = json_data.get('message')
    receiver = json_data.get('receiver')
    client_time = json_data.get('client_time')
    server_time = datetime

    receiver_id = db_session.query(Account).filter_by(username=receiver).first().id

    new_message = Message(
        receiver_id=receiver_id,
        sender_id=sender_id,
        message=message,
        client_time=client_time,
        server_time=server_time
    )
    db_session.add(new_message)
    db_session.commit()
    print("Succeeded in sending messages")
    return flask.jsonify({
        "success": True,
        "message": "Sending messages succeeded",
    }), 200

@chatroom.route('/get_info', methods=["OPTIONS", "POST"], db=True)
def get_info(db_session):
    json_data = flask.request.json
    print("Data: {}".format(json_data))
    user_id = json_data['user_id']
    user_name = db_session.query(Account).filter_by(id=user_id).first().username
    # photo = db_session.query(ProfilePic).filter_by(user=user_id).first().path
    return flask.jsonify({
        "success": True,
        "username": user_name,
        # "photo": photo
    }), 200

@chatroom.route('/upload_photo', methods=["OPTIONS", "POST"], db=True)
def upload_photo(db_session):
    json_data = flask.request.json
    print("Data: {}".format(json_data))
    user_id = json_data.get('user_id')
    photo_path = json_data.get('path')
    photo = ProfilePic(
        user=user_id,
        path=photo_path
    )
    db_session.add(photo)
    db_session.commit()
    print('upload phot succeeds ! ')
    return flask.jsonify({
        "success": True
    }), 200

@chatroom.route('/check_username', methods=["OPTIONS", "POST"], db=True, requires_login=False)
def check_username(db_session):
    json_data = flask.request.json
    print("Data: {}".format(json_data))
    new_username = json_data.get('newUsername')

    found_user = db_session.query(Account).filter_by(username=new_username).first()

    if found_user is None:
        print("Username is available")
        return flask.jsonify({
            "success": True,
            "available": True
        }), 200

    else:
        print("Username is not available")
        return flask.jsonify({
            "success": True,
            "available": False
        })


@chatroom.route('/check_email', methods=["OPTIONS", "POST"], db=True, requires_login=False)
def check_email(db_session):
    json_data = flask.request.json
    print("Data: {}".format(json_data))
    new_email = json_data['newEmail']
    found_email = db_session.query(Account).filter_by(email=new_email).first()

    if found_email is None:
        print("Email address Not Found")
        return flask.jsonify({
            "success": True,
            "available": True,
        })
    else:
        print("Email address Found")
        return flask.jsonify({
            "success": True,
            "available": False,
        })


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

    try:
        new_email = json_data['newEmail']
        new_username = json_data['newUsername']
        new_password = json_data['newPassword']
    except KeyError as e:
        assert False, "You must set {}".format(e)

    assert new_password, "Password cannot be empty"

    password_check = zxcvbn(new_password, user_inputs=[new_email, new_username])
    score = password_check['score']

    password_message = format_password_message(password_check)

    if len(new_password) < 8 or password_check.get('warning'):
        print("Too weak: Score `{}` password_message `{}`".format(
            score, password_message))
        assert False, "Weak password: " + password_message

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
        }), 200

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
        }), 200



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
    # app.run(debug=True)
    socketio.run(app)
