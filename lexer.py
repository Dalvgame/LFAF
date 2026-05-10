import re
from token_type import TokenType
from token_model import Token

_TOKEN_REGEX = re.compile(
    '|'.join(f'(?P<{tt.name}>{tt.value})' for tt in TokenType if tt != TokenType.EOF),
    re.MULTILINE,
)

# Token types whose matches should be silently discarded
_SKIP = {TokenType.WHITESPACE, TokenType.COMMENT}


class Lexer:


    def __init__(self, source: str) -> None:
        self._source = source

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def tokenise(self) -> list[Token]:

        tokens: list[Token] = []

        for match in _TOKEN_REGEX.finditer(self._source):
            kind_name = match.lastgroup          # name of the matched group
            value     = match.group()
            kind      = TokenType[kind_name]

            if kind in _SKIP:
                continue                         # silently discard

            tokens.append(Token(kind, value))

        tokens.append(Token(TokenType.EOF, "EOF"))
        return tokens