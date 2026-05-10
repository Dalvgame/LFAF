from dataclasses import dataclass
from token_type import TokenType


@dataclass
class Token:
    type: TokenType
    value: str

    def __repr__(self) -> str:
        return f"Token(type={self.type.name}, value={self.value!r})"