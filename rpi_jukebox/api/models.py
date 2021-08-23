from sqlalchemy import Column, Integer, String

from rpi_jukebox.api.database import Base

# from flask_sqlalchemy import SQLAlchemy

# from rpi_jukebox.api.views import app

# db = SQLAlchemy(app)

class Musics(Base):
    __tablename__ = 'musics'
    id = Column(Integer, primary_key=True)
    rfid = Column(Integer, unique=True, nullable=False)
    title = Column(String(80), unique=True, nullable=True)

    def __init__(self, rfid=None, title=None):
        self.rfid = rfid
        self.title = title

    def __repr__(self):
        return '<Musics %r>' % (self.title)

if __name__=='__main__':
    db.create_all()
