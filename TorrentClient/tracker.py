from TorrentClient.torrent_wrapper import TorrentWrapper
from TorrentClient.tracker_response import TrackerResponse
import random
from hashlib import sha1
import bencode
from urllib.parse import urlencode
import aiohttp
import requests


class Tracker:
    def __init__(self, filename):
        self.torrent = TorrentWrapper(filename)
        self.peer_id = '-PC0001-' + ''.join([str(random.randint(0, 9)) for _ in range(12)])
        print(bencode.bencode(self.torrent.info))
        self.info_hash = sha1(bencode.bencode(self.torrent.info)).digest()
        # self.http_client = aiohttp.ClientSession()

    @property
    def output_file(self):
        return self.torrent.name

    def connect(self, first=None, uploaded=0, downloaded=0):
        params = {
            'info_hash': self.info_hash,
            'peer_id': self.peer_id,
            'port': 6889,
            'uploaded': uploaded,
            'downloaded': downloaded,
            'left': self.torrent.size - downloaded,
            'compact': 1
        }
        if first:
            params['event'] = 'started'

        url = self.torrent.announce + '?' + urlencode(params)
        print(url)
        response = requests.get(url)
        # with self.http_client.get(url) as response:
        if not response.status_code == 200:
            raise ConnectionError('Failed to connect to tracker!')
        response_text = b''
        for x in response.iter_content():
            response_text += x
        return TrackerResponse(bencode.bdecode(response_text))

    def close(self):
        self.http_client.close()

    def _construct_params(self):
        return {
            'info_hash': self.info_hash,
            'peer_id': self.peer_id,
            'port': 6889,
            'uploaded': 0,
            'downloaded': 0,
            'left': 0,
            'compact': 1
        }

if __name__ == '__main__':
    tracker = Tracker('torrents/ubuntu18.torrent')
    print(tracker.connect())