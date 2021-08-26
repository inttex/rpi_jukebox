import os
import pickle

from flask import request, url_for, redirect
from flask_restful import Resource, abort
import requests
from sqlalchemy import exc

from rpi_jukebox.api.database import db_session
from rpi_jukebox.api.models import Musics

def main():
    print(musics)

def query_by_rfid(rfid):
    r = Musics.query.filter(Musics.rfid==rfid)
    if r.count()==0:
        abort(404, message="rfid {} doesn't exist".format(rfid))
    return r.first()

class Jukebox(Resource):

    def get(self):
        answer = [(el.rfid, el.title) for el in Musics.query.all()]
        return answer

    def post(self):
        rfid = request.form['rfid']
        u = Musics(rfid=rfid)
        db_session.add(u)
        try:
            db_session.commit()
        except exc.SQLAlchemyError as e:
            abort(422, message=repr(e))
        return redirect(url_for('home_page'))

class Music(Resource):
    def get(self, rfid):
        element = query_by_rfid(rfid)
        title = element.title
        if title is None:
            abort(410, message="there is no music for rfid {}".format(rfid))
        return title

    def delete(self, rfid):
        element = query_by_rfid(rfid)
        db_session.delete(element)
        db_session.commit()
        return '', 204

    def put(self, rfid):
        element = query_by_rfid(rfid)
        title = request.form['title']
        element.title = title
        db_session.commit()
        return title, 201

class UnWrapper(Resource):

    def get(self):
        method = request.args.get('method')
        if method == 'DELETE':
            rfid = request.args.get('rfid')
            url = url_for('jukebox', _external=True) + '/{}'.format(rfid)
            requests.delete(url)
            return redirect(url_for('home_page'))

    def post(self):
        method =request.form['method']
        if method == 'PUT':
            rfid = request.form['rfid']
            title = request.form['title']
            url = url_for('jukebox', _external=True) + '/{}'.format(rfid)
            requests.put(url, data={'title': title})
            return redirect(url_for('home_page'))

if __name__=='__main__':
    main()
