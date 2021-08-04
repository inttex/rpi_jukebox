import os
import pickle

from flask import request
from flask_restful import Resource, abort

def main():
    print(musics)

LOCAL_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'db')
DB_FILENAME = os.path.join(LOCAL_DIRECTORY, 'musics.pickle')

def abort_if_music_doesnt_exist(rfid):
    if rfid not in musics:
        abort(404, message="rfid {} doesn't exist".format(rfid))

def abort_if_music_is_empty(rfid):
    if not musics[rfid]:
        abort(410, message="there is no music for rfid {}".format(rfid))

def abort_if_rfid_is_already_defined(rfid):
    if rfid in musics.keys():
        abort(422, message='rfid {} is already in the database'.format(rfid))

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
        abort_if_rfid_is_already_defined(rfid)
        musics[rfid] = None
        try:
            with open(DB_FILENAME, 'wb') as myfile:
                pickle.dump(musics, myfile)
        except IOError:
            print('could not access or find last parameter file')
        return rfid, 201

class Music(Resource):
    def get(self, rfid):
        abort_if_music_doesnt_exist(rfid)
        abort_if_music_is_empty(rfid)
        return musics[rfid]


if __name__=='__main__':
    main()
