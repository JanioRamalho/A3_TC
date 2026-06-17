"""Integracao de todas as etapas do compilador MiniLang."""

from __future__ import annotations

from dataclasses import dataclass

from .executor import ExecutionResult, executar
from .intermediate import gerar_codigo
from .lexer import lexer
from .parser import Program, parser
from .semantic import semantico
from .tokens import Token


@dataclass(frozen=True)
class CompilerResult:
    tokens: list[Token]
    ast: Program
    codigo_intermediario: list[str]
    resultado: ExecutionResult


def compilar(codigo: str) -> CompilerResult:
    """Executa as etapas lexica, sintatica, semantica, intermediaria e de execucao."""

    tokens = lexer(codigo)
    ast = parser(tokens)
    semantico(ast)
    codigo_intermediario = gerar_codigo(ast)
    resultado = executar(codigo_intermediario)

    return CompilerResult(
        tokens=tokens,
        ast=ast,
        codigo_intermediario=codigo_intermediario,
        resultado=resultado,
    )
