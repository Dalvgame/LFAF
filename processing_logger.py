import random
from regex_parser import RegexParser
from regex_node import *

class ProcessingLogger:

    @staticmethod
    def explain_node(node, steps, level=0):
        indent = "  " * level

        if isinstance(node, LiteralNode):
            steps.append(f"{indent}Literal: '{node.value}'")

        elif isinstance(node, SequenceNode):
            steps.append(f"{indent}Sequence start")
            for child in node.nodes:
                ProcessingLogger.explain_node(child, steps, level + 1)
            steps.append(f"{indent}Sequence end")

        elif isinstance(node, AlternationNode):
            steps.append(f"{indent}Alternation start")
            chosen = random.choice(node.options)
            ProcessingLogger.explain_node(chosen, steps, level + 1)
            steps.append(f"{indent}Alternation end")

        elif isinstance(node, RepetitionNode):
            count = random.randint(node.min, node.max)
            steps.append(f"{indent}Repeat {count} times")
            for _ in range(count):
                ProcessingLogger.explain_node(node.node, steps, level + 1)
            steps.append(f"{indent}End repeat")

    @staticmethod
    def explain(regex):
        parser = RegexParser(regex)
        root = parser.parse()

        steps = [f"Processing regex: {regex}"]
        ProcessingLogger.explain_node(root, steps)

        return steps