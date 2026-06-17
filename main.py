"""Interface de terminal para o compilador educacional MiniLang."""

from pathlib import Path

from minilang.compiler import compilar
from minilang.errors import MiniLangError
from minilang.parser import Assignment, BinaryOperation, Number, Print, Program, Variable, While


ROOT = Path(__file__).parent
EXAMPLES = {
    "2": ROOT / "examples" / "valido.min",
    "3": ROOT / "examples" / "erro_lexico.min",
    "4": ROOT / "examples" / "erro_sintatico.min",
    "5": ROOT / "examples" / "erro_semantico.min",
}


def main() -> None:
    while True:
        print("\n=== Compilador MiniLang ===")
        print("1. Digitar codigo MiniLang")
        print("2. Executar exemplo valido")
        print("3. Executar exemplo com erro lexico")
        print("4. Executar exemplo com erro sintatico")
        print("5. Executar exemplo com erro semantico")
        print("6. Explicar etapas da compilacao")
        print("0. Sair")

        option = input("Opcao: ").strip()

        if option == "0":
            print("Encerrando.")
            return
        if option == "1":
            codigo = read_multiline_code()
            run_code(codigo, detailed=True)
        elif option in EXAMPLES:
            codigo = EXAMPLES[option].read_text(encoding="utf-8")
            print("\n--- Codigo de entrada ---")
            print(codigo)
            run_code(codigo, detailed=False)
        elif option == "6":
            explain_stages()
        else:
            print("Opcao invalida.")


def read_multiline_code() -> str:
    print("\nDigite o codigo MiniLang. Use uma linha vazia para finalizar:")
    lines: list[str] = []

    while True:
        line = input("> ")
        if line == "":
            break
        lines.append(line)

    return "\n".join(lines)


def run_code(codigo: str, detailed: bool) -> None:
    try:
        result = compilar(codigo)
    except MiniLangError as error:
        print("\n--- Erro ---")
        print(error)
        print_error_pointer(codigo, error)
        return

    visible_tokens = [token for token in result.tokens if token.value != "\\n"]

    print("\n--- Analise ---")
    print(f"Tokens reconhecidos: {len(visible_tokens)}")
    print("AST gerada com sucesso.")

    if detailed:
        print("\n--- Tokens ---")
        print(visible_tokens)

        print("\n--- AST ---")
        print(format_ast(result.ast))

    print("\n--- Codigo intermediario ---")
    for instruction in result.codigo_intermediario:
        print(instruction)

    print("\n--- Resultado ---")
    if result.resultado.output:
        for value in result.resultado.output:
            print(value)
    else:
        print("(sem saida)")

    print("\n--- Memoria ---")
    print(result.resultado.memory)


def print_error_pointer(codigo: str, error: MiniLangError) -> None:
    if error.line is None or error.column is None:
        return

    lines = codigo.splitlines()
    if not 1 <= error.line <= len(lines):
        return

    source_line = lines[error.line - 1]
    print(source_line)
    print(" " * (error.column - 1) + "^")


def format_ast(program: Program) -> str:
    lines = ["Program"]
    for statement in program.statements:
        lines.extend(format_statement(statement, 1))
    return "\n".join(lines)


def format_statement(statement: Assignment | Print | While, level: int) -> list[str]:
    indent = "  " * level

    if isinstance(statement, Assignment):
        lines = [f"{indent}Assignment {statement.name}"]
        lines.extend(format_expression(statement.expression, level + 1))
        return lines
    if isinstance(statement, Print):
        lines = [f"{indent}Print"]
        lines.extend(format_expression(statement.expression, level + 1))
        return lines
    if isinstance(statement, While):
        lines = [f"{indent}While"]
        lines.append(f"{indent}  Condition")
        lines.extend(format_expression(statement.condition, level + 2))
        lines.append(f"{indent}  Body")
        for body_statement in statement.body:
            lines.extend(format_statement(body_statement, level + 2))
        return lines

    return [f"{indent}Statement desconhecido"]


def format_expression(expression: Number | Variable | BinaryOperation, level: int) -> list[str]:
    indent = "  " * level

    if isinstance(expression, Number):
        return [f"{indent}Number {expression.value}"]
    if isinstance(expression, Variable):
        return [f"{indent}Variable {expression.name}"]
    if isinstance(expression, BinaryOperation):
        lines = [f"{indent}BinaryOperation {expression.operator.value}"]
        lines.extend(format_expression(expression.left, level + 1))
        lines.extend(format_expression(expression.right, level + 1))
        return lines

    return [f"{indent}Expression desconhecida"]


def explain_stages() -> None:
    print("\n--- Etapas da compilacao ---")
    print("1. Lexer: transforma caracteres em tokens usando expressoes regulares.")
    print("2. Parser: valida a gramatica e monta a AST.")
    print("3. Semantico: verifica regras de significado, como variaveis ja definidas.")
    print("4. Intermediario: traduz a AST para pseudo-assembly.")
    print("5. Executor: processa o pseudo-assembly usando memoria, pilha e acumulador.")


if __name__ == "__main__":
    main()
