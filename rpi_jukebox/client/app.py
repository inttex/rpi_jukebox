def main():
    HOST = 'http://localhost:5000/'
    run_jukebox_client(HOST)


def run_jukebox_client(host):
    app = JukeboxApp(host)
    app.run()


class JukeboxApp():

    def __init__(self, host):
        print('TODO: initialize app')

    def run(self):
        print('TODO: run a loop for jukebox')


if __name__ == '__main__':
    main()
