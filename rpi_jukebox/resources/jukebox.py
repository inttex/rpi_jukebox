import os
import pickle

from flask import request
from flask_restful import Resource, abort

def main():
    print(musics)

LOCAL_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'db')
DB_FILENAME = os.path.join(LOCAL_DIRECTORY, 'musics.pickle')
print(DB_FILENAME)

try:
    with open(DB_FILENAME, 'rb') as myfile:
        musics = pickle.load(myfile)
except EOFError:
    print('last parameter file is probably empty..')
    musics = dict()
except IOError:
    print('could not access or find last parameter file')
    musics = dict()


class Jukebox(Resource):

    def get(self):
        return musics

    def post(self):
        rfid = request.form['rfid']
        if rfid not in musics.keys():
            musics[rfid] = None
            try:
                with open(DB_FILENAME, 'wb') as myfile:
                    pickle.dump(musics, myfile)
            except IOError:
                print('could not access or find last parameter file')
            return rfid, 201
        else:
            abort(422, message='rfid {} is already in the database'.format(rfid))


if __name__=='__main__':
    main()
