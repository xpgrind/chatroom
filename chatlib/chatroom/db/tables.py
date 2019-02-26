from sqlalchemy import Column, ForeignKey, Integer, String, Unicode, VARCHAR, TIMESTAMP, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Account(Base):
    __tablename__ = 'account'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password_hash = Column(String(128), nullable=False)
    email = Column(String(80), nullable=False)

class Token(Base):
    __tablename__ = 'token'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    token_string = Column(TEXT)
    create_time = Column(TIMESTAMP, nullable=False)
    expire_time = Column(TIMESTAMP, nullable=False)

class Friend(Base):
    __tablename__ = 'friend'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    friend_id = Column(Integer,nullable=False)
    user_id = Column(Integer, primary_key=True, nullable=False)

class Profile_Pic(Base):
    __tablename__ = 'profile_pic'
    id = Column(Integer, primary_key=True)
    account = relationship("Account", backref="user_of_account")
    user = Column(Integer, ForeignKey("account.id"), nullable=False)
    path = Column(TEXT, nullable=False)
    name = Column(String(30))

class Message(Base):
    __tablename__ = 'message'
    message_id = Column(Integer, primary_key=True)
    message = Column(TEXT)
    receiver_id = Column(Integer, nullable=False)
    sender_id = Column(Integer, nullable=False)
    client_time = Column(TIMESTAMP)
    server_time = Column(TIMESTAMP)
