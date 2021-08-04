import os

from flask_restful import Resource

LOCAL_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'db')

class Jukebox(Resource):
    def get(self):
        return 'dico of database'
