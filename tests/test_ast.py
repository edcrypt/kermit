from kermit.ast import Node


class Other(Node):

    def __init__(self, a=None, b=None):
        self.a = a
        self.b = b


def test_node_equality():
    assert Node() == Node()
    assert Other(1, 2) == Other(1, 2)


def test_node_inequality():
    assert Node() != Other()
    assert Other(1, 2) != Other(3, 4)
