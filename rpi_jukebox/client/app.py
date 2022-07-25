def main():
    run_jukebox_client()

def run_jukebox_client():
    app = JukeboxApp()
    app.run()

class JukeboxApp():

    def __init__(self):
        print('TODO: initialize app')

    def run(self):
        print('TODO: run a loop for jukebox')

if __name__=='__main__':
    main()
