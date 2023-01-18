import enum

from sqlalchemy import Column, Integer, String, LargeBinary, Enum

from rpi_jukebox.api.database import Base


# from flask_sqlalchemy import SQLAlchemy

# from rpi_jukebox.api.views import app

# db = SQLAlchemy(app)

class SpType(enum.Enum):
    ALBUM = 1
    SONG = 2
    PLAYLIST = 3


class Musics(Base):
    __tablename__ = 'sp_musics'
    id = Column(Integer, primary_key=True)
    rfid = Column(Integer, unique=True, nullable=False)
    title = Column(String(80), unique=False, nullable=True)
    sp_uuid = Column(String(80), unique=True, nullable=True)

    # sp_type = Column(Enum(SpType), default=SpType.ALBUM)
    # image = Column(LargeBinary, nullable=True)
    # last_played_song = Column(String(80), nullable=True)
    # last_timestamp = Column(Integer, unique=True, nullable=False)

    def __init__(self, rfid=None, title=None, wavfile=None, sp_uuid=None):
        self.rfid = rfid
        self.title = title
        self.sp_uuid = sp_uuid

    def __repr__(self):
        return '<Musics %r>' % (self.title)


if __name__ == '__main__':
    db.create_all()
