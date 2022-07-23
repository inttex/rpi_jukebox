import os
import pickle
import subprocess
import time

from flask import request, url_for, redirect, make_response, current_app, Response
from flask_restful import Resource, abort
import requests
from sqlalchemy import exc
from requests_toolbelt import MultipartEncoder

from rpi_jukebox.api.database import db_session
from rpi_jukebox.api.models import Musics
from rpi_jukebox.utils import tools

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
        wavfile = element.wavfile
        response = make_response(wavfile)
        response.headers.set('Content-Type', 'audio/x-wav')
        response.headers.set('Content-Disposition', 'attachment')
        return response
        # with open('test', 'wb') as myfile:
            # myfile.write(wavfile)

    def delete(self, rfid):
        element = query_by_rfid(rfid)
        db_session.delete(element)
        db_session.commit()
        return '', 204

    def put(self, rfid):
        element = query_by_rfid(rfid)
        title = request.form['title']
        element.title = title
        wavfile = request.files['wavfile']
        x=wavfile.read()
        element.wavfile = x
        try:
            db_session.commit()
        except exc.SQLAlchemyError as e:
            abort(422, message=repr(e))
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
            wavfile = request.files['wavfile']
            title = wavfile.filename
            url = url_for('jukebox', _external=True) + '/{}'.format(rfid)
            data=MultipartEncoder(fields={'title': title, 'wavfile': ('wavfile', wavfile, 'text/plain')})
            r = requests.put(url, data=data, headers={'Content-Type': data.content_type})
            if r.status_code == 201:
                answer = redirect(url_for('home_page'))
            else:
                answer = r.text, r.status_code
            return answer

class Update(Resource):

    def get(self):
        subprocess.run('/root/bin/update_rpi_jukebox')
        return redirect(url_for('home_page'))

class APILog(Resource):

    def get(self):
        path = os.path.join(current_app.config['DATA_PATH'], 'api_errors')
        ti_m = os.path.getmtime(path)
        m_ti = time.ctime(ti_m)
        with open(path) as myfile:
            text = myfile.read()
        text = f'{m_ti}\n' + text
        return Response(text, mimetype='text/plain')

class ClientError(Resource):

    def get(self):
        path = os.path.join(current_app.config['DATA_PATH'], 'client_errors')
        ti_m = os.path.getmtime(path)
        m_ti = time.ctime(ti_m)
        with open(path) as myfile:
            text = myfile.read()
        text = f'{m_ti}\n' + text
        return Response(text, mimetype='text/plain')

class ClientLog(Resource):

    def get(self):
        with open(current_app.config['CLIENT_LOG_FILE']) as myfile:
            text = myfile.read()
        return Response(text, mimetype='text/plain')


class Parameters(Resource):

    def get(self, name):
        answer = current_app.config['PARAMETERS'][name]
        return answer

    def post(self, name):
        if name=='random_stop':
            new_value = not current_app.config['PARAMETERS'][name]
        else:
            old_value = current_app.config['PARAMETERS'][name]
            new_value = type(old_value)(request.form['new_value'])
        current_app.config['PARAMETERS'][name] = new_value
        tools.save_current_parameters(current_app.config['PARAMETERS'], current_app.config['LAST_PARAMETERS_FILE'])
        return redirect(url_for('home_page'))

if __name__=='__main__':
    main()
