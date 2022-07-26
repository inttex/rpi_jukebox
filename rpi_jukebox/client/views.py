def main():
    view = JukeboxView()
    view._wait_for_input()


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
        print('TODO: loop the view')

    def _wait_for_input(self):
        rfid = input('rfid?:\n')
        return rfid

    def play(self, sound):
        print('play a sound')

    def stop(self):
        print('stop all sound playing')


if __name__ == '__main__':
    main()
