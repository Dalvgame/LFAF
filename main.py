from grammar import Grammar
from cnf_converter import CNFConverter


def build_variant10():
    VN = {"S", "A", "B", "D"}
    VT = {"a", "b", "d"}

    P = {
        "S": [["d", "B"], ["A", "B"]],
        "A": [["d"], ["d", "S"], ["a", "A", "a", "A", "b"], []],  # ε
        "B": [["a"], ["a", "S"], ["A"]],
        "D": [["A", "b", "a"]],
    }

    return Grammar(VN, VT, P, "S")


if __name__ == "__main__":
    g = build_variant10()
    converter = CNFConverter()
    converter.to_cnf(g)