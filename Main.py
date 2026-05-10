from lexer import Lexer
from parser import Parser


SOURCE = """\
def add(x, y)
x + y * 2
sin(3.14)
cos(0)
result = 10.5 - 1.1 / 2
# this is a comment
"""


def main() -> None:
    print("=" * 50)
    print("INPUT")
    print("=" * 50)
    print(SOURCE)

    # --- Lexical analysis ---
    lexer  = Lexer(SOURCE)
    tokens = lexer.tokenise()

    print("=" * 50)
    print("TOKENS")
    print("=" * 50)
    for tok in tokens:
        print(tok)

    # --- Parsing ---
    parser  = Parser(tokens)
    program = parser.parse()

    print()
    print("=" * 50)
    print("AST")
    print("=" * 50)
    program.print("", is_last=True)


if __name__ == "__main__":
    main()