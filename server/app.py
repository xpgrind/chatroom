from chatroom.db.session import get_session
from chatroom.db.tables import Account

from flask import Flask, jsonify, request
from sqlalchemy.exc import IntegrityError
app = Flask(__name__)


class RequestError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(RequestError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/users/<command>', methods=["POST"])
def users(command):
    # This is how you get data from the post request body
    json_data = request.json
    # This is how you get data from the arguments
    args = request.args

    print("Command: {}, Args: {}, Params: {}".format(command, args, json_data))
    if not command in {"register", "list", "remove"}:
        raise RequestError("Invalid command: {}".format(command))

    session = get_session()

    if command == "register":
        try:
            new_user = Account(
                username=args.get('username'),
                description="a silly cat"
            )
            session.add(new_user)
            session.commit()
        except IntegrityError:
            raise RequestError("Username already exists: {}".format(args.get('username')))

    elif command == "list":
        from pprint import pprint; import pdb; pdb.set_trace()
        raise NotImplementedError()
    elif command == "remove":
        user = session.query(Account).filter_by(username=args.get('username')).first()
        if user is None:
            raise RequestError("Username does not exist: {}".format(args.get('username')))

        session.delete(user)
        session.commit()

    return jsonify({
        "message": "Success"
    })


if __name__ == '__main__':
    app.run()
