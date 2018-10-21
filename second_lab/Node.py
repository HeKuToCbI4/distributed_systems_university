from second_lab.settings import bit_count


class Node:
    def __init__(self, node_id: int):
        self.precessor = self
        self.node_id = node_id
        self.finger_table = {}
        for i in range(1, bit_count + 1):
            self.finger_table[(node_id + 2 ** (i - 1)) % (2 ** bit_count)] = None
        self.successor = self

    @property
    def successor(self):
        first_elem_key = list(self.finger_table.keys())[0]
        return self.finger_table[first_elem_key]

    @successor.setter
    def successor(self, value):
        first_elem_key = list(self.finger_table.keys())[0]
        self.finger_table[first_elem_key] = value

    def __str__(self):
        return f'NodeId: {self.node_id} | FingerTable: {self.finger_table}'

    def __repr__(self):
        return f'ChordNode with id: {self.node_id}'
