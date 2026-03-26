from regex_node import *

class RegexParser:

    def __init__(self, regex):
        self.regex = regex
        self.index = 0

    def parse(self):
        return self.parse_sequence()

    def parse_sequence(self):
        sequence = SequenceNode()

        while self.index < len(self.regex) and self.regex[self.index] != ')':
            sequence.nodes.append(self.parse_element())

        return sequence.nodes[0] if len(sequence.nodes) == 1 else sequence

    def parse_element(self):
        if self.regex[self.index] == '(':
            self.index += 1
            node = self.parse_alternation()
            self.index += 1
        else:
            node = LiteralNode(self.regex[self.index])
            self.index += 1

        return self.apply_quantifier(node)

    def parse_alternation(self):
        alt = AlternationNode()
        options = []
        current = ""
        balance = 0

        while self.index < len(self.regex):
            c = self.regex[self.index]

            if c == '(':
                balance += 1
            elif c == ')':
                if balance == 0:
                    break
                balance -= 1

            if c == '|' and balance == 0:
                options.append(current)
                current = ""
            else:
                current += c

            self.index += 1

        options.append(current)

        for opt in options:
            parser = RegexParser(opt)
            alt.options.append(parser.parse_sequence())

        return alt.options[0] if len(alt.options) == 1 else alt

    def apply_quantifier(self, node):
        if self.index >= len(self.regex):
            return node

        c = self.regex[self.index]

        if c == '*':
            self.index += 1
            return RepetitionNode(node, 0, 5)

        if c == '+':
            self.index += 1
            return RepetitionNode(node, 1, 5)

        if c == '?':
            self.index += 1
            return RepetitionNode(node, 0, 1)

        if c == '{':
            self.index += 1
            num = 0
            while self.regex[self.index].isdigit():
                num = num * 10 + int(self.regex[self.index])
                self.index += 1
            self.index += 1
            return RepetitionNode(node, num, num)

        return node