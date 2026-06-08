"""Execution of MiniLang pseudo-assembly."""

from __future__ import annotations

from dataclasses import dataclass

from .errors import ExecutionError


@dataclass(frozen=True)
class ExecutionResult:
    output: list[int]
    memory: dict[str, int]


def executar(codigo_intermediario: list[str]) -> ExecutionResult:
    """Execute pseudo-assembly instructions sequentially."""

    memory: dict[str, int] = {}
    output: list[int] = []
    accumulator = 0

    for line_number, instruction in enumerate(codigo_intermediario, start=1):
        parts = instruction.split()
        if len(parts) != 2:
            raise ExecutionError(f"instrucao invalida '{instruction}'", line_number)

        command, operand = parts

        if command == "LOAD":
            accumulator = _resolve_operand(operand, memory, line_number)
        elif command == "ADD":
            accumulator += _resolve_operand(operand, memory, line_number)
        elif command == "STORE":
            memory[operand] = accumulator
        elif command == "PRINT":
            output.append(_resolve_operand(operand, memory, line_number))
        else:
            raise ExecutionError(f"comando desconhecido '{command}'", line_number)

    return ExecutionResult(output=output, memory=memory)


def _resolve_operand(operand: str, memory: dict[str, int], line_number: int) -> int:
    if operand.lstrip("-").isdigit():
        return int(operand)
    if operand in memory:
        return memory[operand]
    raise ExecutionError(f"variavel '{operand}' nao encontrada na memoria", line_number)
