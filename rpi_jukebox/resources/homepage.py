import os
import pickle

from flask_restful import Resource

LOCAL_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'db')
DB_FILENAME = os.path.join(LOCAL_DIRECTORY, 'musics.pickle')

class Homepage(Resource):
    def get(self):
        try:
            with open(DB_FILENAME, 'rb') as myfile:
                musics = pickle.load(myfile)
        except EOFError:
            print('last parameter file is probably empty..')
            musics = dict()
        except IOError:
            print('could not access or find last parameter file')
            musics = dict()
        lines = list()
        for rfid, title in musics.items():
            lines.append("<p> {}: {}</p>".format(rfid, title))
        html_content = os.linesep.join(lines)
        return html_content
