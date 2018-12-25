from chatroom.db.session import get_session
from chatroom.db.tables import Account

import flask
from flask_cors import CORS
from flask import Flask, jsonify
from flask_socketio import SocketIO, join_room, emit

from sqlalchemy.exc import IntegrityError
app = Flask(__name__)
client_address = "http://localhost:8080"
cors = CORS(app)
socketio = SocketIO(app)


class RequestError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None, headers=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
        self.headers = headers

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(RequestError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    if error.headers is not None:
        h = response.headers
        for k, v in error.headers.items():
            h[k] = v
    return response


@app.route('/login', methods=["OPTIONS", "POST"])
def login():
    raw_methods = ["OPTIONS", "POST"]
    string_methods = ', '.join(sorted(x.upper() for x in raw_methods))
    string_headers = ', '.join(x.upper() for x in ['Content-type'])
    option_headers = {
        'Access-Control-Allow-Origin': client_address,
        'Access-Control-Allow-Methods': string_methods,
        'Access-Control-Allow-Headers': string_headers,
        'Access-Control-Allow-Credentials': 'true',
    }

    if flask.request.method == 'OPTIONS':
        print("Getting OPTIONS")
        response = flask.current_app.make_default_options_response()

    elif flask.request.method == 'POST':
        print("Login Attempt")
        json_data = flask.request.json
        username = json_data.get('username')
        password = json_data.get('password')
        if password != "password":
            raise RequestError("Invalid password", headers=option_headers)

        response = flask.jsonify({
                "username": username,
                "token": "insecure_token",
        })

    h = response.headers
    for k, v in option_headers.items():
        h[k] = v

    return response


@app.route('/users/<command>', methods=["POST"])
def users(command):
    # This is how you get data from the post request body
    json_data = flask.request.json

    # This is how you get data from the arguments
    args = flask.request.args

    print("Command: {}, Args: {}, Params: {}".format(command, args, json_data))
    if not command in {"register", "list", "remove"}:
        raise RequestError("Invalid command: {}".format(command))

    db_session = get_session()

    if command == "register":
        username = json_data.get('username')
        if username is None:
            raise RequestError("Username is null!")
        try:
            new_user = Account(
                username=username,
                description="a silly cat"
            )
            db_session.add(new_user)
            db_session.commit()
        except IntegrityError:
            raise RequestError("Username already exists: {}".format(username))

    elif command == "list":
        from pprint import pprint; import pdb; pdb.set_trace()
        raise NotImplementedError()
    elif command == "remove":
        username = json_data.get('username')
        if username is None:
            raise RequestError("Username is null!")
        user = db_session.query(Account).filter_by(username=username).first()
        if user is None:
            raise RequestError("Username does not exist: {}".format(username))

        db_session.delete(user)
        db_session.commit()

    return jsonify({
        "message": "Command: {}, Success".format(command)
    })


@socketio.on('connect')
def handler__connect():
    print('connect: enter')
    print('cookies:', flask.request.cookies)
    cookies = {k.strip('; '): v for k, v in (flask.request.cookies or {}).items()}
    token = cookies.get('token')
    if token:
        # TODO: Validate login token!
        print('connect: ACCEPT')
        emit('connect_info', {
            'token': token,
            'sid': flask.request.sid,
        })
        return True
    else:
        print('connect: REJECT <no token>')
        return False


@socketio.on('disconnect')
def handler__disconnect():
    print('disconnect: enter')
    sid = getattr(flask.request, 'sid', None)
    token = flask.session.get('token')
    user_uuid = flask.session.get('user_uuid')
    print('sid', (sid or '<NO SID>'))
    print('token', (token or '<NO TOKEN>'))
    print('user_uuid', (user_uuid or '<NO USER_UUID>'))
    print('disconnect: done')


if __name__ == '__main__':
    # app.run()
    socketio.run(app, debug=True)
