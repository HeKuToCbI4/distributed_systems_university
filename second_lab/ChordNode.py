from second_lab.Node import Node
from second_lab.settings import bit_count


class ChordNode:
    def __init__(self):
        self.node_list = []

        pass

    def get_first_node(self):
        return sorted(self.node_list, key=lambda x: x.node_id)[0] if len(self.node_list) > 0 else None

    def get_last_node(self):
        return sorted(self.node_list, key=lambda x: x.node_id)[-1] if len(self.node_list) > 0 else None

    def add_node(self, node: Node):
        if len(self.node_list) == 1:
            self.node_list[0].successor = node
            self.node_list[0].precessor = node
            node.successor = self.node_list[0]
            node.precessor = self.node_list[0]
        else:
            next_node: Node
            prev_node: Node
            next_node = next((x for x in self.node_list if x.node_id > node.node_id), None)
            if next_node is None:
                next_node = self.get_first_node()

            if next_node is not None:
                node.successor = next_node
                next_node.precessor = node

            prev_node = next((x for x in self.node_list if x.node_id < node.node_id), None)
            if prev_node is None:
                prev_node = self.get_last_node()

            if prev_node is not None:
                node.precessor = prev_node
                prev_node.successor = node

            for finger_table_key in node.precessor.finger_table.keys():
                if finger_table_key <= node.node_id:
                    node.precessor.finger_table[finger_table_key] = node

        self.node_list.append(node)
        for i in range(1, bit_count + 1):
            start = (node.node_id + 2 ** (i - 1)) % (2 ** bit_count)
            node.finger_table[start] = next((x for x in self.node_list if x.node_id >= start), self.node_list[0])

    def remove_node(self, node_id: int):
        node: Node
        node = next((x for x in self.node_list if x.node_id == node_id), None)
        if node is not None:
            node.successor.previous = node.precessor
            node.precessor.next = node.successor
            self.node_list.remove(node)
            for i in range(1, bit_count+1):
                start = (node.precessor.node_id + 2 ** (i - 1)) % (2 ** bit_count)
                node.precessor.finger_table[start] = next((x for x in self.node_list if x.node_id >= start),
                                                          self.node_list[0])

