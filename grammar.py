class Grammar:
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol

    def classify(self):
        """
        Classifies grammar according to Chomsky hierarchy.
        """

        is_regular = True
        is_context_free = True

        for left, rights in self.productions.items():

            # Context-Free condition:
            # left side must be single non-terminal
            if len(left) != 2 and left not in self.non_terminals:
                is_context_free = False
                is_regular = False

            for right in rights:

                if right == "ε":
                    continue

                # Regular grammar check (right-linear)
                if len(right) == 2:
                    if not (right[0] in self.terminals and right[1:] in self.non_terminals):
                        is_regular = False

                elif len(right) == 1:
                    if right not in self.terminals:
                        is_regular = False

                else:
                    is_regular = False

        if is_regular:
            return "Type 3 - Regular Grammar"
        elif is_context_free:
            return "Type 2 - Context-Free Grammar"
        else:
            return "Type 0/1 - More General Grammar"

    def print_productions(self):
        for left, rights in self.productions.items():
            print(left, "→", " | ".join(rights))