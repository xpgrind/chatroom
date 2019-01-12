import os
import sys
from sqlalchemy.orm import relationship

from chatroom.db.session import get_session
from chatroom.db.tables import Account

email = sys.argv[1]

db_session = get_session()
topher_user = db_session.query(Account).filter_by(email=email).first()
if topher_user is None:
    print("Email not in database")
else:
    print("Email in database")
