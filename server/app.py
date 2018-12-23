from chatroom.db.session import get_session
from chatroom.db.tables import Account

from flask import Flask, jsonify
app = Flask(__name__)


@app.route('/')
def hello():
    session = get_session()
    print("Adding topher")
    new_topher = Account(username='topher', description="a silly cat")
    session.add(new_topher)
    session.commit()

    return jsonify({
        "message": "Successfully added topher"
    })


if __name__ == '__main__':
    app.run()
