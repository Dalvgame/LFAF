import random
from finite_automaton import FiniteAutomaton


class Grammar:
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol

    def generate_string(self):
        current_symbol = self.start_symbol
        result = ""

        while current_symbol in self.non_terminals:
            production = random.choice(self.productions[current_symbol])

            if len(production) == 1:
                result += production
                break
            else:
                result += production[0]
                current_symbol = production[1]

        return result

    def to_finite_automaton(self):
        states = set(self.non_terminals)
        alphabet = set(self.terminals)
        transitions = {}
        start_state = self.start_symbol
        final_states = {"q_final"}
        states.add("q_final")

        for non_terminal, rules in self.productions.items():
            for rule in rules:
                if len(rule) == 2:
                    symbol = rule[0]
                    next_state = rule[1]
                    transitions.setdefault((non_terminal, symbol), set()).add(next_state)
                elif len(rule) == 1:
                    symbol = rule
                    transitions.setdefault((non_terminal, symbol), set()).add("q_final")

        return FiniteAutomaton(states, alphabet, transitions, start_state, final_states)
