import logging


import simpleaudio


def main():
    view = JukeboxView()
    view.run()


class JukeboxView():

    def __init__(self):

        self.controller = None

    def set_controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """
        self.controller = controller

    def run(self):
        while True:
            rfid = self._wait_for_input()
            self.controller.process_rfid(rfid)

    def _wait_for_input(self):
        rfid = input('rfid?:\n')
        return rfid

    def play(self, seg):
        logging.info('play the music')
        simpleaudio.play_buffer(
                seg.raw_data,
                num_channels=seg.channels,
                bytes_per_sample=seg.sample_width,
                sample_rate=seg.frame_rate,
                )

    def stop(self):
        logging.info('music is stopped')
        simpleaudio.stop_all()


if __name__ == '__main__':
    main()
