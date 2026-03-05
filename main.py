from finite_automaton import FiniteAutomaton


def format_state(state):
    """Convert frozenset({'q1','q2'}) -> {q1,q2}"""
    if not state:
        return "-"
    return "{" + ",".join(sorted(state)) + "}"


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

    print("b) Determinism check\n")

    print("Original FA")
    print(f"{'State':15}", end="")
    for symbol in alphabet:
        print(f"{symbol:15}", end="")
    print()

    for state in states:

        state_name = state
        if state == start_state:
            state_name = "->" + state_name
        if state in final_states:
            state_name = "*" + state_name

        print(f"{state_name:15}", end="")

        for symbol in alphabet:
            next_state = transitions.get((state, symbol), None)

            if next_state:
                print(f"{list(next_state)!s:15}", end="")
            else:
                print(f"{'-':15}", end="")

        print()

    print("\nIs deterministic:", fa.is_deterministic())

    # ------------------ STRING TESTING ------------------

    print("\nSTRING TESTING\n")

    test_words = ["bc", "abc", "bbbc", "ac"]

    for word in test_words:
        result = fa.string_belongs_to_language(word)
        print(f"Test word '{word}': {result}")

    # ------------------ REGULAR GRAMMAR ------------------

    print("\nCONVERSION TO REGULAR GRAMMAR\n")

    grammar = fa.to_regular_grammar()
    grammar.print_productions()

    print("\nGrammar Classification:")
    print(grammar.classify())

    # ------------------ NDFA → DFA ------------------

    print("\nc) NDFA -> DFA conversion\n")

    dfa_states, dfa_transitions, dfa_start, dfa_finals = fa.to_dfa()

    print("DFA after subset construction")

    print(f"{'State':15}", end="")
    for symbol in alphabet:
        print(f"{symbol:15}", end="")
    print()

    for state in dfa_states:

        state_name = format_state(state)

        if state == dfa_start:
            state_name = "->" + state_name

        if state in dfa_finals:
            state_name = "*" + state_name

        print(f"{state_name:15}", end="")

        for symbol in alphabet:
            next_state = dfa_transitions.get((state, symbol), frozenset())
            formatted = format_state(next_state)

            if formatted != "-":
                formatted = "['" + formatted + "']"

            print(f"{formatted:15}", end="")

        print()

    print("\nIs deterministic: True")


if __name__ == "__main__":
    main()