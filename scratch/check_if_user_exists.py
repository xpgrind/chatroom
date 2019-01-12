import os
import sys
from sqlalchemy.orm import relationship

from chatroom.db.session import get_session
from chatroom.db.tables import Account

username = sys.argv[1]

db_session = get_session()
topher_user = db_session.query(Account).filter_by(username=username).first()
if topher_user is None:
    print("User not in database")
else:
    print("User in database")
