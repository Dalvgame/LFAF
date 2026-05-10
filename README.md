# Laboratory Work 6 – Parser & Building an Abstract Syntax Tree

**Course:** Formal Languages & Finite Automata  
**Author:** Cuibari  Vladislav  
**Group:** FAF-243

---

## Theory

**Parsing** is the process of analysing a sequence of tokens to determine its grammatical structure
according to a formal grammar. Where the lexer converts raw characters into tokens, the parser
decides how those tokens relate to each other and organises them into a tree.

An **Abstract Syntax Tree (AST)** represents only the semantically meaningful structure of the
source text – it discards punctuation noise like parentheses or commas and keeps constructs like
function definitions, assignments, binary operations, and calls. Each node in the tree represents
one such construct, and the tree shape makes it straightforward for later stages (interpreters,
compilers, static analysers) to walk the program structure without re-reading raw text.

---

## Objectives

1. Get familiar with parsing and how it can be programmed.
2. Get familiar with the concept of AST.
3. Extend the Lab 3 lexer work by:
   - Having a `TokenType` enum that uses **regular expressions** to categorise tokens.
   - Implementing the necessary data structures for an AST.
   - Implementing a simple recursive-descent parser.

---

## Project Structure

```
src/
├── token_type.py   # TokenType enum – each member holds a regex pattern
├── token_model.py  # Token dataclass (type + value)
├── lexer.py        # Lexer – regex-based tokeniser
├── ast_nodes.py    # AST node hierarchy
├── parser.py       # Recursive-descent parser
└── main.py         # Entry point
```

---

## Implementation

### `TokenType` – regex-driven categorisation

Each member of the `TokenType` enum carries its own regex pattern as its value.
A single combined regex is compiled from all members in declaration order, which guarantees
that keywords (`def`, `sin`, `cos`) are tried **before** the generic `IDENTIFIER` pattern.

```python
class TokenType(Enum):
    DEF        = r'\bdef\b'
    SIN        = r'\bsin\b'
    COS        = r'\bcos\b'
    NUMBER     = r'\d+\.\d+|\d+'
    IDENTIFIER = r'[A-Za-z_][A-Za-z0-9_]*'
    PLUS       = r'\+'
    MINUS      = r'-'
    MULTIPLY   = r'\*'
    DIVIDE     = r'/'
    ASSIGN     = r'='
    LPAREN     = r'\('
    RPAREN     = r'\)'
    COMMA      = r','
    COMMENT    = r'#[^\n]*'
    WHITESPACE = r'[ \t\r\n]+'
    EOF        = r'$^'
```

### `Lexer` – single-pass regex scan

All patterns are joined into one compiled regex where each group is named after its `TokenType`.
A single `re.finditer` call walks the source string; `WHITESPACE` and `COMMENT` matches are
silently discarded. An `EOF` sentinel is appended at the end.

```python
_TOKEN_REGEX = re.compile(
    '|'.join(f'(?P<{tt.name}>{tt.value})' for tt in TokenType if tt != TokenType.EOF),
    re.MULTILINE,
)

def tokenise(self) -> list[Token]:
    tokens = []
    for match in _TOKEN_REGEX.finditer(self._source):
        kind = TokenType[match.lastgroup]
        if kind in _SKIP:
            continue
        tokens.append(Token(kind, match.group()))
    tokens.append(Token(TokenType.EOF, "EOF"))
    return tokens
```

### `ASTNode` – node hierarchy

`ASTNode` is an abstract base class. Every concrete node overrides `label()` and optionally
`children()`. The base class provides a `print()` method that recursively draws the tree with
Unicode box-drawing characters.

| Node class      | Represents          | Children                  |
|-----------------|---------------------|---------------------------|
| `Program`       | root of the program | all top-level statements  |
| `FunctionDef`   | `def add(x, y)`     | none (params in label)    |
| `Assignment`    | `result = expr`     | the value expression      |
| `FunctionCall`  | `sin(3.14)`         | the argument expressions  |
| `BinaryOp`      | `left OP right`     | left, right               |
| `NumberLiteral` | `3.14`              | none                      |
| `Identifier`    | `x`, `result`       | none                      |

### `Parser` – recursive descent

Operator precedence is encoded purely through method nesting:

```
program    -> statement*
statement  -> funcDef | assignment | expr
funcDef    -> DEF IDENTIFIER LPAREN paramList RPAREN
assignment -> IDENTIFIER ASSIGN expr
expr       -> term  ((PLUS | MINUS) term)*         <- lowest precedence
term       -> factor ((MULTIPLY | DIVIDE) factor)* <- higher
factor     -> NUMBER | LPAREN expr RPAREN | funcCall | IDENTIFIER
funcCall   -> (SIN | COS | IDENTIFIER) LPAREN argList RPAREN
```

Distinguishing assignment from expression uses a two-token lookahead:

```python
def _parse_statement(self) -> ASTNode:
    if self._check(TokenType.DEF):
        return self._parse_function_def()
    if self._check(TokenType.IDENTIFIER) and self._lookahead(1) == TokenType.ASSIGN:
        return self._parse_assignment()
    return self._parse_expr()
```

---

## Results

### Input

```
def add(x, y)
x + y * 2
sin(3.14)
cos(0)
result = 10.5 - 1.1 / 2
```

### Token stream

```
Token(type=DEF, value='def')
Token(type=IDENTIFIER, value='add')
Token(type=LPAREN, value='(')
Token(type=IDENTIFIER, value='x')
Token(type=COMMA, value=',')
Token(type=IDENTIFIER, value='y')
Token(type=RPAREN, value=')')
Token(type=IDENTIFIER, value='x')
Token(type=PLUS, value='+')
Token(type=IDENTIFIER, value='y')
Token(type=MULTIPLY, value='*')
Token(type=NUMBER, value='2')
Token(type=SIN, value='sin')
Token(type=LPAREN, value='(')
Token(type=NUMBER, value='3.14')
Token(type=RPAREN, value=')')
Token(type=COS, value='cos')
Token(type=LPAREN, value='(')
Token(type=NUMBER, value='0')
Token(type=RPAREN, value=')')
Token(type=IDENTIFIER, value='result')
Token(type=ASSIGN, value='=')
Token(type=NUMBER, value='10.5')
Token(type=MINUS, value='-')
Token(type=NUMBER, value='1.1')
Token(type=DIVIDE, value='/')
Token(type=NUMBER, value='2')
Token(type=EOF, value='EOF')
```

### AST

```
└── Program
    ├── FunctionDef: add(x, y)
    ├── BinaryOp: +
    │   ├── Identifier: x
    │   └── BinaryOp: *
    │       ├── Identifier: y
    │       └── Number: 2
    ├── Call: sin
    │   └── Number: 3.14
    ├── Call: cos
    │   └── Number: 0
    └── Assign: result
        └── BinaryOp: -
            ├── Number: 10.5
            └── BinaryOp: /
                ├── Number: 1.1
                └── Number: 2
```

---

## Conclusions

The parser correctly handles all five constructs in the input.

- **Operator precedence** falls out naturally from call nesting – no explicit precedence table needed.
- **Lookahead** cleanly resolves the ambiguity between `result = ...` (assignment) and a bare
  identifier expression, as well as between a function call and a plain variable reference.
- **Regex-driven lexing** means adding a new token kind only requires one new enum member.
- The comment `# this is a comment` is silently dropped by the lexer and never reaches the parser.