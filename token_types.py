from enum import Enum

class TokenType(Enum):
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    PLUS = "+"
    MINUS = "-"
    MUL = "*"
    DIV = "/"
    LPAREN = "("
    RPAREN = ")"
    FUNCTION = "FUNCTION"
    VARIABLE = "VARIABLE"