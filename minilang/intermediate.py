"""Geracao de pseudo-assembly intermediario para MiniLang."""

from __future__ import annotations

from .parser import Assignment, BinaryOperation, Expression, Number, Operator, Print, Program, Variable, While


ARITHMETIC_COMMANDS = {
    Operator.ADD: "ADD_STACK",
    Operator.SUB: "SUB_STACK",
    Operator.MUL: "MUL_STACK",
    Operator.DIV: "DIV_STACK",
    Operator.LT: "LT_STACK",
    Operator.GT: "GT_STACK",
    Operator.EQ: "EQ_STACK",
}


class CodeGenerator:
    def __init__(self) -> None:
        self.instructions: list[str] = []
        self.label_count = 0

    def generate(self, program: Program) -> list[str]:
        self._statements(program.statements)
        return self.instructions

    def _statements(self, statements: list[Assignment | Print | While]) -> None:
        for statement in statements:
            if isinstance(statement, Assignment):
                self._expression(statement.expression)
                self.instructions.append(f"STORE {statement.name}")
            elif isinstance(statement, Print):
                self._expression(statement.expression)
                self.instructions.append("PRINT_ACC")
            elif isinstance(statement, While):
                self._while(statement)

    def _while(self, statement: While) -> None:
        start_label = self._new_label("WHILE_START")
        end_label = self._new_label("WHILE_END")

        self.instructions.append(f"LABEL {start_label}")
        self._expression(statement.condition)
        self.instructions.append(f"JZ {end_label}")
        self._statements(statement.body)
        self.instructions.append(f"JMP {start_label}")
        self.instructions.append(f"LABEL {end_label}")

    def _expression(self, expression: Expression) -> None:
        if isinstance(expression, Number):
            self.instructions.append(f"LOAD {expression.value}")
        elif isinstance(expression, Variable):
            self.instructions.append(f"LOAD {expression.name}")
        elif isinstance(expression, BinaryOperation):
            # Para expressoes aninhadas, a esquerda fica guardada na pilha
            # enquanto a direita e calculada no acumulador.
            self._expression(expression.left)
            self.instructions.append("PUSH")
            self._expression(expression.right)
            self.instructions.append(ARITHMETIC_COMMANDS[expression.operator])
        else:
            raise ValueError("expressao desconhecida")

    def _new_label(self, prefix: str) -> str:
        self.label_count += 1
        return f"{prefix}_{self.label_count}"


def gerar_codigo(program: Program) -> list[str]:
    """Gera instrucoes pseudo-assembly a partir da AST."""

    return CodeGenerator().generate(program)
