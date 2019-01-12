import os
import sys
from sqlalchemy.orm import relationship

from chatroom.db.session import get_session
from chatroom.db.tables import Account

session = get_session()
print("Removing topher")
topher_user = session.query(Account).filter_by(username='topher').first()
session.delete(topher_user)
session.commit()

session = get_session()
print("Adding topher")
new_topher = Account(username='topher', description="a silly cat")
session.add(new_topher)
session.commit()
