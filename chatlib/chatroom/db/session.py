from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import get_db_uri

_engine = create_engine(get_db_uri())
_DBSession = sessionmaker(bind=_engine)

def get_session():
    return _DBSession()
