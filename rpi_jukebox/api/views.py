import signal
import sys
from functools import partial
import os
import pickle

from flask import Flask, render_template, url_for
from flask_restful import Resource, Api

from rpi_jukebox.api import resources, homepage
from rpi_jukebox.api.database import db_session


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

def stop_server(signal, frame):
    print('stop api in clean way')
    sys.exit(0)

@app.route('/')
def home_page():
    try:
        with open(DB_FILENAME, 'rb') as myfile:
            musics = pickle.load(myfile)
    except EOFError:
        print('last parameter file is probably empty..')
        musics = dict()
    except IOError:
        print('could not access or find last parameter file')
        musics = dict()
    html_content = homepage.index(musics)
    # return render_template('index.html', musics=musics)
    return html_content

signal.signal(signal.SIGTERM, partial(stop_server))
signal.signal(signal.SIGINT, partial(stop_server))

if __name__ == '__main__':
    app.run(debug=True)
