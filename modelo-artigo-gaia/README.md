# Artigo do projeto do Gaia — Capítulo 3

Esqueleto do artigo do **projeto do Capítulo 3**, no modelo de artigo da
disciplina: a vizinhança solar medida com o catálogo do Gaia.

## O que tem aqui

    main.tex                     o esqueleto, com as seções, as equações e os
                                 comentários dizendo o que cada parte cobra
    main.pdf                     como fica compilado
    udesc.png                    logotipo do cabeçalho
    figuras/diagrama_hr.pdf      EXEMPLO, feito com os dados reais do arquivo
    figuras/completeza.pdf       EXEMPLO — substitua pelos seus

As duas figuras são exemplos, para o modelo compilar de saída. **Troque as
duas pelas suas**: elas são o resultado do seu trabalho, não do meu.

## Diferença para os outros capítulos

Nos laboratórios dos Capítulos 1, 2 e 4 o painel gera o `main.tex` já
preenchido com os seus dados. Aqui não há painel: o projeto do Gaia é um CSV
que você analisa no Excel ou em Python. O que este pacote entrega é o
esqueleto certo — as seções que o capítulo pede, na ordem certa, com os
lugares das figuras e das tabelas já referenciados no texto.

## Como usar

1. Baixe o `.zip`, descompacte e envie a pasta inteira ao Overleaf.
2. Preencha os campos marcados `PREENCHA` no topo do `main.tex`.
3. Substitua as duas figuras de exemplo pelas suas.
4. Escreva. Os comentários `%` dizem o que cada seção precisa conter — pode
   apagá-los na versão final.
5. Compile com pdfLaTeX **duas vezes**: a segunda resolve as referências.

## O arquivo de dados

`01_gaia_estrelas_25pc.csv`, em
<https://rafaelcrdelima.github.io/Astronomia/apostila-astrofisica-moderna/dados/>

O roteiro passo a passo está no Capítulo 3 da apostila.
