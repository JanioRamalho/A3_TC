"""Terminal interface for the MiniLang educational compiler."""

from pathlib import Path

from minilang.compiler import compilar
from minilang.errors import MiniLangError


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
        print("0. Sair")

        option = input("Opcao: ").strip()

        if option == "0":
            print("Encerrando.")
            return
        if option == "1":
            codigo = read_multiline_code()
            run_code(codigo)
        elif option in EXAMPLES:
            codigo = EXAMPLES[option].read_text(encoding="utf-8")
            print("\n--- Codigo de entrada ---")
            print(codigo)
            run_code(codigo)
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


def run_code(codigo: str) -> None:
    try:
        result = compilar(codigo)
    except MiniLangError as error:
        print("\n--- Erro ---")
        print(error)
        return

    visible_tokens = [token for token in result.tokens if token.value != "\\n"]

    print("\n--- Tokens ---")
    print(visible_tokens)

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


if __name__ == "__main__":
    main()
