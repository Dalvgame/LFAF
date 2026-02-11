from grammar import Grammar


if __name__ == "__main__":
    VN = {"S", "B", "L"}
    VT = {"a", "b", "c"}

    P = {
        "S": ["aB"],
        "B": ["bB", "cL"],
        "L": ["cL", "aS", "b"]
    }

    grammar = Grammar(VN, VT, P, "S")

    print("Generated strings:")
    for _ in range(5):
        print(grammar.generate_string())

    fa = grammar.to_finite_automaton()

    print("\nMembership tests:")
    test_strings = ["abcb", "abcccb", "acb", "abbbbbcaaab", "abbbbbcb"]
    for s in test_strings:
        print(s, "->", fa.string_belongs_to_language(s))
