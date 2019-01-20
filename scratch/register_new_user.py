import os
import sys
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from chatroom.db.session import get_session
from chatroom.db.tables import Account

db_session = get_session()

username = 'topher'
email = 'topher@gmail.com'
password = 'password'

hash_method = 'pbkdf2:sha256:50000'
password_hash = generate_password_hash(password, method=hash_method, salt_length=8)

new_user = Account(
    username=username,
    password_hash=password_hash,
    email=email,
)

db_session.add(new_user)
db_session.commit()
