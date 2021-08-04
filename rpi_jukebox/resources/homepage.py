import os

def index(musics):
        lines = list()
        for rfid, title in musics.items():
            lines.append("<p> {}: {}</p>".format(rfid, title))
        html_content = os.linesep.join(lines)
        return html_content
