class Grammar:
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        self.VN = set(non_terminals)
        self.VT = set(terminals)
        self.P = {k: [list(rhs) for rhs in v] for k, v in productions.items()}
        self.S = start_symbol

    def get_non_terminals(self):
        return self.VN

    def get_terminals(self):
        return self.VT

    def get_productions(self):
        return self.P

    def get_start_symbol(self):
        return self.S

    def __str__(self):
        result = []
        result.append(f"V_N = {self.VN}")
        result.append(f"V_T = {self.VT}")
        result.append(f"S   = {self.S}")
        result.append("P:")

        for lhs, rules in self.P.items():
            for rhs in rules:
                if not rhs:
                    result.append(f"  {lhs} -> ε")
                else:
                    result.append(f"  {lhs} -> {' '.join(rhs)}")

        return "\n".join(result)