from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = None
session = None


def shutdown_session(exception=None):
    global session
    session.remove()


def init_db(app):
    global engine
    engine = create_engine(app.config['DATABASE_URL'])

    global session
    session = scoped_session(sessionmaker(bind=engine))

    Base.metadata.bind = engine

    if app.config.get('TESTING'):
        Base.metadata.create_all(engine)

    # Close session at the end of each request
    # Or when the app is shutdown
    app.teardown_appcontext(shutdown_session)
