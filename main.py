from finite_automaton import FiniteAutomaton


def main():

    # Variant 10 definition
    states = {"q0", "q1", "q2", "q3"}
    alphabet = {"a", "b", "c"}

    transitions = {
        ("q0", "a"): {"q1"},
        ("q0", "b"): {"q2"},
        ("q1", "b"): {"q1", "q2"},  # nondeterminism
        ("q2", "c"): {"q3"},
        ("q3", "a"): {"q1"},
    }

    start_state = "q0"
    final_states = {"q3"}

    fa = FiniteAutomaton(states, alphabet, transitions, start_state, final_states)

    print("FINITE AUTOMATON ANALYSIS\n")

    print("Is Deterministic?")
    print(fa.is_deterministic())

    print("\nCONVERSION TO REGULAR GRAMMAR\n")

    grammar = fa.to_regular_grammar()
    grammar.print_productions()

    print("\nGrammar Classification:")
    print(grammar.classify())

    print("\nNDFA → DFA CONVERSION \n")

    dfa_states, dfa_transitions, dfa_start, dfa_finals = fa.to_dfa()

    print("DFA States:")
    for state in dfa_states:
        print(state)

    print("\nDFA Final States:")
    for state in dfa_finals:
        print(state)


if __name__ == "__main__":
    main()