import socket
from struct import unpack


class TrackerResponse:
    def __init__(self, response: dict):
        self.response = response

    @property
    def failure(self):
        if 'failure_reason' in self.response:
            return self.response['failure_reason']
        return None

    @property
    def interval(self) -> int:
        return self.response.get('interval', 0)

    @property
    def complete(self):
        return self.response.get('complete', 0)

    @property
    def incomplete(self):
        return self.response.get('incomplete', 0)

    @property
    def peers(self):
        print(self.response)
        peers = self.response['peers']
        if type(peers) == list:
            raise NotImplementedError
        peers = [peers[i:i + 6] for i in range(0, len(peers), 6)]
        return [(socket.inet_ntoa(p[:4]), unpack('>H', p[4:])[0]) for p in peers]

    def __repr__(self):
        return f'interval: {self.interval}\ncomplete: {self.complete}\n' \
               f'incomplete: {self.incomplete}\npeers: {self.peers}'

    def __str__(self):
        return self.__repr__()
