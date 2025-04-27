# db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

DB_FILENAME = 'db.sqlite'
DB_URL = f'sqlite:///{DB_FILENAME}'

engine = create_engine(DB_URL, connect_args={'check_same_thread': False})
SessionLocal = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

def init_db():
    if not os.path.exists(DB_FILENAME):
        Base.metadata.create_all(bind=engine)
