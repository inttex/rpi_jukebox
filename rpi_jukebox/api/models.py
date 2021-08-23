from sqlalchemy import Column, Integer, String

from rpi_jukebox.api.database import Base

# from flask_sqlalchemy import SQLAlchemy

# from rpi_jukebox.api.views import app

# db = SQLAlchemy(app)

class Musics(Base):
    __tablename__ = 'musics'
    id = Column(Integer, primary_key=True)
    title = Column(String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Musics %r>' % self.title

if __name__=='__main__':
    db.create_all()
