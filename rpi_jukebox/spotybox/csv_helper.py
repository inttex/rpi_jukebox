import csv
from pprint import pprint

from rpi_jukebox.spotify_client.data_structs import Sp_Music, SpType, ReplayType
from rpi_jukebox.spotybox.dataclasses import COMMAND


def get_commands() -> dict:
    commands_dict = {}
    with open('command_rfids.csv', 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for line in reader:
            commands_dict.update({int(line[0]): COMMAND[line[1].split('.')[1]]})
    return commands_dict


def get_collection():
    # read from csv
    # to pandas?

    collection_dict = {}
    with open('collection.csv', 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for line in reader:
            entry = Sp_Music(rfid=int(line[0]),
                             title=line[1],
                             sp_link=line[2],
                             sp_type=SpType[line[3]],
                             replay_type=ReplayType[line[4]],
                             last_played_song=line[5])
            collection_dict.update({int(line[0]): entry})
    return collection_dict


def write_collection(collection):
    with open('collection.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        for entry in collection.values():
            entry: Sp_Music
            writer.writerow((entry.rfid, entry.title, entry.sp_link, entry.sp_type.name, entry.replay_type.name,
                             entry.last_played_song))


def main():
    # get_commands()
    collection = get_collection()
    pprint(collection)


if __name__ == '__main__':
    main()
