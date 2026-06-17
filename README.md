# Compilador Educacional MiniLang

Projeto da A3 de **Teoria da Computação** e **Compiladores e Linguagens Formais**.

O objetivo é mostrar, de forma simples, como um compilador funciona: ele lê um código, analisa, valida, traduz para código intermediário e executa.

## O que o projeto faz

O projeto implementa uma linguagem simples chamada **MiniLang**.

Ela permite:

- variáveis;
- números inteiros;
- operações `+`, `-`, `*` e `/`;
- parênteses em expressões;
- `print(expressao)`;
- laço `while`;
- comparadores `<`, `>` e `==`.

Exemplo:

```text
x = 0
y = (10 + 5) * 2
while x < 3
x = x + 1
end
print(y - x)
```

Saída esperada:

```text
27
```

Memória final:

```text
{'x': 3, 'y': 30}
```

## Como executar

Na raiz do projeto:

```powershell
python main.py
```

O menu possui:

```text
1. Digitar codigo MiniLang
2. Executar exemplo valido
3. Executar exemplo com erro lexico
4. Executar exemplo com erro sintatico
5. Executar exemplo com erro semantico
6. Explicar etapas da compilacao
0. Sair
```

## Etapas do compilador

O fluxo principal está em `minilang/compiler.py`:

```python
tokens = lexer(codigo)
ast = parser(tokens)
semantico(ast)
codigo_intermediario = gerar_codigo(ast)
resultado = executar(codigo_intermediario)
```

Cada etapa fica em um arquivo:

| Etapa | Arquivo | Função |
|---|---|---|
| Tokens | `tokens.py` | Define os tipos de tokens |
| Léxico | `lexer.py` | Transforma código em tokens |
| Sintático | `parser.py` | Valida a gramática e gera a AST |
| Semântico | `semantic.py` | Verifica uso correto de variáveis |
| Intermediário | `intermediate.py` | Gera pseudo-assembly |
| Execução | `executor.py` | Executa o pseudo-assembly |
| Integração | `compiler.py` | Junta todas as etapas |
| Interface | `main.py` | Menu do terminal |

## Conceitos usados no projeto

O projeto aplica os principais conceitos de Teoria da Computação em partes diferentes do compilador.

### Expressões regulares e AFD

Arquivo:

```text
minilang/lexer.py
```

O lexer usa a variável `TOKEN_REGEX` para reconhecer padrões da linguagem, como variáveis, números, operadores e palavras reservadas.

Essa etapa pode ser relacionada a um **Autômato Finito Determinístico**, pois o código é lido da esquerda para a direita e cada padrão reconhecido gera um token.

### Tokens

Arquivo:

```text
minilang/tokens.py
```

Define os tipos de tokens usados pela linguagem, como:

```text
ID, NUM, PLUS, PRINT, WHILE, END, EOF
```

Esses tokens são a entrada da próxima etapa, o parser.

### Gramática Livre de Contexto e Autômato de Pilha

Arquivo:

```text
minilang/parser.py
```

O parser verifica se os tokens seguem a estrutura correta da MiniLang.

Ele valida, por exemplo:

```text
x = 10
print(x + 5)
while x < 3
...
end
```

Essa etapa representa uma **Gramática Livre de Contexto**. O conceito de **Autômato de Pilha** aparece no controle de estruturas aninhadas, como parênteses e blocos `while/end`.

### AST

Arquivo:

```text
minilang/parser.py
```

Além de validar a estrutura, o parser monta uma **AST**.

AST significa **Árvore Sintática Abstrata**. Ela representa a organização lógica do código antes da geração do código intermediário.

### Linguagem Sensível ao Contexto

Arquivo:

```text
minilang/semantic.py
```

A análise semântica verifica regras que dependem do contexto.

Exemplo:

```text
y = x + 5
```

Esse código é estruturalmente válido, mas está semanticamente errado se `x` ainda não foi definido.

### Código intermediário

Arquivo:

```text
minilang/intermediate.py
```

Transforma a AST em pseudo-assembly.

Exemplo:

```text
LOAD 10
STORE x
```

Essa etapa mostra a tradução da linguagem MiniLang para instruções mais simples.

### Máquina de Turing

Arquivo:

```text
minilang/executor.py
```

O executor processa o pseudo-assembly passo a passo.

Ele usa:

- memória;
- pilha;
- acumulador;
- rótulos;
- saltos.

Essa execução sequencial representa, de forma simplificada, a ideia de uma **Máquina de Turing**.

### Integração das etapas

Arquivo:

```text
minilang/compiler.py
```

Esse arquivo junta todas as etapas:

```text
lexer -> parser -> semântico -> código intermediário -> execução
```

## Como cada etapa funciona

### 1. Análise léxica

Arquivo:

```text
minilang/lexer.py
```

Recebe o código como texto e transforma em tokens.

Exemplo:

```text
x = 10 + 5
```

Vira algo como:

```text
ID(x), ASSIGN, NUM(10), PLUS, NUM(5)
```

Essa etapa demonstra **expressões regulares** e **Autômato Finito Determinístico**.

### 2. Análise sintática

Arquivo:

```text
minilang/parser.py
```

Verifica se os tokens estão na ordem correta e monta a AST.

Exemplo válido:

```text
print(x + y)
```

Exemplo inválido:

```text
x = (10 + 5
```

Essa etapa demonstra **Gramática Livre de Contexto** e, conceitualmente, **Autômato de Pilha**.

### 3. Análise semântica

Arquivo:

```text
minilang/semantic.py
```

Verifica se o código faz sentido.

Exemplo inválido:

```text
y = x + 5
```

Nesse caso, `x` foi usado antes de ser definido.

Essa etapa demonstra uma regra dependente de contexto.

### 4. Código intermediário

Arquivo:

```text
minilang/intermediate.py
```

Traduz a AST para pseudo-assembly.

Exemplo:

```text
y = (10 + 5) * 2
```

Pode gerar:

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

### 5. Execução

Arquivo:

```text
minilang/executor.py
```

Executa o pseudo-assembly usando:

- memória;
- pilha;
- acumulador;
- rótulos;
- saltos.

Essa etapa representa a ideia de **processamento sequencial**, associada à **Máquina de Turing**.

## Exemplos disponíveis

Os exemplos ficam na pasta `examples/`:

```text
valido.min
erro_lexico.min
erro_sintatico.min
erro_semantico.min
```

Eles demonstram:

- execução correta;
- erro léxico;
- erro sintático;
- erro semântico.

## Testes

Os testes ficam na pasta `tests/`.

Para executar:

```powershell
python -m unittest discover -s tests
```

## Resposta obrigatória

**Como a Teoria da Computação foi aplicada no projeto?**

A Teoria da Computação foi aplicada em todas as etapas do compilador MiniLang. A análise léxica usa expressões regulares e pode ser relacionada a Autômatos Finitos Determinísticos. A análise sintática usa uma gramática para validar a estrutura do código, relacionando-se com Gramáticas Livres de Contexto e Autômatos de Pilha. A análise semântica verifica regras dependentes de contexto, como impedir o uso de variáveis antes de sua definição. Depois, o código é traduzido para pseudo-assembly e executado passo a passo com memória, pilha, acumulador e saltos, representando a ideia de Máquina de Turing.

## Conclusão

O projeto cumpre o objetivo de demonstrar um compilador educacional completo, com análise léxica, sintática, semântica, geração de código intermediário, execução e relação direta com os conceitos de Teoria da Computação.
