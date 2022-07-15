import signal
import sys
from functools import partial
import os
import pickle

from flask import Flask, render_template, url_for
from flask_restful import Resource, Api

from rpi_jukebox.api import resources
from rpi_jukebox.api.database import db_session
from rpi_jukebox.api.models import Musics

LOCAL_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'db')
DB_FILENAME = os.path.join(LOCAL_DIRECTORY, 'musics.pickle')

app = Flask(__name__)
app.config.from_object('rpi_jukebox.api.config')
# To get one variable, tape app.config['MY_VARIABLE']
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

api = Api(app)

api.add_resource(resources.Jukebox, '/jukebox')
api.add_resource(resources.UnWrapper, '/unwrapper')
api.add_resource(resources.Music, '/jukebox/<rfid>')
api.add_resource(resources.Update, '/update')
api.add_resource(resources.APILog, '/log/api')
api.add_resource(resources.ClientLog, '/log/client')

def stop_server(signal, frame):
    print('stop api in clean way')
    sys.exit(0)

@app.route('/')
def home_page():
    # html_content = homepage.index()
    # return html_content
    musics = Musics.query.all()
    return render_template('index.html', musics=musics, random_stop=app.config['parameters']['random_stop'])

signal.signal(signal.SIGTERM, partial(stop_server))
signal.signal(signal.SIGINT, partial(stop_server))

if __name__ == '__main__':
    app.run(debug=True)
