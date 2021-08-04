import signal
import sys
from functools import partial

from flask import Flask
from flask_restful import Resource, Api

from rpi_jukebox import resources

def main():
    run()

def run():

    app = Flask(__name__)
    app.config.from_object('rpi_jukebox.api.config')
    # To get one variable, tape app.config['MY_VARIABLE']
    api = Api(app)



    api.add_resource(resources.homepage.Homepage, '/')
    api.add_resource(resources.jukebox.Jukebox, '/jukebox')

    signal.signal(signal.SIGTERM, partial(stop_server))
    signal.signal(signal.SIGINT, partial(stop_server))

    app.run(debug=True)

def stop_server(signal, frame):
    print('stop api in clean way')
    sys.exit(0)

if __name__ == '__main__':
    main()
