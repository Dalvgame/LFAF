import random
from regex_node import LiteralNode, SequenceNode, AlternationNode, RepetitionNode


class Generator:

    def generate(self, node):
        # Literal node → just return the character
        if isinstance(node, LiteralNode):
            return node.value

        # Sequence → concatenate all parts
        elif isinstance(node, SequenceNode):
            result = ""
            for n in node.nodes:
                result += self.generate(n)
            return result

        # Alternation → randomly pick one option
        elif isinstance(node, AlternationNode):
            chosen = random.choice(node.options)
            return self.generate(chosen)

        # Repetition → repeat node between min and max times
        elif isinstance(node, RepetitionNode):
            count = random.randint(node.min, node.max)

            result = ""
            for i in range(count):   # explicit loop (fixes warning)
                result += self.generate(node.node)

            return result

        # fallback (should not happen)
        return ""