import asyncio
import logging
import math
import os
import time
from asyncio import Queue
from collections import namedtuple
from hashlib import sha1
from TorrentClient.tracker import Tracker

class TorrentClient:
    def __init__(self, torrent):
        self.tracker = Tracker(torrent)
        # The list of potential peers is the work queue, consumed by the
        # PeerConnections
        self.available_peers = Queue()
        # The list of peers is the list of workers that *might* be connected
        # to a peer. Else they are waiting to consume new remote peers from
        # the `available_peers` queue. These are our workers!
        self.peers = []
        # The piece manager implements the strategy on which pieces to
        # request, as well as the logic to persist received pieces to disk.
        self.piece_manager = PieceManager(torrent)
        self.abort = False