# Compilador Educacional MiniLang

Projeto desenvolvido para a A3 de Teoria da Computacao / Compiladores e Linguagens Formais.

O objetivo e implementar um compilador educacional simplificado em Python para uma linguagem chamada **MiniLang**. O projeto mostra, na pratica, as principais etapas de um compilador:

- Analise lexica
- Analise sintatica
- Analise semantica
- Geracao de codigo intermediario
- Execucao do codigo
- Integracao das etapas
- Interface em terminal
- Relatorio relacionando o projeto com Teoria da Computacao

## O que e a MiniLang?

A MiniLang e uma linguagem simples criada para demonstrar como um compilador funciona.

Ela permite:

- Criar variaveis
- Atribuir numeros inteiros
- Somar valores com o operador `+`
- Imprimir valores com `print()`

Exemplo valido:

```text
x = 10
y = x + 5
print(y)
```

Resultado esperado:

```text
15
```

## Sintaxe da Linguagem

A linguagem segue estas regras:

- Uma instrucao por linha
- Variaveis podem ter nomes como `x`, `y`, `total`, `idade`
- Numeros devem ser inteiros
- O operador disponivel e `+`
- O comando de saida e `print(variavel)`

Exemplos validos:

```text
x = 10
print(x)
```

```text
x = 10
y = x + 5
print(y)
```

```text
idade = 18
proxima_idade = idade + 1
print(proxima_idade)
```

Exemplos invalidos:

```text
x 10 = + 5
```

Motivo: a ordem dos tokens esta incorreta.

```text
y = x + 5
print(y)
```

Motivo: a variavel `x` foi usada antes de ser definida.

```text
x = 10 @ 5
```

Motivo: o caractere `@` nao pertence a linguagem.

## Como Executar

Na pasta do projeto, execute:

```bash
python main.py
```

O sistema abrira um menu:

```text
1. Digitar codigo MiniLang
2. Executar exemplo valido
3. Executar exemplo com erro lexico
4. Executar exemplo com erro sintatico
5. Executar exemplo com erro semantico
0. Sair
```

Para escrever seu proprio codigo, escolha a opcao `1`.

Exemplo de entrada:

```text
> x = 10
> y = x + 5
> print(y)
>
```

A linha vazia finaliza a digitacao e inicia a compilacao.

## Como Rodar os Testes

O projeto usa `unittest`, biblioteca padrao do Python.

Execute:

```bash
python -m unittest discover -s tests
```

Os testes cobrem:

- Codigo valido com atribuicao
- Codigo valido com soma
- Codigo valido com `print`
- Erro lexico
- Erro sintatico
- Erro semantico
- Geracao de codigo intermediario
- Execucao final

## Estrutura do Projeto

```text
A3_Teoria da Computacao/
├── main.py
├── minilang/
│   ├── tokens.py
│   ├── lexer.py
│   ├── parser.py
│   ├── semantic.py
│   ├── intermediate.py
│   ├── executor.py
│   ├── compiler.py
│   └── errors.py
├── examples/
│   ├── valido.min
│   ├── erro_lexico.min
│   ├── erro_sintatico.min
│   └── erro_semantico.min
├── tests/
└── docs/
    └── relatorio.md
```

## Como o Compilador Funciona

O fluxo completo fica em `minilang/compiler.py`.

```python
tokens = lexer(codigo)
ast = parser(tokens)
semantico(ast)
codigo_intermediario = gerar_codigo(ast)
resultado = executar(codigo_intermediario)
```

### 1. Analise Lexica

Arquivo: `minilang/lexer.py`

Essa etapa transforma o codigo fonte em tokens.

Entrada:

```text
x = 10
```

Saida:

```text
ID(x), ASSIGN, NUM(10)
```

Aqui entram as **expressoes regulares**. O usuario nao precisa escrever uma expressao regular na MiniLang. As expressoes regulares sao usadas internamente pelo compilador para reconhecer numeros, variaveis, operadores e parenteses.

Exemplos de padroes reconhecidos:

- Numeros: `10`, `25`, `100`
- Variaveis: `x`, `y`, `total`, `idade`
- Operador: `+`
- Atribuicao: `=`
- Comando: `print`

Relacao com Teoria da Computacao:

- Expressoes Regulares
- Automato Finito Deterministico, AFD

### 2. Analise Sintatica

Arquivo: `minilang/parser.py`

Essa etapa verifica se os tokens estao em uma ordem valida.

Exemplo valido:

```text
x = 10 + 5
```

Exemplo invalido:

```text
x 10 = + 5
```

Gramatica usada:

```text
programa   -> instrucao*
instrucao  -> atribuicao | impressao
atribuicao -> ID "=" expressao
impressao  -> "print" "(" ID ")"
expressao  -> termo ("+" termo)?
termo      -> ID | NUM
```

Relacao com Teoria da Computacao:

- Gramatica Livre de Contexto
- Automato de Pilha, PDA

### 3. Analise Semantica

Arquivo: `minilang/semantic.py`

Essa etapa verifica se o codigo faz sentido.

Principal regra:

- Uma variavel so pode ser usada depois de ser definida.

Exemplo invalido:

```text
y = x + 5
```

Nesse caso, `x` nao foi definido antes.

Relacao com Teoria da Computacao:

- Linguagem Sensivel ao Contexto, CSL

### 4. Codigo Intermediario

Arquivo: `minilang/intermediate.py`

Essa etapa transforma a AST em pseudo-assembly.

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

Essa etapa ajuda a mostrar que o compilador traduziu a linguagem MiniLang para uma representacao mais proxima de maquina.

### 5. Execucao

Arquivo: `minilang/executor.py`

Essa etapa executa o pseudo-assembly.

Ela usa:

- Um acumulador
- Uma memoria de variaveis
- Uma lista de saidas

Exemplo de memoria final:

```text
{'x': 10, 'y': 15}
```

Relacao com Teoria da Computacao:

- Maquina de Turing
- Processamento sequencial
- Memoria e mudanca de estado

## O Projeto Cumpre o Documento da A3?

Sim. O projeto cumpre os requisitos obrigatorios principais do documento.

| Requisito do documento | Onde foi implementado |
| --- | --- |
| Ler codigo de entrada | `main.py` |
| Analise lexica | `minilang/lexer.py` |
| Analise sintatica | `minilang/parser.py` |
| Analise semantica | `minilang/semantic.py` |
| Gerar codigo intermediario | `minilang/intermediate.py` |
| Executar o codigo | `minilang/executor.py` |
| Fluxo completo do compilador | `minilang/compiler.py` |
| Interface em terminal | `main.py` |
| Exibir tokens, erros e resultado | `main.py` |
| Relatorio obrigatorio | `docs/relatorio.md` |
| Exemplos validos e invalidos | `examples/` |
| Testes das etapas | `tests/` |

Tambem foram contemplados os conceitos teoricos pedidos:

| Conceito | Aplicacao no projeto |
| --- | --- |
| AFD | Reconhecimento de tokens no lexer |
| Expressoes Regulares | Padroes usados no lexer |
| Gramatica Livre de Contexto | Regras da linguagem no parser |
| PDA | Validacao estrutural da sintaxe |
| CSL | Verificacao de variaveis conforme contexto |
| Maquina de Turing | Execucao sequencial com memoria |

## Limitacoes Atuais

Esta versao foi feita para cumprir o escopo obrigatorio da A3. Por isso, a linguagem ainda e simples.

Limitacoes:

- Suporta apenas o operador `+`
- Nao possui `if`, `while` ou funcoes
- Nao possui numeros negativos digitados diretamente
- Nao possui comentarios no codigo MiniLang
- A expressao suporta uma soma simples, como `x + 5`

Essas limitacoes nao impedem a entrega, porque o documento pede uma linguagem educacional simplificada com variaveis, inteiros, operador `+` e `print()`.

## Exemplo Completo para Apresentacao

Codigo MiniLang:

```text
x = 10
y = x + 5
print(y)
```

Tokens:

```text
ID(x), ASSIGN, NUM(10), ID(y), ASSIGN, ID(x), PLUS, NUM(5), PRINT, LPAREN, ID(y), RPAREN
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

Resultado:

```text
15
```

Memoria final:

```text
{'x': 10, 'y': 15}
```

## Resposta Curta para a Apresentacao

O projeto aplica Teoria da Computacao porque cada etapa do compilador representa um conceito estudado. A analise lexica usa expressoes regulares e pode ser representada por um AFD. A analise sintatica usa uma gramatica livre de contexto e se relaciona com automatos de pilha. A analise semantica depende do contexto, pois verifica se variaveis ja foram declaradas. Por fim, a execucao processa instrucoes sequencialmente, alterando memoria, o que se relaciona com a ideia de Maquina de Turing.
