"""Lexical analysis for MiniLang."""

from __future__ import annotations

import re

from .errors import LexicalError
from .tokens import Token, TokenType


TOKEN_REGEX = re.compile(
    r"(?P<NUM>\d+)"
    r"|(?P<ID>[A-Za-z_][A-Za-z0-9_]*)"
    r"|(?P<ASSIGN>=)"
    r"|(?P<PLUS>\+)"
    r"|(?P<LPAREN>\()"
    r"|(?P<RPAREN>\))"
    r"|(?P<SKIP>[ \t]+)"
    r"|(?P<MISMATCH>.)"
)


def lexer(codigo: str) -> list[Token]:
    """Transform source code into a list of tokens.

    The scanner consumes the input from left to right, like a small AFD:
    each recognized regular expression moves the analysis to a token state.
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

            token_type = TokenType.PRINT if kind == "ID" and value == "print" else TokenType[kind]
            tokens.append(Token(token_type, value, line_number, column))

        tokens.append(Token(TokenType.NEWLINE, "\\n", line_number, len(line) + 1))

    eof_line = max(len(codigo.splitlines()), 1)
    tokens.append(Token(TokenType.EOF, "", eof_line, 1))
    return tokens
