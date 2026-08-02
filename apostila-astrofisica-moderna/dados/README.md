# Dados reais para os laboratórios da apostila

Todos os arquivos são CSV com **vírgula** separando campos e **ponto** como separador
decimal — o formato que Excel, LibreOffice, Python (`pandas.read_csv`) e Mathematica
(`Import`) leem sem ajuste. Nenhum arquivo passa de 1 MB.

Cada arquivo corresponde a um laboratório descrito na apostila, no capítulo indicado.
Os dados **não foram simulados nem retocados**: vieram dos arquivos públicos citados
na coluna de origem, com no máximo um recorte de faixa e um filtro de qualidade.

| Arquivo | Capítulo | Conteúdo | Origem |
|---|---|---|---|
| `01_gaia_estrelas_25pc.csv` | 1 e 5 | 2000 estrelas com paralaxe > 40 mas (d < 25 pc): posição, paralaxe e erro, movimento próprio, velocidade radial, magnitude G e cor BP−RP | ESA Gaia DR3, via TAP |
| `02_terceira_lei_kepler.csv` | 2 | Semieixo maior e período de 21 corpos: planetas do Sol, luas de Júpiter, luas de Saturno e a Lua | valores tabelados JPL/NASA |
| `03_espectro_solar.csv` | 3 | Irradiância espectral solar medida acima da atmosfera, 200–2400 nm, passo de 0,5 nm | WHI reference spectrum, LASP/LISIRD |
| `05_estrelas_massa_raio_teff.csv` | 5 | 581 estrelas de binárias eclipsantes destacadas: massa, raio e temperatura efetiva medidos | Eker et al. 2018, MNRAS 479, 5491 (VizieR) |
| `07_pulsares_atnf.csv` | 7 | 2052 pulsares com período e derivada do período medidos | ATNF Pulsar Catalogue (VizieR B/psr) |
| `08_gw150914_strain.csv` | 8 | 2,8 s de tensão (*strain*) dos detectores H1 e L1 em torno de GW150914, 4096 amostras/s | GWOSC (LIGO Open Science Center) |
| `09_planetas_sistema_solar.csv` | 9 | Distância, raio, massa, albedo de Bond e temperatura média medida dos oito planetas | NASA Planetary Fact Sheet |
| `10a_exoplanetas_massa_raio.csv` | 10 | 1035 exoplanetas com massa e raio medidos e respectivas incertezas | NASA Exoplanet Archive (`pscomppars`) |
| `10b_transito_kepler.csv` | 10 | Curvas de luz dobradas de HAT-P-7 b e Kepler-10 b, cadência de 1 min | arquivo público do Kepler (MAST) |
| `11_curvas_rotacao_sparc.csv` | 11 | Curvas de rotação de 176 galáxias: raio, velocidade observada e contribuições de gás, disco e bojo | SPARC, Lelli et al. 2016 (VizieR) |
| `13_supernovas_ia_pantheon.csv` | 13 e 16 | 1573 supernovas Ia: desvio para o vermelho, módulo de distância e incerteza | Pantheon+ / SH0ES data release |
| `19_zona_habitavel.csv` | 19 | 5557 exoplanetas com semieixo maior, raio e luminosidade da estrela hospedeira | NASA Exoplanet Archive (`pscomppars`) |

## Como usar

No Excel ou LibreOffice: abra o arquivo diretamente. Se a coluna vier toda em uma
célula, use *Dados → Texto para colunas*, separador vírgula.

Em Python:

```python
import pandas as pd
df = pd.read_csv("05_estrelas_massa_raio_teff.csv")
```

No Mathematica:

```mathematica
dados = Import["05_estrelas_massa_raio_teff.csv", "Dataset", HeaderLines -> 1]
```

## Reprodutibilidade

Os scripts que geraram e filtraram estes arquivos, junto com os que produzem as
figuras da apostila, estão em `figuras/fontes/` no repositório do curso. Nenhum
arquivo aqui depende de credencial: todas as fontes são públicas e podem ser
baixadas de novo pelos endereços citados acima.
