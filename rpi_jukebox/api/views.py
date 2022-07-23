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
api.add_resource(resources.Update, '/admin/update')
api.add_resource(resources.APILog, '/log/api')
api.add_resource(resources.ClientLog, '/log/client_log')
api.add_resource(resources.ClientError, '/log/client_error')
api.add_resource(resources.Parameters, '/parameters/<name>')

def stop_server(signal, frame):
    print('stop api in clean way')
    sys.exit(0)

@app.route('/')
def home_page():
    musics = Musics.query.all()
    return render_template('index.html', musics=musics, random_stop=app.config['PARAMETERS']['random_stop'])

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

@app.route('/log')
def log_page():
    return render_template('log.html')

@app.route('/parameters')
def parameters_page():
    return render_template('parameters.html', parameters=app.config['PARAMETERS'])

signal.signal(signal.SIGTERM, partial(stop_server))
signal.signal(signal.SIGINT, partial(stop_server))

if __name__ == '__main__':
    app.run(debug=True)
