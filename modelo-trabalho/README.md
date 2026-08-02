# Modelo de trabalho / relatório — Astronomia (AST0001)

Modelo em LaTeX para os trabalhos e relatórios da disciplina, com capa da
UDESC e as quatro seções exigidas: Introdução, Teoria Básica, Dados e Conclusão.

## Arquivos

| Arquivo | Para que serve |
|---|---|
| `main.tex` | O modelo. É o único arquivo que você edita. |
| `udesc.png` | Logo usado na capa. Não renomeie. |
| `figura_exemplo.pdf` | Figura de exemplo, para você ver como incluir gráficos. Substitua pela sua. |
| `main.pdf` | O resultado compilado, para conferência. |

## Como usar

**No Overleaf (mais simples):** crie um projeto novo, envie os três arquivos
(`main.tex`, `udesc.png`, `figura_exemplo.pdf`) e clique em *Recompile*.

**No seu computador:** com uma distribuição LaTeX instalada (TeX Live ou MiKTeX),
rode duas vezes:

```
pdflatex main.tex
pdflatex main.tex
```

A segunda passagem é necessária para que as referências cruzadas — números de
equação, de figura e de tabela — apareçam corretamente. Se ainda estiverem como
`??`, rode mais uma vez.

## O que preencher

No início do `main.tex`, quatro linhas:

```latex
\newcommand{\aluno}{Nome Completo do Aluno}
\newcommand{\titulotrabalho}{Título do Trabalho}
\newcommand{\disciplina}{ASTRONOMIA (AST0001)}
\newcommand{\semestre}{2026/2}
```

Depois escreva o conteúdo nas quatro seções. Os comentários do arquivo — as
linhas que começam com `%` — explicam o que se espera de cada seção e como
fazer equações, tabelas, figuras e citações. Leia esses comentários: eles são
a parte mais útil do modelo. Você pode apagá-los na versão final.

## Exemplos incluídos

- equação numerada com rótulo e citação por `\eqref`;
- várias linhas alinhadas com `align`;
- equação sem numeração;
- matemática dentro do texto e unidades com `\SI{}{}`;
- tabela com `booktabs`, com legenda e rótulo;
- figura com `includegraphics`, com legenda e rótulo;
- como apresentar um resultado com valor, incerteza e unidade;
- lista de referências e citação com `\cite`.

## Erros mais comuns

- **Acento aparece errado:** salve o arquivo em UTF-8.
- **Figura não aparece:** o arquivo precisa estar na mesma pasta do `main.tex`,
  e o nome diferencia maiúsculas de minúsculas.
- **Referência vira `??`:** falta compilar uma segunda vez.
- **`Undefined control sequence`:** quase sempre um comando escrito errado ou
  um pacote que faltou no preâmbulo. A mensagem indica a linha.
