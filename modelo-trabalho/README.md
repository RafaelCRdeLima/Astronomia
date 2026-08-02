# Modelo de trabalho — Astronomia (AST0001)

Modelo em LaTeX no formato de artigo de revista científica: duas colunas,
logo da UDESC no alto à direita, título, resumo destacado e as seções
Introdução, Revisão Teórica, Dados e Discussão, Conclusão e Bibliografia.

## Arquivos

| Arquivo | Para que serve |
|---|---|
| `main.tex` | O modelo. É o único arquivo que você edita. |
| `udesc.png` | Logo do cabeçalho. Não renomeie. |
| `figura_exemplo.pdf` | Figura de exemplo, para ver como incluir gráficos. Substitua pela sua. |
| `main.pdf` | O resultado compilado, para conferência. |

## Como usar

**No Overleaf (mais simples):** crie um projeto novo, envie os três arquivos
(`main.tex`, `udesc.png`, `figura_exemplo.pdf`) e clique em *Recompile*.

**No seu computador:** com TeX Live ou MiKTeX instalado, rode duas vezes:

```
pdflatex main.tex
pdflatex main.tex
```

A segunda passagem resolve as referências cruzadas — números de equação, de
figura, de tabela e de citação. Se ainda aparecerem como `??`, rode mais uma vez.

## O que preencher

No início do `main.tex`, cinco linhas:

```latex
\newcommand{\titulo}{Título do trabalho: uma frase que diz o que foi medido}
\newcommand{\aluno}{Nome Completo do Aluno}
\newcommand{\email}{email@edu.udesc.br}
\newcommand{\tituloCurto}{Título curto para o cabeçalho}
\newcommand{\semestre}{2026/2}
```

O título curto aparece no cabeçalho das páginas seguintes, como em periódico.

## A estrutura, seção por seção

| Seção | O que se espera |
|---|---|
| **Resumo** | Um parágrafo de 120 a 200 palavras: contexto, o que foi feito, que dados, o resultado numérico com incerteza, e a conclusão em uma frase. Escrito por último, lido primeiro. |
| **Introdução** | Do que trata, por que importa, o que já se sabe (com citação) e qual pergunta este trabalho responde. |
| **Revisão Teórica** | Só as equações que serão usadas, com o significado de cada símbolo e as hipóteses assumidas. |
| **Dados e Discussão** | Origem dos dados, critério de seleção, tabelas e figuras, o resultado com incerteza e a comparação com o valor esperado. |
| **Conclusão** | O que o número significa, qual é a maior fonte de incerteza e o que melhoraria a medida. Sem resultado novo. |
| **Bibliografia** | Apenas o que foi consultado de fato. |

## Exemplos incluídos no arquivo

- equação numerada com rótulo, citada por `\eqref`;
- várias linhas alinhadas com `align`;
- equação sem numeração;
- matemática no meio do texto e unidades com `\SI{}{}`;
- tabela com `booktabs`, em uma coluna;
- figura em uma coluna, com legenda e rótulo;
- figura larga ocupando as duas colunas (`figure*`), comentada e pronta para usar;
- resultado apresentado com valor, incerteza e unidade;
- citações com `\cite` e lista de referências.

Os comentários do arquivo — linhas que começam com `%` — explicam cada comando
e o que se espera de cada seção. Pode apagá-los na versão final.

## Erros mais comuns

- **Acento aparece errado:** salve o arquivo em UTF-8.
- **Figura não aparece:** ela precisa estar na mesma pasta do `main.tex`, e o nome
  diferencia maiúsculas de minúsculas.
- **Referência vira `??`:** falta compilar uma segunda vez.
- **A figura foi parar em outra página:** é o comportamento normal de figuras
  flutuantes em duas colunas. O `[t]` pede o topo da página; use `figure*` para
  figuras largas, que sempre vão para o topo de uma página.
- **`Undefined control sequence`:** comando escrito errado ou pacote faltando;
  a mensagem indica a linha.
