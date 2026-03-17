import re
from token_types import TokenType

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"{self.type.name}({self.value})"


class Lexer:

    token_specification = [
        ('FLOAT', r'\d+\.\d+'),
        ('INTEGER', r'\d+'),
        ('FUNCTION', r'sin|cos|tan'),
        ('PLUS', r'\+'),
        ('MINUS', r'-'),
        ('MUL', r'\*'),
        ('DIV', r'/'),
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('VARIABLE', r'[a-zA-Z]+'),
        ('SKIP', r'[ \t]+'),
    ]

    def __init__(self, text):
        self.text = text

    def tokenize(self):

        tokens = []

        regex = '|'.join(f'(?P<{name}>{pattern})'
                         for name, pattern in self.token_specification)

        for match in re.finditer(regex, self.text):

            kind = match.lastgroup
            value = match.group()

            if kind == 'SKIP':
                continue

            tokens.append(Token(TokenType[kind], value))

        return tokens