import re
from enum import Enum


class TokenType(Enum):

    # Keywords
    DEF        = r'\bdef\b'
    SIN        = r'\bsin\b'
    COS        = r'\bcos\b'

    # Literals and names
    NUMBER     = r'\d+\.\d+|\d+'      # floats before ints  (e.g. 3.14 before 3)
    IDENTIFIER = r'[A-Za-z_][A-Za-z0-9_]*'

    # Operators
    PLUS       = r'\+'
    MINUS      = r'-'
    MULTIPLY   = r'\*'
    DIVIDE     = r'/'
    ASSIGN     = r'='

    # Punctuation
    LPAREN     = r'\('
    RPAREN     = r'\)'
    COMMA      = r','

    # Skipped
    COMMENT    = r'#[^\n]*'
    WHITESPACE = r'[ \t\r\n]+'

    # Sentinel
    EOF        = r'$^'               # never matches real input; used as sentinel