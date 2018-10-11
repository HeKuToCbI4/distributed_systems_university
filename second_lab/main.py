from second_lab.ChordNode import ChordNode
from second_lab.Node import Node
bit_count = 8
from time import sleep
if __name__ == '__main__':
    ChordNode = ChordNode()
    ChordNode.add_node(Node(11))
    #ChordNode.add_tuple(15, 'Test data.')
    ChordNode.add_node(Node(20))
    ChordNode.add_node(Node(17))
    ChordNode.add_node(Node(13))
    ChordNode.add_node(Node(70))

    print(ChordNode.node_list)
    for node in ChordNode.node_list:
        print(node.data_tuple_list, node.node_id)
    ChordNode.remove_node(17)
    for node in ChordNode.node_list:
        print(node.tuple_list, node.node_id)

