from collections import defaultdict, deque
from copy import deepcopy
from grammar import Grammar


class CNFConverter:
    def __init__(self):
        self.counter = 0

    def to_cnf(self, g):
        print("ORIGINAL GRAMMAR\n", g, "\n")

        g1 = self.remove_epsilon(g)
        print("STEP 1: Eliminate ε-productions\n", g1, "\n")

        g2 = self.remove_unit(g1)
        print("STEP 2: Eliminate renaming rules\n", g2, "\n")

        g3 = self.remove_inaccessible(g2)
        print("STEP 3: Eliminate inaccessible symbols\n", g3, "\n")

        g4 = self.remove_non_productive(g3)
        print("STEP 4: Eliminate non-productive symbols\n", g4, "\n")

        g5 = self.to_proper_cnf(g4)
        print("STEP 5: Chomsky Normal Form\n", g5, "\n")

        return g5

    # -----------------------------
    # STEP 1: ε-productions
    # -----------------------------
    def remove_epsilon(self, g):
        nullable = set()

        changed = True
        while changed:
            changed = False
            for A, rules in g.P.items():
                for rhs in rules:
                    if not rhs or all(x in nullable for x in rhs):
                        if A not in nullable:
                            nullable.add(A)
                            changed = True

        newP = defaultdict(set)

        for A, rules in g.P.items():
            for rhs in rules:
                variants = self.expand_nullable(rhs, nullable)
                for v in variants:
                    if v:
                        newP[A].add(tuple(v))

        if g.S in nullable:
            newP[g.S].add(tuple())

        return Grammar(g.VN, g.VT, {k: list(v) for k, v in newP.items()}, g.S)

    def expand_nullable(self, rhs, nullable):
        result = set()
        n = len(rhs)

        for mask in range(1 << n):
            new = []
            valid = True
            for i in range(n):
                if mask & (1 << i):
                    if rhs[i] not in nullable:
                        valid = False
                        break
                else:
                    new.append(rhs[i])
            if valid:
                result.add(tuple(new))

        return result

    # -----------------------------
    # STEP 2: unit rules
    # -----------------------------
    def remove_unit(self, g):
        newP = defaultdict(set)

        for A in g.VN:
            closure = self.unit_closure(A, g)
            for B in closure:
                for rhs in g.P.get(B, []):
                    if not (len(rhs) == 1 and rhs[0] in g.VN):
                        newP[A].add(tuple(rhs))

        return Grammar(g.VN, g.VT, {k: list(v) for k, v in newP.items()}, g.S)

    def unit_closure(self, A, g):
        visited = set()
        queue = deque([A])

        while queue:
            x = queue.popleft()
            if x in visited:
                continue
            visited.add(x)

            for rhs in g.P.get(x, []):
                if len(rhs) == 1 and rhs[0] in g.VN:
                    queue.append(rhs[0])

        return visited

    # -----------------------------
    # STEP 3: inaccessible
    # -----------------------------
    def remove_inaccessible(self, g):
        reachable = set()
        queue = deque([g.S])

        while queue:
            A = queue.popleft()
            if A in reachable:
                continue
            reachable.add(A)

            for rhs in g.P.get(A, []):
                for x in rhs:
                    if x in g.VN:
                        queue.append(x)

        newP = {A: g.P[A] for A in reachable if A in g.P}
        return Grammar(reachable, g.VT, newP, g.S)

    # -----------------------------
    # STEP 4: non-productive
    # -----------------------------
    def remove_non_productive(self, g):
        productive = set(g.VT)

        changed = True
        while changed:
            changed = False
            for A, rules in g.P.items():
                for rhs in rules:
                    if all(x in productive for x in rhs):
                        if A not in productive:
                            productive.add(A)
                            changed = True

        newVN = {x for x in g.VN if x in productive}
        newP = {}

        for A in newVN:
            valid = []
            for rhs in g.P.get(A, []):
                if all(x in productive for x in rhs):
                    valid.append(rhs)
            if valid:
                newP[A] = valid

        return Grammar(newVN, g.VT, newP, g.S)

    # -----------------------------
    # STEP 5: CNF
    # -----------------------------
    def to_proper_cnf(self, g):
        VN = set(g.VN)
        VT = set(g.VT)
        P = deepcopy(g.P)

        term_map = {}

        for A in list(P.keys()):
            new_rules = []
            for rhs in P[A]:
                if len(rhs) <= 1:
                    new_rules.append(rhs)
                    continue

                new_rhs = []
                for x in rhs:
                    if x in VT:
                        if x not in term_map:
                            new_nt = f"T_{x.upper()}{self.counter}"
                            self.counter += 1
                            VN.add(new_nt)
                            term_map[x] = new_nt
                        new_rhs.append(term_map[x])
                    else:
                        new_rhs.append(x)

                new_rules.append(new_rhs)

            P[A] = new_rules

        for t, nt in term_map.items():
            P[nt] = [[t]]

        newP = defaultdict(list)

        for A, rules in P.items():
            for rhs in rules:
                while len(rhs) > 2:
                    new_nt = f"X{self.counter}"
                    self.counter += 1
                    VN.add(new_nt)

                    newP[A].append([rhs[0], new_nt])
                    rhs = rhs[1:]
                    A = new_nt

                newP[A].append(rhs)

        return Grammar(VN, VT, dict(newP), g.S)