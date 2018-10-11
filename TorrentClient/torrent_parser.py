from collections import OrderedDict

INT_TOKEN = b'i'
LIST_TOKEN = b'l'
DICT_TOKEN = b'd'
END_TOKEN = b'e'
SEP_TOKEN = b':'

class Parser:
    def __init__(self, data: bytes):
        # Initialize parser object.
        if not isinstance(data, bytes):
            raise ValueError("Data must be bytes.")
        self._data = data
        self._index = 0

    def parse(self):
        # Decode bytes and return python object.
        c = self._peek()
