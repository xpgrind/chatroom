import os
import sys
from sqlalchemy.orm import relationship

from chatroom.db.session import get_session
from chatroom.db.tables import Friend

# Goal: Add the following friendships:
    #    5 |         3
    #    5 |         2
    #    5 |         1
# Then delete just 1 of them (Delete 5 friends with 2)
user_id = sys.argv[1]
friend_id = sys.argv[2]

db_session = get_session()
friend_exists = db_session.query(Friend).filter_by(user_id=user_id, friend_id=friend_id).first()
# You can do this,
# User.query.filter_by(id=123).delete()
# or
# User.query.filter(User.id == 123).delete()

if friend_exists is None:
    print("friendship not in database, add him already")
    new_friend = Friend(
                user_id=user_id,
                friend_id=friend_id
            )
    db_session.add(new_friend)

else:
    print("friendship in database, delete him")
    db_session.query(Friend).filter_by(user_id=user_id, friend_id=friend_id).delete()

db_session.commit()

print("Showing current friends")
for row in db_session.query(Friend):
    print(row.user_id, row.friend_id)

db_session.close()
