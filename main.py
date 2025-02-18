import qbittorrentapi
import argparse
import os


def createClient(host: str, port: int, username: str, password: str):
    qbt = qbittorrentapi.Client(
        host=host,
        port=port,
        username=username,
        password=password
    )

    try:
        qbt.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)

    return qbt


def addTorrentURL(qbt: qbittorrentapi.Client, torrent_url: str, save_path: str):
    return qbt.torrents.add(
        urls=torrent_url,
        save_path=save_path
    ) == 'Ok.'


def addTorrentFile(qbt: qbittorrentapi.Client, torrent_path: str, save_path: str):
    return qbt.torrents.add(
        torrent_files=torrent_path,
        save_path=save_path
    ) == 'Ok.'


def getTorrents(qbt: qbittorrentapi.Client):
    return qbt.torrents_info()


if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('-d', '--directory', type=str, required=False)
    argument_parser.add_argument('-u', '--url', type=str, required=False)
    argument_parser.add_argument('-o', '--output', type=str)
    args = argument_parser.parse_args()

    qbt = createClient('localhost', 1230, 'simonfalke', 'simonfalkeadmin')

    # add all torrents in the directory
    if args.directory:
        for torrent in os.listdir(args.directory):
            addTorrentFile(qbt, args.directory + '/' + torrent, args.output)

    print(getTorrents(qbt))
