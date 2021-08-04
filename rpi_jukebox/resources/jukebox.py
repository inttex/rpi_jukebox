import os
import pickle

from flask_restful import Resource

def main():
    print(musics)

LOCAL_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'db')
DB_FILENAME = os.path.join(LOCAL_DIRECTORY, 'musics.pickle')

try:
    with open(DB_FILENAME, 'rb') as myfile:
        musics = pickle.load(myfile)
except EOFError:
    print('last parameter file is probably empty..')
    musics = dict()
except IOError:
    print('could not access or find last parameter file')
    musics = dict()

# try:
    # with open(DB_FILENAME, 'wb') as myfile:
        # pickle.dump(musics, myfile)
# except IOError:
    # print('could not access or find last parameter file')

class Jukebox(Resource):
    def get(self):
        return musics

if __name__=='__main__':
    main()
