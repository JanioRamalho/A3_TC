# Saida da Opcao 2 - Exemplo Valido

Este documento explica o que acontece quando o usuario escolhe a opcao `2` no menu principal:

```text
2. Executar exemplo valido
```

Essa opcao carrega automaticamente o arquivo:

```text
examples/valido.min
```

## Codigo executado

O exemplo valido atual e:

```text
x = 0
y = (10 + 5) * 2
while x < 3
x = x + 1
end
print(y - x)
```

Esse programa faz o seguinte:

1. Cria a variavel `x` com valor `0`.
2. Calcula `(10 + 5) * 2`, resultando em `30`, e guarda em `y`.
3. Executa um laco `while` enquanto `x < 3`.
4. Dentro do laco, soma `1` ao valor de `x`.
5. Quando `x` chega em `3`, o laco para.
6. Imprime `y - x`, ou seja, `30 - 3`.

Resultado final:

```text
27
```

## Saida esperada no terminal

Ao escolher a opcao `2`, a saida deve ser parecida com esta:

```text
--- Codigo de entrada ---
x = 0
y = (10 + 5) * 2
while x < 3
x = x + 1
end
print(y - x)

--- Analise ---
Tokens reconhecidos: 31
AST gerada com sucesso.

--- Codigo intermediario ---
LOAD 0
STORE x
LOAD 10
PUSH
LOAD 5
ADD_STACK
PUSH
LOAD 2
MUL_STACK
STORE y
LABEL WHILE_START_1
LOAD x
PUSH
LOAD 3
LT_STACK
JZ WHILE_END_2
LOAD x
PUSH
LOAD 1
ADD_STACK
STORE x
JMP WHILE_START_1
LABEL WHILE_END_2
LOAD y
PUSH
LOAD x
SUB_STACK
PRINT_ACC

--- Resultado ---
27

--- Memoria ---
{'x': 3, 'y': 30}
```

## Explicacao por partes

### Codigo de entrada

Esta parte mostra o codigo MiniLang que sera analisado:

```text
x = 0
y = (10 + 5) * 2
while x < 3
x = x + 1
end
print(y - x)
```

Aqui o humano escreve em uma linguagem formal simples. O computador ainda nao executa diretamente esse texto; antes, ele precisa reconhecer, validar e traduzir.

### Analise

```text
Tokens reconhecidos: 31
AST gerada com sucesso.
```

Essa parte confirma duas etapas importantes.

Primeiro, a analise lexica conseguiu transformar o texto em tokens. Tokens sao unidades reconhecidas pela linguagem, como:

```text
ID, NUM, ASSIGN, PLUS, STAR, WHILE, END, PRINT
```

Isso esta relacionado a expressoes regulares e automatos finitos.

Depois, a analise sintatica conseguiu montar a AST, que e a arvore sintatica abstrata. Isso significa que o codigo respeita a gramatica da MiniLang.

Essa parte esta relacionada a gramaticas livres de contexto e automatos de pilha.

### Codigo intermediario

O codigo intermediario e uma traducao do programa MiniLang para instrucoes mais simples.

Por exemplo:

```text
LOAD 0
STORE x
```

significa:

```text
carregue o valor 0
guarde esse valor na variavel x
```

Outro trecho:

```text
LOAD 10
PUSH
LOAD 5
ADD_STACK
PUSH
LOAD 2
MUL_STACK
STORE y
```

representa:

```text
(10 + 5) * 2
```

O `PUSH` guarda temporariamente um valor na pilha. Depois, instrucoes como `ADD_STACK` e `MUL_STACK` pegam esse valor guardado e combinam com o valor atual do acumulador.

### Laco while

Este trecho representa o `while x < 3`:

```text
LABEL WHILE_START_1
LOAD x
PUSH
LOAD 3
LT_STACK
JZ WHILE_END_2
```

Ele funciona assim:

```text
marque o inicio do laco
carregue x
compare x < 3
se o resultado for falso, pule para o fim do laco
```

Depois vem o corpo do laco:

```text
LOAD x
PUSH
LOAD 1
ADD_STACK
STORE x
```

Isso representa:

```text
x = x + 1
```

No final:

```text
JMP WHILE_START_1
LABEL WHILE_END_2
```

O `JMP` volta para o inicio do laco. O `LABEL WHILE_END_2` marca o ponto para onde o programa pula quando a condicao fica falsa.

Essa parte mostra bem a ideia de execucao passo a passo, memoria, estado e repeticao.

### Resultado

```text
--- Resultado ---
27
```

Esse e o valor impresso pelo comando:

```text
print(y - x)
```

No final da execucao:

```text
y = 30
x = 3
```

Logo:

```text
y - x = 30 - 3 = 27
```

### Memoria

```text
--- Memoria ---
{'x': 3, 'y': 30}
```

Essa parte mostra o estado final da memoria do programa.

A variavel `x` terminou com valor `3`, porque foi incrementada dentro do `while`.

A variavel `y` terminou com valor `30`, porque recebeu o resultado de `(10 + 5) * 2`.

## Importancia para Teoria da Computacao

Essa saida demonstra varias etapas importantes:

- O lexer reconhece tokens usando expressoes regulares.
- O parser valida a gramatica e monta a AST.
- A analise semantica verifica se as variaveis foram definidas antes do uso.
- O gerador intermediario traduz a linguagem MiniLang para pseudo-assembly.
- O executor simula uma maquina simples com memoria, pilha, acumulador e saltos.

Por isso, a opcao `2` e uma boa opcao para apresentar o projeto: ela mostra um programa correto passando por todas as etapas de um compilador educacional.
