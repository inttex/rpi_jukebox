import os

def index(musics):
        lines = list()
        for rfid, title in musics.items():
            lines.append("<p> {}: {}</p>".format(rfid, title))
        lines.append("<form method=post action=/jukebox> <input type='text' name='rfid'/><input type='submit' value='post'/></form>")
        html_content = os.linesep.join(lines)
        return html_content
