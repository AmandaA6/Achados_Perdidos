from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, DeclarativeBase

engine = create_engine("sqlite:///database.db")

SessionLocal = scoped_session(sessionmaker(bind=engine))

class Base(DeclarativeBase):
    pass
