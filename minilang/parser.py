"""Analise sintatica e construcao da AST da MiniLang."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .errors import SyntaxErrorMiniLang
from .tokens import Token, TokenType


class Operator(Enum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    LT = "<"
    GT = ">"
    EQ = "=="


@dataclass(frozen=True)
class Number:
    value: int


@dataclass(frozen=True)
class Variable:
    name: str
    line: int
    column: int


@dataclass(frozen=True)
class BinaryOperation:
    left: "Expression"
    operator: Operator
    right: "Expression"


# Alias mantido para compatibilidade com os testes/codigo antigo.
BinaryAdd = BinaryOperation


Expression = Number | Variable | BinaryOperation


@dataclass(frozen=True)
class Assignment:
    name: str
    expression: Expression
    line: int
    column: int


@dataclass(frozen=True)
class Print:
    expression: Expression
    line: int
    column: int


@dataclass(frozen=True)
class While:
    condition: Expression
    body: list["Statement"]
    line: int
    column: int


Statement = Assignment | Print | While


@dataclass(frozen=True)
class Program:
    statements: list[Statement]


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.position = 0

    def parse(self) -> Program:
        # Um programa completo e um bloco que termina somente no EOF.
        statements = self._block_until(TokenType.EOF)
        self._consume(TokenType.EOF, "esperado fim do arquivo")
        return Program(statements)

    def _block_until(self, end_token: TokenType) -> list[Statement]:
        # A mesma funcao serve para o programa inteiro e para o corpo do while.
        statements: list[Statement] = []
        self._skip_newlines()

        while not self._check(end_token) and not self._check(TokenType.EOF):
            statements.append(self._statement())
            self._skip_newlines()

        return statements

    def _statement(self) -> Statement:
        if self._check(TokenType.PRINT):
            statement = self._print()
        elif self._check(TokenType.WHILE):
            statement = self._while()
        elif self._check(TokenType.ID):
            statement = self._assignment()
        else:
            token = self._current()
            raise SyntaxErrorMiniLang("esperado atribuicao, print() ou while", token.line, token.column)

        self._consume_statement_end()
        return statement

    def _assignment(self) -> Assignment:
        name = self._consume(TokenType.ID, "esperado nome da variavel")
        self._consume(TokenType.ASSIGN, f"esperado '=' apos variavel '{name.value}'")
        expression = self._expression()
        return Assignment(name.value, expression, name.line, name.column)

    def _print(self) -> Print:
        start = self._consume(TokenType.PRINT, "esperado comando print")
        self._consume(TokenType.LPAREN, "esperado '(' apos print")
        expression = self._expression()
        self._consume(TokenType.RPAREN, "esperado ')' apos expressao do print")
        return Print(expression, start.line, start.column)

    def _while(self) -> While:
        start = self._consume(TokenType.WHILE, "esperado comando while")
        condition = self._comparison()
        self._consume_statement_end()

        body = self._block_until(TokenType.END)
        self._consume(TokenType.END, "esperado 'end' para fechar o while")
        return While(condition, body, start.line, start.column)

    def _comparison(self) -> Expression:
        expression = self._expression()

        if self._match(TokenType.LT):
            return BinaryOperation(expression, Operator.LT, self._expression())
        if self._match(TokenType.GT):
            return BinaryOperation(expression, Operator.GT, self._expression())
        if self._match(TokenType.EQ):
            return BinaryOperation(expression, Operator.EQ, self._expression())

        token = self._current()
        raise SyntaxErrorMiniLang("esperado comparador '<', '>' ou '==' no while", token.line, token.column)

    def _expression(self) -> Expression:
        expression = self._term()

        # Soma e subtracao tem precedencia menor que multiplicacao e divisao.
        while self._check(TokenType.PLUS) or self._check(TokenType.MINUS):
            if self._match(TokenType.PLUS):
                operator = Operator.ADD
            else:
                self._consume(TokenType.MINUS, "esperado '-'")
                operator = Operator.SUB
            expression = BinaryOperation(expression, operator, self._term())

        return expression

    def _term(self) -> Expression:
        expression = self._factor()

        # Multiplicacao e divisao sao agrupadas antes de soma e subtracao.
        while self._check(TokenType.STAR) or self._check(TokenType.SLASH):
            if self._match(TokenType.STAR):
                operator = Operator.MUL
            else:
                self._consume(TokenType.SLASH, "esperado '/'")
                operator = Operator.DIV
            expression = BinaryOperation(expression, operator, self._factor())

        return expression

    def _factor(self) -> Expression:
        if self._check(TokenType.NUM):
            token = self._advance()
            return Number(int(token.value))
        if self._check(TokenType.ID):
            token = self._advance()
            return Variable(token.value, token.line, token.column)
        if self._match(TokenType.LPAREN):
            expression = self._expression()
            self._consume(TokenType.RPAREN, "esperado ')' apos expressao")
            return expression

        token = self._current()
        raise SyntaxErrorMiniLang("esperado numero, variavel ou '('", token.line, token.column)

    def _consume_statement_end(self) -> None:
        if self._check(TokenType.NEWLINE) or self._check(TokenType.EOF) or self._check(TokenType.END):
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
    """Valida a ordem dos tokens e retorna a AST da MiniLang."""

    return Parser(tokens).parse()
