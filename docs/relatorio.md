# Relatorio - Compilador Educacional MiniLang

## Objetivo

O projeto implementa um compilador educacional simplificado para a linguagem MiniLang. O compilador le um codigo de entrada, executa analise lexica, analise sintatica, analise semantica, gera codigo intermediario em pseudo-assembly e executa esse codigo.

Exemplo de entrada:

```text
x = 0
y = (10 + 5) * 2
while x < 3
x = x + 1
end
print(y - x)
```

Saida esperada:

```text
27
```

## Definicao da Linguagem MiniLang

A MiniLang possui uma instrucao por linha, variaveis simples, numeros inteiros, operadores aritmeticos, parenteses, comando `print()` e laco `while`.

Gramatica usada no parser:

```text
programa    -> instrucao*
instrucao   -> atribuicao | impressao | repeticao
atribuicao  -> ID "=" expressao
impressao   -> "print" "(" expressao ")"
repeticao   -> "while" comparacao instrucao* "end"
comparacao  -> expressao ("<" | ">" | "==") expressao
expressao   -> termo (("+" | "-") termo)*
termo       -> fator (("*" | "/") fator)*
fator       -> ID | NUM | "(" expressao ")"
```

## Analise Lexica - AFD e Expressoes Regulares

A etapa lexica transforma o codigo fonte em tokens. Ela identifica variaveis, numeros inteiros, operadores aritmeticos, comparadores, atribuicao, parenteses e palavras reservadas como `print`, `while` e `end`.

No projeto, essa etapa usa expressoes regulares em Python. O comportamento pode ser explicado como um Automato Finito Deterministico: o analisador percorre os caracteres da esquerda para a direita e, conforme o padrao reconhecido, chega a um estado final correspondente a um token.

Exemplo:

```text
y = (10 + 5) * 2
```

Tokens:

```text
ID(y), ASSIGN, LPAREN, NUM(10), PLUS, NUM(5), RPAREN, STAR, NUM(2)
```

## Analise Sintatica - Gramatica Livre de Contexto e PDA

A etapa sintatica valida a ordem dos tokens com base na gramatica da MiniLang. Ela aceita atribuicoes, impressoes de expressoes, parenteses e lacos `while` bem formados.

Exemplo valido:

```text
print((x + y) * 2)
```

Exemplo invalido:

```text
x = (10 + 5
```

Essa etapa se relaciona com Gramaticas Livres de Contexto porque a estrutura da linguagem e descrita por regras de producao. Tambem pode ser explicada por um Automato de Pilha, pois o parser precisa acompanhar estruturas aninhadas, como parenteses e blocos `while ... end`.

## Analise Semantica - Linguagem Sensivel ao Contexto

A etapa semantica verifica o significado do codigo. A regra principal implementada e: uma variavel so pode ser usada depois de ter sido definida.

Exemplo invalido:

```text
y = x + 5
```

Nesse caso, `x` ainda nao foi definido. Essa verificacao depende do contexto das linhas anteriores, por isso se relaciona com Linguagens Sensiveis ao Contexto.

## Codigo Intermediario

Depois das validacoes, o compilador gera pseudo-assembly. A versao atual usa acumulador, pilha e rotulos para representar expressoes e repeticoes.

Entrada:

```text
x = 0
y = (10 + 5) * 2
print(y - x)
```

Codigo intermediario simplificado:

```text
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
LOAD y
PUSH
LOAD x
SUB_STACK
PRINT_ACC
```

Essa representacao facilita a demonstracao da traducao feita pelo compilador antes da execucao.

## Execucao - Maquina de Turing

A etapa de execucao processa as instrucoes sequencialmente. Ela usa um acumulador, uma pilha, uma memoria de variaveis, rotulos de salto e uma lista de saidas.

Exemplo de memoria apos a execucao:

```text
x = 3
y = 30
```

Essa etapa se relaciona com a ideia de Maquina de Turing porque simula um processamento passo a passo, mantendo estado interno e atualizando a memoria ao longo da execucao.

## Como a Teoria da Computacao foi aplicada no projeto?

A Teoria da Computacao foi aplicada em todas as etapas do compilador. O lexer usa expressoes regulares e pode ser explicado como um AFD. O parser usa uma gramatica livre de contexto e valida a estrutura das instrucoes, relacionando-se com PDA. A analise semantica verifica regras que dependem do contexto, como variaveis previamente declaradas, aproximando-se de linguagens sensiveis ao contexto. Por fim, a execucao percorre instrucoes em sequencia, manipula memoria, pilha e saltos, representando a ideia de processamento de uma Maquina de Turing.

## Melhorias implementadas

- Expressoes com `+`, `-`, `*` e `/`.
- Precedencia de operadores.
- Parenteses em expressoes.
- `print(expressao)`.
- Laco `while` com comparadores `<`, `>` e `==`.
- Exibicao da AST no terminal.
- Indicador visual da coluna em mensagens de erro.
- Opcao no menu para explicar as etapas da compilacao.

## Exemplos para Apresentacao

Codigo valido:

```text
x = 0
y = (10 + 5) * 2
while x < 3
x = x + 1
end
print(y - x)
```

Erro lexico:

```text
y = x @ 5
```

Erro sintatico:

```text
x = (10 + 5
```

Erro semantico:

```text
y = x + 5
```
