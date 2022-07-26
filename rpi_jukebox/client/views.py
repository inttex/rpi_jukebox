def main():
    print('ok')


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
        pass

    def wait_for_input(self):
        pass

    def play(self, sound):
        pass

    def stop(self):
        pass


if __name__ == '__main__':
    main()
