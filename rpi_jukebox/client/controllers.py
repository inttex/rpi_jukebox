import logging


def main():
    HOST = 'http://localhost:43210/'
    from rpi_jukebox.client.models import APICommunicator, MusicLoader
    from rpi_jukebox.client.views import JukeboxView
    apicommunicator = APICommunicator(HOST)
    musicloader = MusicLoader()
    view = JukeboxView()
    controller = JukeboxController(apicommunicator, musicloader, view)
    controller.process_rfid(1)


class JukeboxController():
    def __init__(self, apicommunicator, musicloader, view):
        self.apicommunicator = apicommunicator
        self.musicloader = musicloader
        self.view = view

    def process_rfid(self, rfid):
        if rfid is not None:
            self.view.stop()
            success = True
            if not rfid == self.musicloader.rfid:
                wav_file = self.apicommunicator.get_music_file(rfid)
                if wav_file is None:
                    success = False
            else:
                wav_file = None
            if success:
                self.musicloader.volume_increase_dB = self.apicommunicator.get_parameter('volume_increase_dB')
                if wav_file:
                    random_stop = self.apicommunicator.get_parameter('random_stop')
                    self.musicloader.random_stop = random_stop
                    if random_stop:
                        self.musicloader.tmin_ms = 1000 * self.apicommunicator.get_parameter('tmin')
                        self.musicloader.tmax_ms = 1000 * self.apicommunicator.get_parameter('tmax')
                sound = self.musicloader.get_sound(wav_file)
                duration = len(sound) /1000
                logging.info('the music will be stopped after %s', duration)
                self.view.play(sound)
                self.musicloader.rfid = rfid


if __name__ == '__main__':
    main()
