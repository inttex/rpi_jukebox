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
            html += "<form method=get action=/unwrapper>"
            html += '<p>'
            html +='{}: {}'.format(rfid, title)
            html += "<input type='hidden' name='method' value='DELETE'/>"
            html += "<input type='hidden' name='rfid' value='{}'/>".format(rfid)
            html += "<input type='submit' value='DELETE'/>"
            html += "</form>"
            html += '</p>'
            lines.append(html)
        lines.append("<form method=post action=/jukebox> <input type='text' name='rfid'/><input type='submit' value='post'/></form>")
        html_content = os.linesep.join(lines)
        return html_content

if __name__=='__main__':
    main()
