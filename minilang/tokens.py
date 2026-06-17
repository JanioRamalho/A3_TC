"""Definicoes de tokens da MiniLang."""

from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    ID = auto()
    NUM = auto()
    ASSIGN = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    LT = auto()
    GT = auto()
    EQ = auto()
    PRINT = auto()
    WHILE = auto()
    END = auto()
    LPAREN = auto()
    RPAREN = auto()
    NEWLINE = auto()
    EOF = auto()


@dataclass(frozen=True)
class Token:
    type: TokenType
    value: str
    line: int
    column: int

    def __repr__(self) -> str:
        if self.type in {TokenType.ID, TokenType.NUM}:
            return f"{self.type.name}({self.value})"
        if self.type is TokenType.EOF:
            return "EOF"
        if self.type is TokenType.NEWLINE:
            return "NEWLINE"
        return self.type.name
