import qbittorrent as bt
import time
import sys

torrent_path = 'torrents/ubuntu18.torrent'

if __name__ == '__main__':
    client = bt.Client('http://127.0.0.1:8080/')
    client.login()
    client.download_from_file(open(torrent_path, 'rb'), label='ubuntu')
    time.sleep(2)
    print(client.torrents())
    while client.torrents()[0]['amount_left'] != 0:
        i = client.torrents()[0]['downloaded'] / client.torrents()[0]['size'] * 100
        sys.stdout.write('\r')
        # the exact output you're looking for:
        sys.stdout.write("[%-100s] %f%%" % ('=' * int(i), i))
        sys.stdout.flush()
        time.sleep(0.25)
    client.logout()
