"""Syntax analysis and AST construction for MiniLang."""

from __future__ import annotations

from dataclasses import dataclass

from .errors import SyntaxErrorMiniLang
from .tokens import Token, TokenType


@dataclass(frozen=True)
class Number:
    value: int


@dataclass(frozen=True)
class Variable:
    name: str
    line: int
    column: int


@dataclass(frozen=True)
class BinaryAdd:
    left: "Expression"
    right: "Expression"


Expression = Number | Variable | BinaryAdd


@dataclass(frozen=True)
class Assignment:
    name: str
    expression: Expression
    line: int
    column: int


@dataclass(frozen=True)
class Print:
    name: str
    line: int
    column: int


Statement = Assignment | Print


@dataclass(frozen=True)
class Program:
    statements: list[Statement]


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.position = 0

    def parse(self) -> Program:
        statements: list[Statement] = []
        self._skip_newlines()

        while not self._check(TokenType.EOF):
            statements.append(self._statement())
            self._consume_statement_end()
            self._skip_newlines()

        return Program(statements)

    def _statement(self) -> Statement:
        if self._check(TokenType.PRINT):
            return self._print()
        if self._check(TokenType.ID):
            return self._assignment()

        token = self._current()
        raise SyntaxErrorMiniLang("esperado atribuicao ou print()", token.line, token.column)

    def _assignment(self) -> Assignment:
        name = self._consume(TokenType.ID, "esperado nome da variavel")
        self._consume(TokenType.ASSIGN, f"esperado '=' apos variavel '{name.value}'")
        expression = self._expression()
        return Assignment(name.value, expression, name.line, name.column)

    def _print(self) -> Print:
        start = self._consume(TokenType.PRINT, "esperado comando print")
        self._consume(TokenType.LPAREN, "esperado '(' apos print")
        name = self._consume(TokenType.ID, "esperado variavel dentro de print()")
        self._consume(TokenType.RPAREN, "esperado ')' apos variavel do print")
        return Print(name.value, start.line, start.column)

    def _expression(self) -> Expression:
        expression = self._term()

        if self._match(TokenType.PLUS):
            right = self._term()
            expression = BinaryAdd(expression, right)

        return expression

    def _term(self) -> Expression:
        if self._check(TokenType.NUM):
            token = self._advance()
            return Number(int(token.value))
        if self._check(TokenType.ID):
            token = self._advance()
            return Variable(token.value, token.line, token.column)

        token = self._current()
        raise SyntaxErrorMiniLang("esperado numero ou variavel", token.line, token.column)

    def _consume_statement_end(self) -> None:
        if self._check(TokenType.NEWLINE) or self._check(TokenType.EOF):
            return

        token = self._current()
        raise SyntaxErrorMiniLang("esperado fim da linha", token.line, token.column)

    def _skip_newlines(self) -> None:
        while self._match(TokenType.NEWLINE):
            pass

    def _consume(self, token_type: TokenType, message: str) -> Token:
        if self._check(token_type):
            return self._advance()

        token = self._current()
        raise SyntaxErrorMiniLang(message, token.line, token.column)

    def _match(self, token_type: TokenType) -> bool:
        if self._check(token_type):
            self._advance()
            return True
        return False

    def _check(self, token_type: TokenType) -> bool:
        return self._current().type is token_type

    def _advance(self) -> Token:
        token = self._current()
        if token.type is not TokenType.EOF:
            self.position += 1
        return token

    def _current(self) -> Token:
        return self.tokens[self.position]


def parser(tokens: list[Token]) -> Program:
    """Validate token order and return the MiniLang AST."""

    return Parser(tokens).parse()
