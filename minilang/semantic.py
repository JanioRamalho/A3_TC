"""Semantic analysis for MiniLang."""

from __future__ import annotations

from .errors import SemanticError
from .parser import Assignment, BinaryAdd, Expression, Number, Print, Program, Variable


def semantico(program: Program) -> set[str]:
    """Validate variable usage and return the set of defined variables."""

    defined: set[str] = set()

    for statement in program.statements:
        if isinstance(statement, Assignment):
            _check_expression(statement.expression, defined)
            defined.add(statement.name)
        elif isinstance(statement, Print):
            if statement.name not in defined:
                raise SemanticError(
                    f"variavel '{statement.name}' usada antes de ser definida",
                    statement.line,
                    statement.column,
                )

    return defined


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
    if isinstance(expression, BinaryAdd):
        _check_expression(expression.left, defined)
        _check_expression(expression.right, defined)
        return

    raise SemanticError("expressao desconhecida")
