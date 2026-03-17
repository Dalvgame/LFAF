from lexer import Lexer

with open("examples.txt") as f:
    lines = f.readlines()

for i, line in enumerate(lines, start=1):

    text = line.strip()

    if not text:
        continue

    print(f"\nExpression {i}: {text}")

    lexer = Lexer(text)
    tokens = lexer.tokenize()

    for token in tokens:
        print(token)