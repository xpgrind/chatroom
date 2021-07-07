import os
import sys
from sqlalchemy.orm import relationship

from chatroom.db.session import get_session
from chatroom.db.tables import Account

user = sys.argv[1]

db_session = get_session()

user_id = db_session.query(Account).filter_by(username=user).first().id

if user_id is None:
    print("User not in database")

else:
    print(user_id)
