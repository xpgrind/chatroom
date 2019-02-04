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
    friend_id = Column(Integer, nullable=True)
    user_id = Column(Integer, primary_key=True, nullable=False)
