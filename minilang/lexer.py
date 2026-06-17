"""Analise lexica da MiniLang."""

from __future__ import annotations

import re

from .errors import LexicalError
from .tokens import Token, TokenType


TOKEN_REGEX = re.compile(
    r"(?P<NUM>\d+)"
    r"|(?P<ID>[A-Za-z_][A-Za-z0-9_]*)"
    r"|(?P<EQ>==)"
    r"|(?P<ASSIGN>=)"
    r"|(?P<PLUS>\+)"
    r"|(?P<MINUS>-)"
    r"|(?P<STAR>\*)"
    r"|(?P<SLASH>/)"
    r"|(?P<LT><)"
    r"|(?P<GT>>)"
    r"|(?P<LPAREN>\()"
    r"|(?P<RPAREN>\))"
    r"|(?P<SKIP>[ \t]+)"
    r"|(?P<MISMATCH>.)"
)


def lexer(codigo: str) -> list[Token]:
    """Transforma codigo-fonte em uma lista de tokens.

    O analisador consome a entrada da esquerda para a direita, como um
    pequeno AFD: cada expressao regular reconhecida move a analise para
    um estado de token.
    """

    tokens: list[Token] = []

    for line_number, line in enumerate(codigo.splitlines(), start=1):
        for match in TOKEN_REGEX.finditer(line):
            kind = match.lastgroup
            value = match.group()
            column = match.start() + 1

            if kind == "SKIP":
                continue
            if kind == "MISMATCH":
                raise LexicalError(f"caractere invalido '{value}'", line_number, column)

            keywords = {
                "print": TokenType.PRINT,
                "while": TokenType.WHILE,
                "end": TokenType.END,
            }
            token_type = keywords.get(value, TokenType[kind]) if kind == "ID" else TokenType[kind]
            tokens.append(Token(token_type, value, line_number, column))

        tokens.append(Token(TokenType.NEWLINE, "\\n", line_number, len(line) + 1))

    eof_line = max(len(codigo.splitlines()), 1)
    tokens.append(Token(TokenType.EOF, "", eof_line, 1))
    return tokens
