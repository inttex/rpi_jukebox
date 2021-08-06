import os

from flask import Flask, render_template, url_for

def main():
    musics = {'123': 'titre1', '124': 'titre2'}
    html_content = index(musics)

    app = Flask(__name__)

    @app.route('/')
    def home_page():
        return html_content
    app.run(debug=True)

def index(musics):
        lines = list()
        for rfid, title in musics.items():
            html = str()
            html += '<p>'
            html +='{}: {}'.format(rfid, title)
            html += "<form method=get action=/unwrapper style='float: left;'>"
            html += "<input type='hidden' name='method' value='DELETE'/>"
            html += "<input type='hidden' name='rfid' value='{}'/>".format(rfid)
            html += "<input type='submit' value='DELETE'/>"
            html += "</form>"
            html += "<form method=post action=/unwrapper>"
            html += "<input type='hidden' name='method' value='PUT'/>"
            html += "<input type='hidden' name='rfid' value='{}'/>".format(rfid)
            html += "<input type='text' name='title'/>"
            html += "<input type='submit' value='PUT'/>"
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
