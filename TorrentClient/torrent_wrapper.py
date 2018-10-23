import bencode


class TorrentWrapper:
    def __init__(self, filename):
        data_file = None
        try:
            data_file = open(filename, 'rb')
        except FileNotFoundError:
            print(f'Error opening {filename}, file does not exist')
        if data_file is not None:
            data = data_file.read()
            self.parsed_data = bencode.bdecode(data)
            self.announce = self.parsed_data['announce']
            self.announce_list = self.parsed_data['announce-list']
            self.comment = self.parsed_data['comment']
            self.create_date = self.parsed_data['creation date']
            self.info = self.parsed_data['info']
            if 'length' in self.parsed_data['info'].keys():
                self.size = self.parsed_data['info']['length']
            else:
                self.size = 0
            if 'name' in self.parsed_data['info'].keys():
                self.name = self.parsed_data['info']['name']
            if 'piece length' in self.parsed_data['info'].keys():
                self.piece_length = self.parsed_data['info']['piece length']
            if 'pieces' in self.parsed_data['info'].keys():
                self.pieces = self.parsed_data['info']['pieces']

    def __repr__(self):
        return f'{self.name} torrent file data wrapper.'

    def __str__(self):
        return self.__repr__() + f' {self.comment}'


if __name__ == '__main__':
    torrent = TorrentWrapper('torrents/ubuntu18.torrent')
    print(torrent)
