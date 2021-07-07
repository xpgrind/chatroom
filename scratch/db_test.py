import os
import sys
from sqlalchemy.orm import relationship
from chatroom.db.session import get_session
from chatroom.db.tables import Message

session = get_session()
topher_user = session.query(Message).filter_by(receiver_id='2').all()

for i in topher_user:
    print(i.message)
