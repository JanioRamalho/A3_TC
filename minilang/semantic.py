"""Analise semantica da MiniLang."""

from __future__ import annotations

from .errors import SemanticError
from .parser import Assignment, BinaryOperation, Expression, Number, Print, Program, Variable, While


def semantico(program: Program) -> set[str]:
    """Valida o uso de variaveis e retorna o conjunto de variaveis definidas."""

    defined: set[str] = set()
    _check_statements(program.statements, defined)
    return defined


def _check_statements(statements: list[Assignment | Print | While], defined: set[str]) -> None:
    for statement in statements:
        if isinstance(statement, Assignment):
            _check_expression(statement.expression, defined)
            defined.add(statement.name)
        elif isinstance(statement, Print):
            _check_expression(statement.expression, defined)
        elif isinstance(statement, While):
            _check_expression(statement.condition, defined)
            body_defined = set(defined)
            _check_statements(statement.body, body_defined)


def _check_expression(expression: Expression, defined: set[str]) -> None:
    if isinstance(expression, Number):
        return
    if isinstance(expression, Variable):
        if expression.name not in defined:
            raise SemanticError(
                f"variavel '{expression.name}' usada antes de ser definida",
                expression.line,
                expression.column,
            )
        return
    if isinstance(expression, BinaryOperation):
        _check_expression(expression.left, defined)
        _check_expression(expression.right, defined)
        return

    raise SemanticError("expressao desconhecida")
