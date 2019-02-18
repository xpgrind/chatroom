import os
import sys
from sqlalchemy.orm import relationship

from chatroom.db.session import get_session
from chatroom.db.tables import Account

userid = sys.argv[1]

db_session = get_session()

user_name = db_session.query(Account).filter_by(id=userid).first().username

if user_name is None:
    print("User not in database")

else:
    print(user_name)
