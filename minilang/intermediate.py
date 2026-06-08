"""Intermediate pseudo-assembly generation for MiniLang."""

from __future__ import annotations

from .parser import Assignment, BinaryAdd, Expression, Number, Print, Program, Variable


def gerar_codigo(program: Program) -> list[str]:
    """Generate pseudo-assembly instructions from the AST."""

    instructions: list[str] = []

    for statement in program.statements:
        if isinstance(statement, Assignment):
            instructions.extend(_expression_code(statement.expression))
            instructions.append(f"STORE {statement.name}")
        elif isinstance(statement, Print):
            instructions.append(f"PRINT {statement.name}")

    return instructions


def _expression_code(expression: Expression) -> list[str]:
    if isinstance(expression, Number):
        return [f"LOAD {expression.value}"]
    if isinstance(expression, Variable):
        return [f"LOAD {expression.name}"]
    if isinstance(expression, BinaryAdd):
        instructions = _expression_code(expression.left)
        instructions.append(f"ADD {_operand(expression.right)}")
        return instructions

    raise ValueError("expressao desconhecida")


def _operand(expression: Expression) -> str:
    if isinstance(expression, Number):
        return str(expression.value)
    if isinstance(expression, Variable):
        return expression.name
    raise ValueError("a MiniLang suporta soma apenas entre termos simples")
