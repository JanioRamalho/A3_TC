# Relatorio - Compilador Educacional MiniLang

## Objetivo

O projeto implementa um compilador educacional simplificado para a linguagem MiniLang. O compilador le um codigo de entrada, executa analise lexica, analise sintatica, analise semantica, gera codigo intermediario em pseudo-assembly e executa esse codigo.

Exemplo de entrada:

```text
x = 10
y = x + 5
print(y)
```

Saida esperada:

```text
15
```

## Definicao da Linguagem MiniLang

A MiniLang possui uma instrucao por linha, variaveis simples, numeros inteiros, operador de soma e comando `print()`.

Gramatica usada no parser:

```text
programa   -> instrucao*
instrucao  -> atribuicao | impressao
atribuicao -> ID "=" expressao
impressao  -> "print" "(" ID ")"
expressao  -> termo ("+" termo)?
termo      -> ID | NUM
```

## Analise Lexica - AFD e Expressoes Regulares

A etapa lexica transforma o codigo fonte em tokens. Ela identifica variaveis, numeros inteiros, operador `+`, atribuicao `=`, parenteses e o comando `print`.

No projeto, essa etapa usa expressoes regulares em Python. O comportamento pode ser explicado como um Autômato Finito Determinístico: o analisador percorre os caracteres da esquerda para a direita e, conforme o padrao reconhecido, chega a um estado final correspondente a um token.

Exemplo:

```text
x = 10 + 5
```

Tokens:

```text
ID(x), ASSIGN, NUM(10), PLUS, NUM(5)
```

## Analise Sintatica - Gramatica Livre de Contexto e PDA

A etapa sintatica valida a ordem dos tokens com base na gramatica da MiniLang. Ela aceita atribuicoes e comandos `print()` bem formados.

Exemplo valido:

```text
x = 10 + 5
```

Exemplo invalido:

```text
x 10 = + 5
```

Essa etapa se relaciona com Gramaticas Livres de Contexto porque a estrutura da linguagem e descrita por regras de producao. Tambem pode ser explicada por um Automato de Pilha, pois o parser acompanha a estrutura esperada da instrucao, especialmente chamadas como `print(y)`.

## Analise Semantica - Linguagem Sensivel ao Contexto

A etapa semantica verifica o significado do codigo. A regra principal implementada e: uma variavel so pode ser usada depois de ter sido definida.

Exemplo invalido:

```text
y = x + 5
```

Nesse caso, `x` ainda nao foi definido. Essa verificacao depende do contexto das linhas anteriores, por isso se relaciona com Linguagens Sensiveis ao Contexto.

## Codigo Intermediario

Depois das validacoes, o compilador gera pseudo-assembly.

Entrada:

```text
x = 10
y = x + 5
print(y)
```

Codigo intermediario:

```text
LOAD 10
STORE x
LOAD x
ADD 5
STORE y
PRINT y
```

Essa representacao facilita a demonstracao da traducao feita pelo compilador antes da execucao.

## Execucao - Maquina de Turing

A etapa de execucao processa as instrucoes sequencialmente. Ela usa um acumulador, uma memoria de variaveis e uma lista de saidas.

Exemplo de memoria apos a execucao:

```text
x = 10
y = 15
```

Essa etapa se relaciona com a ideia de Maquina de Turing porque simula um processamento passo a passo, mantendo estado interno e atualizando a memoria ao longo da execucao.

## Como a Teoria da Computacao foi aplicada no projeto?

A Teoria da Computacao foi aplicada em todas as etapas do compilador. O lexer usa expressoes regulares e pode ser explicado como um AFD. O parser usa uma gramatica livre de contexto e valida a estrutura das instrucoes, relacionando-se com PDA. A analise semantica verifica regras que dependem do contexto, como variaveis previamente declaradas, aproximando-se de linguagens sensiveis ao contexto. Por fim, a execucao percorre instrucoes em sequencia e manipula memoria, representando a ideia de processamento de uma Maquina de Turing.

## Exemplos para Apresentacao

Codigo valido:

```text
x = 10
y = x + 5
print(y)
```

Erro lexico:

```text
y = x @ 5
```

Erro sintatico:

```text
x 10 = + 5
```

Erro semantico:

```text
y = x + 5
```
