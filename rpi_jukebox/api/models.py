from sqlalchemy import Column, Integer, String

from api.database import Base

# from flask_sqlalchemy import SQLAlchemy

# from rpi_jukebox.api.views import app

# db = SQLAlchemy(app)

class Musics(Base):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Musics %r>' % self.title

if __name__=='__main__':
    db.create_all()
