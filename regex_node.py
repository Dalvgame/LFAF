import random

class RegexNode:
    pass


class LiteralNode(RegexNode):
    def __init__(self, value):
        self.value = value


class SequenceNode(RegexNode):
    def __init__(self):
        self.nodes = []


class AlternationNode(RegexNode):
    def __init__(self):
        self.options = []


class RepetitionNode(RegexNode):
    def __init__(self, node, min_rep, max_rep):
        self.node = node
        self.min = min_rep
        self.max = max_rep