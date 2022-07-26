def main():
    from rpi_jukebox.client.models import APICommunicator, MusicLoader
    from rpi_jukebox.client.views import JukeboxView
    apicommunicator = APICommunicator()
    musicloader = MusicLoader()
    view = JukeboxView()
    controller = JukeboxController(apicommunicator, musicloader, view)
    print(dir(controller))


class JukeboxController():
    def __init__(self, apicommunicator, musicloader, view):
        self.apicommunicator = apicommunicator
        self.musicloader = musicloader
        self.view = view


if __name__ == '__main__':
    main()
