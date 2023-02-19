import csv

from rpi_jukebox.spotybox.dataclasses import COMMAND


def get_commands() -> dict:
    commands_dict = {}
    with open('command_rfids.csv', 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for line in reader:
            commands_dict.update({line[0]: COMMAND[line[1].split('.')[1]]})
    return commands_dict


def main():
    get_commands()


if __name__ == '__main__':
    main()
