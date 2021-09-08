import os

from flask import Flask, render_template, url_for

from rpi_jukebox.api.database import db_session
from rpi_jukebox.api.models import Musics

def main():
    musics = {'123': 'titre1', '124': 'titre2'}
    html_content = index(musics)

    app = Flask(__name__)

    @app.route('/')
    def home_page():
        return html_content
    app.run(debug=True)

def index():
        lines = list()
        musics = Musics.query.all()
        for elements in musics:
            rfid = elements.rfid
            title = elements.title
            html = str()
            html += '<p>'
            html += "<form method=get action=/unwrapper style='width=200px; display:inline-block;'>"
            html +="<label>{}: {}</label>".format(rfid, title)
            html += "<input type='hidden' name='method' value='DELETE'/>"
            html += "<input type='hidden' name='rfid' value='{}'/>".format(rfid)
            html += "<input type='submit' value='DELETE'/>"
            html += "</form>"
            html += "<form method=post action=/unwrapper enctype='multipart/form-data' style='width=200px; display:inline-block;'>"
            html += "<input type='hidden' name='method' value='PUT'/>"
            html += "<input type='hidden' name='rfid' value='{}'/>".format(rfid)
            html += "<input type='file' name='wavfile'/>"
            html += "<input type='submit' value='PUT'/>"
            html += "</form>"
            html += "<form method=get action=/jukebox/{} style='width=200px; display:inline-block;'>".format(rfid)
            html += "<input type='submit' value='GET'/>"
            html += "</form>"
            html += '</p>'
            lines.append(html)
        html = str()
        html += "<form method=post action=/jukebox>"
        html += '<p>'
        html += '<label>rfid no</label> : '
        html += "<input type='text' name='rfid'/>"
        html += "<input type='submit' value='NEW'/>"
        html += '</p>'
        html += "</form>"
        lines.append(html)
        html_content = os.linesep.join(lines)
        return html_content

if __name__=='__main__':
    main()
