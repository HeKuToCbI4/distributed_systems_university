import socket
from TorrentClient.tracker import Tracker
import re
import os
import shutil
import threading
import datetime

handshake_pattern = b"\x13BitTorrent protocol.{8}(.{20})(-.{6}-.{12})"


class TorrentClient:
    def __init__(self, torrent):
        self.tracker = Tracker(torrent)
        tracker_response = self.tracker.connect()
        self.peers = tracker_response.peers
        self.peer_id = self.tracker.peer_id
        self.log_directory = self.tracker.torrent.name
        if os.path.exists(self.log_directory):
            shutil.rmtree(self.log_directory)
        os.mkdir(self.log_directory)
        self.thread_pool = []

    def tcp_peer_connection(self, peer):
        # Attempt connection
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        network_info_string = f'{peer[0]}_{peer[1]}'
        current_peer_info_file = open(os.path.join(self.log_directory, f'{network_info_string}.txt'), 'wb+')
        bitfield_data = b''
        try:
            peer_socket.connect(peer)
            current_peer_info_file.write(bytes(f'Connected to {network_info_string}', encoding='utf-8'))
            # Handshake
            handshake_message = bytes(chr(19) + 'BitTorrent protocol' + 8 * chr(0),
                                      encoding='utf-8') + self.tracker.info_hash + bytes(self.peer_id, encoding='utf-8')
            peer_socket.send(handshake_message)
            handshake_data = peer_socket.recv(4096)
            reg_match = re.match(handshake_pattern, handshake_data)
            assert reg_match is not None
            remote_hash = reg_match.group(1)
            remote_peer_id = reg_match.group(2)
            assert remote_hash == self.tracker.info_hash
            # Log info.
            current_peer_info_file.write(bytes(f'Connected successfully to {network_info_string}.\n', encoding='utf-8'))
            current_peer_info_file.write(bytes(f'Remote peer id: {remote_peer_id}.\n', encoding='utf-8'))
            current_peer_info_file.write(bytes('Remote and local hash matches.\n', encoding='utf-8'))
            current_peer_info_file.write(bytes(f'Remote peer handshake message: {handshake_data}\n', encoding='utf-8'))
            # Try get bitfield message
            now = datetime.datetime.now()
            peer_socket.settimeout(5)
            while datetime.datetime.now() <= now + datetime.timedelta(seconds=15):
                bitfield_data_chunk = peer_socket.recv(2048)
                if bitfield_data_chunk is not None:
                    bitfield_data += bitfield_data_chunk
                else:
                    break
        except BaseException as e:
            current_peer_info_file.write(bytes(f'Failure occurred {e}', encoding='utf-8'))
        finally:
            if bitfield_data != b'':
                current_peer_info_file.write(
                    bytes('Received BitField data message from remote peer \\/\n', encoding='utf-8'))
                current_peer_info_file.write(bitfield_data)
            else:
                current_peer_info_file.write(
                    bytes('BitField message was not received from remote peer.\n', encoding='utf-8'))
            current_peer_info_file.close()

    def multithreaded_peer_connection(self):
        for peer in self.peers:
            self.thread_pool.append(threading.Thread(target=self.tcp_peer_connection, args=(peer,)))
            self.thread_pool[-1].daemon = True
        for thread in self.thread_pool:
            thread.start()
        for thread in self.thread_pool:
            thread.join()


if __name__ == '__main__':
    client = TorrentClient('torrents/ubuntu18.torrent')
    client.multithreaded_peer_connection()
