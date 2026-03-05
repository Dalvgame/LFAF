from collections import defaultdict


class FiniteAutomaton:

    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states

    def is_deterministic(self):
        """
        A FA is deterministic if every (state, symbol)
        leads to at most one next state.
        """
        for (state, symbol), next_states in self.transitions.items():
            if len(next_states) > 1:
                return False
        return True

    def string_belongs_to_language(self, word):
        """
        Simulates the automaton (works for NDFA).
        Returns True if the word is accepted.
        """
        current_states = {self.start_state}

        for symbol in word:

            next_states = set()

            for state in current_states:

                if (state, symbol) in self.transitions:
                    next_states.update(self.transitions[(state, symbol)])

            current_states = next_states

            if not current_states:
                return False

        return any(state in self.final_states for state in current_states)

    def to_regular_grammar(self):
        """
        Converts FA to right-linear grammar.
        """
        from grammar import Grammar

        productions = defaultdict(list)

        for (state, symbol), next_states in self.transitions.items():

            for next_state in next_states:

                productions[state].append(symbol + next_state)

        for final_state in self.final_states:

            productions[final_state].append("ε")

        return Grammar(
            non_terminals=self.states,
            terminals=self.alphabet,
            productions=productions,
            start_symbol=self.start_state
        )

    def to_dfa(self):
        """
        Subset construction algorithm.
        Converts NDFA to DFA.
        """

        dfa_states = []
        dfa_transitions = {}
        dfa_final_states = []

        start = frozenset([self.start_state])

        unprocessed = [start]

        dfa_states.append(start)

        while unprocessed:

            current = unprocessed.pop()

            for symbol in self.alphabet:

                next_set = set()

                for state in current:

                    if (state, symbol) in self.transitions:

                        next_set.update(self.transitions[(state, symbol)])

                next_frozen = frozenset(next_set)

                dfa_transitions[(current, symbol)] = next_frozen

                if next_frozen not in dfa_states:

                    dfa_states.append(next_frozen)

                    unprocessed.append(next_frozen)

        for state_set in dfa_states:

            if any(state in self.final_states for state in state_set):

                dfa_final_states.append(state_set)

        return dfa_states, dfa_transitions, start, dfa_final_states