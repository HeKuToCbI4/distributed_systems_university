from second_lab.settings import bit_count


class Node:
    def __init__(self, node_id: int):
        self.predcessor = self
        self.successor = self
        self.node_id = node_id
        self.finger_table = {}
        for i in range(1, bit_count):
            self.finger_table[(node_id + 2 ** (i - 1)) % (2 ** bit_count)] = None
