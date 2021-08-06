import os
import pickle

from flask import request, url_for, redirect
from flask_restful import Resource, abort
import requests

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

def save_db(musics):
    try:
        with open(DB_FILENAME, 'wb') as myfile:
            pickle.dump(musics, myfile)
    except IOError:
        print('could not access or find last parameter file')


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
        save_db(musics)
        return rfid, 201

class Music(Resource):
    def get(self, rfid):
        abort_if_music_doesnt_exist(rfid)
        abort_if_music_is_empty(rfid)
        return musics[rfid]

    def delete(self, rfid):
        abort_if_music_doesnt_exist(rfid)
        del musics[rfid]
        save_db(musics)
        return '', 204

    def put(self, rfid):
        abort_if_music_doesnt_exist(rfid)
        title = request.form['title']
        musics[rfid] = title
        save_db(musics)
        return title, 201

class UnWrapper(Resource):

    def get(self):
        method = request.args.get('method')
        if method == 'DELETE':
            rfid = request.args.get('rfid')
            url = url_for('jukebox', _external=True) + '/{}'.format(rfid)
            requests.delete(url)
            return redirect(url_for('home_page'))

if __name__=='__main__':
    main()
