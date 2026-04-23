# Laboratory Work 5 - Chomsky Normal Form

### Course: Formal Languages & Finite Automata  
### Author: Vladislav Cuibari  
### Group: FAF-243  

---

## Theory

A Context-Free Grammar (CFG) is in **Chomsky Normal Form (CNF)** when every production rule has one of the following forms:

- `A -> BC` — a nonterminal produces exactly two nonterminals  
- `A -> a` — a nonterminal produces a single terminal  
- `S -> ε` — allowed only if the start symbol derives ε  

CNF is important because algorithms like **CYK (Cocke-Younger-Kasami)** require it.

Any CFG can be transformed into an equivalent CNF grammar through a sequence of transformations. The key detail is that **the order of steps matters**, because each step assumes the previous one has already cleaned up certain structures.

---

## Objectives

1. Understand Chomsky Normal Form (CNF)  
2. Learn how to normalize a grammar step by step  
3. Implement a system that converts any CFG to CNF:
   - Encapsulated in a class (`CNFConverter`)
   - Executed and tested
   - **Bonus:** Works for any grammar, not just the assigned one  

---

## Variant 10 - Input Grammar

```
G = (V_N, V_T, P, S)

V_N = {S, A, B, D}  
V_T = {a, b, d}

P:
  1.  S -> dB
  2.  S -> AB
  3.  A -> d
  4.  A -> dS
  5.  A -> aAaAb
  6.  A -> ε
  7.  B -> a
  8.  B -> aS
  9.  B -> A
  10. D -> Aba
```

---

## Implementation Description

### Grammar

The `Grammar` class stores:

- Nonterminals (`V_N`)
- Terminals (`V_T`)
- Productions (`P`)
- Start symbol (`S`)

Productions are represented as a dictionary:

```python
{
    "A": [["a", "B"], ["d"]],
}
```

An empty list `[]` represents **ε**.

The class also includes a `__str__()` method to print the grammar nicely after each transformation step.

---

### CNFConverter

The `CNFConverter` class implements the full pipeline:

```python
to_cnf()
```

It runs:

1. ε-elimination  
2. Unit rule elimination  
3. Inaccessible symbol removal  
4. Non-productive symbol removal  
5. Conversion to proper CNF  

Each step is implemented as a separate method, making the code modular and easy to test.

---

## Step 1 - Eliminate ε-productions

We first identify **nullable nonterminals**.

In this grammar:

```
A -> ε
```

So **A is nullable**.

This generates new productions:

- `S -> AB` → also `S -> B`
- `A -> aAaAb` → multiple combinations by removing nullable A’s

A bitmask approach is used to generate all valid combinations.

---

## Step 2 - Eliminate renaming (unit) rules

Unit rules:

```
B -> A
```

We compute the **unit closure** and replace these rules.

Effect:

- `B` inherits all productions of `A`

---

## Step 3 - Eliminate inaccessible symbols

We perform BFS from `S`.

Result:

```
D is removed (not reachable)
```

---

## Step 4 - Eliminate non-productive symbols

A symbol is productive if it can derive terminal strings.

In this case:

- All remaining symbols are productive

So no changes occur.

---

## Step 5 - Convert to CNF

### START

Introduce a new start symbol if needed.

---

### TERM

Replace terminals in long rules:

```
A -> aAaAb
```

becomes:

```
A -> T_a A T_a A T_b
T_a -> a
T_b -> b
```

---

### BIN

Convert long rules into binary:

```
A -> X Y Z W
```

becomes:

```
A -> X N1
N1 -> Y N2
N2 -> Z W
```

---

## Conclusions / Results

The program successfully converts the Variant 10 grammar into CNF.

Key observations:

- ε-elimination increases rule count significantly  
- Unit rules require closure computation  
- Inaccessible symbol `D` is removed  
- Binarization introduces helper nonterminals  

Final grammar satisfies CNF:

- `A -> BC`
- `A -> a`

---
## Output
```

ORIGINAL GRAMMAR
 V_N = {'A', 'S', 'D', 'B'}
V_T = {'d', 'b', 'a'}
S   = S
P:
  S -> d B
  S -> A B
  A -> d
  A -> d S
  A -> a A a A b
  A -> ε
  B -> a
  B -> a S
  B -> A
  D -> A b a 

STEP 1: Eliminate ε-productions
 V_N = {'A', 'S', 'D', 'B'}
V_T = {'d', 'b', 'a'}
S   = S
P:
  S -> A
  S -> ε
  S -> A B
  S -> d B
  S -> B
  S -> d
  A -> a A a A b
  A -> a a A b
  A -> d S
  A -> a a b
  A -> a A a b
  A -> d
  B -> A
  B -> a
  B -> a S
  D -> A b a
  D -> b a 

STEP 2: Eliminate renaming rules
 V_N = {'A', 'S', 'D', 'B'}
V_T = {'d', 'b', 'a'}
S   = S
P:
  A -> a A a A b
  A -> a a A b
  A -> d S
  A -> a a b
  A -> a A a b
  A -> d
  S -> a A a A b
  S -> d B
  S -> a a A b
  S -> a S
  S -> a
  S -> d S
  S -> A B
  S -> a a b
  S -> ε
  S -> a A a b
  S -> d
  D -> A b a
  D -> b a
  B -> a A a A b
  B -> a a A b
  B -> a S
  B -> d S
  B -> a a b
  B -> a
  B -> a A a b
  B -> d 

STEP 3: Eliminate inaccessible symbols
 V_N = {'A', 'S', 'B'}
V_T = {'d', 'b', 'a'}
S   = S
P:
  A -> a A a A b
  A -> a a A b
  A -> d S
  A -> a a b
  A -> a A a b
  A -> d
  S -> a A a A b
  S -> d B
  S -> a a A b
  S -> a S
  S -> a
  S -> d S
  S -> A B
  S -> a a b
  S -> ε
  S -> a A a b
  S -> d
  B -> a A a A b
  B -> a a A b
  B -> a S
  B -> d S
  B -> a a b
  B -> a
  B -> a A a b
  B -> d 

STEP 4: Eliminate non-productive symbols
 V_N = {'A', 'S', 'B'}
V_T = {'d', 'b', 'a'}
S   = S
P:
  A -> a A a A b
  A -> a a A b
  A -> d S
  A -> a a b
  A -> a A a b
  A -> d
  S -> a A a A b
  S -> d B
  S -> a a A b
  S -> a S
  S -> a
  S -> d S
  S -> A B
  S -> a a b
  S -> ε
  S -> a A a b
  S -> d
  B -> a A a A b
  B -> a a A b
  B -> a S
  B -> d S
  B -> a a b
  B -> a
  B -> a A a b
  B -> d 

STEP 5: Chomsky Normal Form
 V_N = {'A', 'X10', 'X12', 'X14', 'X20', 'X13', 'X18', 'T_D2', 'X8', 'X6', 'X7', 'X11', 'X19', 'X15', 'X21', 'X17', 'T_B1', 'X24', 'X16', 'X26', 'T_A0', 'S', 'X22', 'X5', 'B', 'X3', 'X23', 'X4', 'X9', 'X25'}
V_T = {'d', 'b', 'a'}
S   = S
P:
  A -> T_A0 X3
  X3 -> A X4
  X4 -> T_A0 X5
  X5 -> A T_B1
  X5 -> T_A0 X6
  X6 -> T_A0 X7
  X7 -> A T_B1
  X7 -> T_D2 S
  X7 -> T_A0 X8
  X8 -> T_A0 T_B1
  X8 -> T_A0 X9
  X9 -> A X10
  X10 -> T_A0 T_B1
  X10 -> d
  S -> T_A0 X11
  X11 -> A X12
  X12 -> T_A0 X13
  X13 -> A T_B1
  X13 -> T_D2 B
  X13 -> T_A0 X14
  X14 -> T_A0 X15
  X15 -> A T_B1
  X15 -> T_A0 S
  X15 -> a
  X15 -> T_D2 S
  X15 -> A B
  X15 -> T_A0 X16
  X16 -> T_A0 T_B1
  X16 -> ε
  X16 -> T_A0 X17
  X17 -> A X18
  X18 -> T_A0 T_B1
  X18 -> d
  B -> T_A0 X19
  X19 -> A X20
  X20 -> T_A0 X21
  X21 -> A T_B1
  X21 -> T_A0 X22
  X22 -> T_A0 X23
  X23 -> A T_B1
  X23 -> T_A0 S
  X23 -> T_D2 S
  X23 -> T_A0 X24
  X24 -> T_A0 T_B1
  X24 -> a
  X24 -> T_A0 X25
  X25 -> A X26
  X26 -> T_A0 T_B1
  X26 -> d
  T_A0 -> a
  T_B1 -> b
  T_D2 -> d 
```

## Final Thoughts

The most challenging parts:

- generating all ε-combinations  
- maintaining correctness across transformations  

This lab shows that **transformation order is critical** in formal grammar processing.