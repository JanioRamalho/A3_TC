"""Execucao do pseudo-assembly da MiniLang."""

from __future__ import annotations

from dataclasses import dataclass

from .errors import ExecutionError


@dataclass(frozen=True)
class ExecutionResult:
    output: list[int]
    memory: dict[str, int]


def executar(codigo_intermediario: list[str]) -> ExecutionResult:
    """Executa instrucoes pseudo-assembly sequencialmente."""

    # Rotulos sao mapeados antes da execucao para permitir saltos no while.
    labels = _map_labels(codigo_intermediario)
    memory: dict[str, int] = {}
    output: list[int] = []
    stack: list[int] = []
    accumulator = 0
    instruction_pointer = 0

    while instruction_pointer < len(codigo_intermediario):
        instruction = codigo_intermediario[instruction_pointer]
        parts = instruction.split()
        if len(parts) > 2:
            raise ExecutionError(f"instrucao invalida '{instruction}'", instruction_pointer + 1)

        command = parts[0]
        operand = parts[1] if len(parts) == 2 else None
        line_number = instruction_pointer + 1

        if command == "LABEL":
            instruction_pointer += 1
            continue
        if command == "LOAD":
            accumulator = _resolve_operand(_required_operand(operand, instruction, line_number), memory, line_number)
        elif command == "PUSH":
            _reject_operand(operand, instruction, line_number)
            stack.append(accumulator)
        elif command in {"ADD_STACK", "SUB_STACK", "MUL_STACK", "DIV_STACK", "LT_STACK", "GT_STACK", "EQ_STACK"}:
            _reject_operand(operand, instruction, line_number)
            left = _pop_stack(stack, line_number)
            accumulator = _apply_stack_operation(command, left, accumulator, line_number)
        elif command == "STORE":
            memory[_required_operand(operand, instruction, line_number)] = accumulator
        elif command == "PRINT":
            output.append(_resolve_operand(_required_operand(operand, instruction, line_number), memory, line_number))
        elif command == "PRINT_ACC":
            _reject_operand(operand, instruction, line_number)
            output.append(accumulator)
        elif command == "JMP":
            instruction_pointer = _jump_to(_required_operand(operand, instruction, line_number), labels, line_number)
            continue
        elif command == "JZ":
            label = _required_operand(operand, instruction, line_number)
            if accumulator == 0:
                instruction_pointer = _jump_to(label, labels, line_number)
                continue
        else:
            raise ExecutionError(f"comando desconhecido '{command}'", line_number)

        instruction_pointer += 1

    return ExecutionResult(output=output, memory=memory)


def _map_labels(codigo_intermediario: list[str]) -> dict[str, int]:
    labels: dict[str, int] = {}

    for index, instruction in enumerate(codigo_intermediario):
        parts = instruction.split()
        if parts and parts[0] == "LABEL":
            if len(parts) != 2:
                raise ExecutionError(f"instrucao invalida '{instruction}'", index + 1)
            labels[parts[1]] = index

    return labels


def _apply_stack_operation(command: str, left: int, right: int, line_number: int) -> int:
    if command == "ADD_STACK":
        return left + right
    if command == "SUB_STACK":
        return left - right
    if command == "MUL_STACK":
        return left * right
    if command == "DIV_STACK":
        if right == 0:
            raise ExecutionError("divisao por zero", line_number)
        return left // right
    if command == "LT_STACK":
        return int(left < right)
    if command == "GT_STACK":
        return int(left > right)
    if command == "EQ_STACK":
        return int(left == right)

    raise ExecutionError(f"operacao desconhecida '{command}'", line_number)


def _resolve_operand(operand: str, memory: dict[str, int], line_number: int) -> int:
    if operand.lstrip("-").isdigit():
        return int(operand)
    if operand in memory:
        return memory[operand]
    raise ExecutionError(f"variavel '{operand}' nao encontrada na memoria", line_number)


def _required_operand(operand: str | None, instruction: str, line_number: int) -> str:
    if operand is None:
        raise ExecutionError(f"instrucao invalida '{instruction}'", line_number)
    return operand


def _reject_operand(operand: str | None, instruction: str, line_number: int) -> None:
    if operand is not None:
        raise ExecutionError(f"instrucao invalida '{instruction}'", line_number)


def _pop_stack(stack: list[int], line_number: int) -> int:
    if not stack:
        raise ExecutionError("pilha vazia durante operacao", line_number)
    return stack.pop()


def _jump_to(label: str, labels: dict[str, int], line_number: int) -> int:
    if label not in labels:
        raise ExecutionError(f"rotulo '{label}' nao encontrado", line_number)
    return labels[label]
