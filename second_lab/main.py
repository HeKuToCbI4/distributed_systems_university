from second_lab.ChordNode import ChordNode
from second_lab.Node import Node
bit_count = 8
from time import sleep
if __name__ == '__main__':
    ChordNode = ChordNode()
    ChordNode.add_node(Node(1))
    ChordNode.add_node(Node(3))
    ChordNode.add_node(Node(5))
    # ChordNode.add_node(Node(4))
    # ChordNode.add_node(Node(6))
    ChordNode.remove_node(3)
    for node in ChordNode.node_list:
        print(node)

