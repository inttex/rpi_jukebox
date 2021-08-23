import os

import xdg
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

path = 'sqlite:///' + os.path.join(xdg.xdg_data_home(), 'rpi_jukebox', 'musics.db')
engine = create_engine(path, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import rpi_jukebox.api.models
    Base.metadata.create_all(bind=engine)
