"""Erros personalizados usados pelas etapas do compilador MiniLang."""


class MiniLangError(Exception):
    """Classe base para todos os erros da MiniLang."""

    label = "Erro"

    def __init__(self, message: str, line: int | None = None, column: int | None = None):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(self.__str__())

    def __str__(self) -> str:
        location = ""
        if self.line is not None:
            location = f" na linha {self.line}"
            if self.column is not None:
                location += f", coluna {self.column}"
        return f"{self.label}{location}: {self.message}"


class LexicalError(MiniLangError):
    label = "Erro lexico"


class SyntaxErrorMiniLang(MiniLangError):
    label = "Erro sintatico"


class SemanticError(MiniLangError):
    label = "Erro semantico"


class ExecutionError(MiniLangError):
    label = "Erro de execucao"
