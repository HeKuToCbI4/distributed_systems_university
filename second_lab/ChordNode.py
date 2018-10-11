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
            self.node_list[0].next = node
            self.node_list[0].previous = node
            node.successor = self.node_list[0]
            node.predcessor = self.node_list[0]
        else:
            next_node: Node
            prev_node: Node
            next_node = next((x for x in self.node_list if x.node_id > node.node_id), None)
            if next_node == None:
                next_node = self.get_first_node()

            if next_node is not None:
                node.successor = next_node
                next_node.predcessor = node

            prev_node = next((x for x in self.node_list if x.node_id < node.node_id), None)
            if prev_node == None:
                prev_node = self.get_last_node()

            if prev_node is not None:
                node.predcessor = prev_node
                prev_node.successor = node

            change_list = []
            for x in node.predcessor.data_tuple_list:
                if x[0] >= node.node_id:
                    change_list.append(x)
            for x in change_list:
                if x in node.predcessor.data_tuple_list:
                    node.predcessor.data_tuple_list.remove(x)
        self.node_list.append(node)
        for i in range(1, bit_count):
            start = (node.node_id + 2 ** (i - 1)) % (2 ** bit_count)
            node.finger_table[start] = next((x for x in self.node_list if x.node_id >= start), self.node_list[0])

    def remove_node(self, node_id: int):
        node: Node
        node = next((x for x in self.node_list if x.node_id == node_id), None)
        if node is not None:
            node.successor.previous = node.predcessor
            node.predcessor.next = node.successor
            for i in range(1, bit_count):
                start = (node.predcessor.node_id + 2 ** (i - 1)) % (2**bit_count)
                node.predcessor.finger_table[start] = next((x for x in self.node_list if x.node_id >= start),
                                                           self.node_list[0])
            self.node_list.remove(node)

