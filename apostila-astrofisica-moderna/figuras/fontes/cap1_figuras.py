"""Figuras do Capítulo 1 -- Fundamentos observacionais e escalas de medida.

Todas são calculadas, não desenhadas à mão:

  esfera_celeste.pdf  (a) esfera celeste para Joimville (phi = -26,30 graus), com a
                          convenção de azimute explícita; (b) o triângulo PZX.
  sol_joinville.pdf   declinação solar, altura máxima, duração do dia e insolação
                          relativa ao longo do ano, para phi = -26,30 graus.
  equacao_tempo.pdf   as duas componentes da equação do tempo e sua soma.
  precessao.pdf       trajetória do polo celeste norte entre as estrelas em 26 000 anos.
  paralaxe.pdf        (a) geometria da paralaxe; (b) distância x paralaxe com marcos reais.
  extincao.pdf        (a) curva de extinção A_lambda/A_V; (b) vetor de avermelhamento
                          sobre o diagrama cor-magnitude real do Gaia.

Saída: PDF vetorial em ../ (pasta figuras/).
"""
import csv
import math
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, Polygon

NAVY, BLUE, CYAN, GOLD, MUTED, LINE = (
    "#14213D", "#2F6690", "#35A7B8", "#F2A541", "#667085", "#D8E2EC")
RED = "#C1666B"

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.normpath(os.path.join(AQUI, ".."))
DADOS = os.path.normpath(os.path.join(AQUI, "..", "..", "dados",
                                      "01_gaia_estrelas_25pc.csv"))
PHI = -26.30                      # latitude de Joinville
EPS = 23.4393                     # obliquidade J2000

plt.rcParams.update({"font.family": "serif", "font.serif": ["DejaVu Serif"],
                     "mathtext.fontset": "cm", "axes.linewidth": 0.8})
r = np.radians


def salvar(fig, nome):
    fig.savefig(os.path.join(SAIDA, nome), bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    print("  ", nome)


# ============================================================ 1. esfera celeste
def versor(azimute, altura):
    """Leste-Norte-Zenite a partir de azimute (do Norte para Leste) e altura."""
    a, h = r(azimute), r(altura)
    return np.array([np.cos(h) * np.sin(a), np.cos(h) * np.cos(a), np.sin(h)])


def arco(u, v, n=120):
    """Arco de círculo máximo entre dois versores (interpolação esférica)."""
    u, v = np.asarray(u, float), np.asarray(v, float)
    omega = np.arccos(np.clip(u @ v, -1, 1))
    t = np.linspace(0, 1, n)
    if omega < 1e-9:
        return np.tile(u, (n, 1))
    return (np.sin((1 - t)[:, None] * omega) * u
            + np.sin(t[:, None] * omega) * v) / np.sin(omega)


def circulo_maximo(polo, n=400):
    """Círculo máximo cujo polo é o versor dado."""
    polo = np.asarray(polo, float)
    a = np.array([0.0, 0.0, 1.0])
    if abs(polo @ a) > 0.95:
        a = np.array([1.0, 0.0, 0.0])
    e1 = np.cross(polo, a); e1 /= np.linalg.norm(e1)
    e2 = np.cross(polo, e1)
    t = np.linspace(0, 2 * np.pi, n)
    return np.cos(t)[:, None] * e1 + np.sin(t)[:, None] * e2


def camera(azimute, altura):
    """Base de projeção ortográfica para um observador fora da esfera."""
    vista = versor(azimute, altura)
    a = np.array([0.0, 0.0, 1.0])
    d = np.cross(vista, a); d /= np.linalg.norm(d)
    return vista, d, np.cross(d, vista)


CAM = camera(90.0, 16.0)          # olhando do Leste: meridiano no plano da página


def proj(p, cam=None):
    vista, d, cima = cam or CAM
    p = np.atleast_2d(np.asarray(p, float))
    return np.column_stack([p @ d, p @ cima]), p @ vista


def traco(ax, pts, cor, lw=1.2, ls="-", z=2, atras=True, label=None, cam=None):
    xy, prof = proj(pts, cam)
    vis = prof >= 0
    ax.plot(np.where(vis, xy[:, 0], np.nan), np.where(vis, xy[:, 1], np.nan),
            color=cor, lw=lw, ls=ls, zorder=z, label=label)
    if atras:
        ax.plot(np.where(~vis, xy[:, 0], np.nan), np.where(~vis, xy[:, 1], np.nan),
                color=cor, lw=lw * 0.7, ls=(0, (2, 2)), alpha=0.45, zorder=z)


def ponto(ax, p, cor, texto=None, dx=0.05, dy=0.05, ms=5.5, fs=8.5, ha="left", cam=None):
    xy, _ = proj(p, cam)
    ax.plot(xy[0, 0], xy[0, 1], "o", color=cor, ms=ms, zorder=6)
    if texto:
        ax.text(xy[0, 0] + dx, xy[0, 1] + dy, texto, fontsize=fs, color=cor,
                ha=ha, zorder=7)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.1, 3.5))

Z = versor(0, 90)                       # zênite
POLO = versor(180, abs(PHI))            # polo celeste sul, elevado de |phi|
NORTE, LESTE, SUL, OESTE = [versor(a, 0) for a in (0, 90, 180, 270)]
X = versor(122.7, 31.1)                 # estrela do exemplo
PE = versor(122.7, 0)                   # pé do círculo vertical

# câmera do painel (b): olhando para o centro do próprio triângulo
_c = POLO + Z + X; _c /= np.linalg.norm(_c)
_d = np.cross(_c, np.array([0.0, 0.0, 1.0])); _d /= np.linalg.norm(_d)
CAM_B = (_c, _d, np.cross(_d, _c))

for ax, titulo in ((ax1, "(a) a esfera celeste em Joinville"),
                   (ax2, "(b) o triângulo esférico $PZX$")):
    ax.add_patch(Circle((0, 0), 1.0, fc="#FBFCFE", ec=LINE, lw=0.9, zorder=0))
    ax.set_xlim(-1.30, 1.30); ax.set_ylim(-1.34, 1.24)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(titulo, fontsize=9.5, color=NAVY, pad=2)

# ---- (a)
traco(ax1, circulo_maximo(Z), MUTED, lw=1.3)                      # horizonte
traco(ax1, circulo_maximo(POLO), BLUE, lw=1.0)                    # equador celeste
traco(ax1, arco(NORTE, PE), GOLD, lw=2.4, atras=False, z=5)       # azimute
traco(ax1, arco(PE, X), CYAN, lw=2.4, atras=False, z=5)           # altura
traco(ax1, arco(Z, SUL), MUTED, lw=0.8, ls=(0, (4, 3)))           # meridiano
ponto(ax1, NORTE, MUTED, "N", -0.10, -0.02, ms=3.2, fs=8, ha="right")
ponto(ax1, SUL, MUTED, "S", 0.09, -0.02, ms=3.2, fs=8)
ponto(ax1, LESTE, MUTED, "L", 0.0, -0.13, ms=3.2, fs=8, ha="center")
ponto(ax1, Z, NAVY, "$Z$ zênite", 0.0, 0.07, ha="center")
ponto(ax1, POLO, BLUE, "$P$ polo sul celeste", -0.04, 0.09, ha="right")
ponto(ax1, X, RED, "$X$", 0.05, 0.03)
xy, _ = proj(versor(60, 0))
ax1.text(xy[0, 0], xy[0, 1] - 0.15, "$A_z$", fontsize=10, color=GOLD, ha="center")
xy, _ = proj(versor(122.7, 16))
ax1.text(xy[0, 0] + 0.07, xy[0, 1], "$h$", fontsize=10, color=CYAN)
xy, _ = proj(versor(180, 13))
ax1.text(xy[0, 0] + 0.07, xy[0, 1], r"$|\varphi|$", fontsize=8.5, color=BLUE)
ax1.text(0.0, -1.30, "azimute contado do Norte para Leste;\n"
                     "altura medida sobre o círculo vertical",
         fontsize=7.6, color=MUTED, ha="center", linespacing=1.35)

# ---- (b)
traco(ax2, circulo_maximo(Z), LINE, lw=0.7, atras=False, cam=CAM_B)
for u, v, cor in ((POLO, Z, BLUE), (POLO, X, GOLD), (Z, X, CYAN)):
    traco(ax2, arco(u, v), cor, lw=2.4, atras=False, z=4, cam=CAM_B)
ponto(ax2, Z, NAVY, "$Z$ zênite", 0.0, 0.08, ha="center", cam=CAM_B)
ponto(ax2, POLO, BLUE, "$P$ polo", 0.07, 0.02, ha="left", cam=CAM_B)
ponto(ax2, X, RED, "$X$ astro", -0.07, 0.05, ha="right", cam=CAM_B)
meio = lambda u, v: arco(u, v)[60]
vert, _ = proj(np.vstack([POLO, Z, X]), CAM_B)
centro = vert.mean(axis=0)
for u, v, rot, cor in ((POLO, Z, r"$90^\circ-\varphi$", BLUE),
                       (POLO, X, r"$90^\circ-\delta$", GOLD),
                       (Z, X, r"$90^\circ-h$", CYAN)):
    xy, _ = proj(meio(u, v), CAM_B)
    fora = xy[0] - centro
    fora = fora / np.linalg.norm(fora) * 0.20
    ax2.text(xy[0, 0] + fora[0], xy[0, 1] + fora[1], rot, fontsize=8.5,
             color=cor, ha="center", va="center")
xy, _ = proj(POLO, CAM_B)
ax2.text(xy[0, 0] + 0.05, xy[0, 1] + 0.19, "$H$", fontsize=11, color=NAVY)
ax2.text(0.0, -1.30, r"$\sin h=\sin\varphi\sin\delta+\cos\varphi\cos\delta\cos H$",
         fontsize=8.6, color=NAVY, ha="center")
salvar(fig, "esfera_celeste.pdf")


# ====================================================== 2. o Sol em Joinville
dia = np.arange(1, 366)
# declinação solar (Bourges): erro < 0,02 graus
g = r(360 / 365.24 * (dia - 80.0))
dec = np.degrees(np.arcsin(np.sin(r(EPS)) * np.sin(g + r(1.914) * np.sin(g - r(2.87)))))
hmax = 90 - np.abs(PHI - dec)
cosH0 = np.clip(-np.tan(r(PHI)) * np.tan(r(dec)), -1, 1)
H0 = np.degrees(np.arccos(cosH0))
duracao = 2 * H0 / 15.0
insol = np.sin(r(hmax))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.1, 2.9))
ax1.plot(dia, dec, color=GOLD, lw=1.8, label=r"declinação do Sol $\delta_\odot$")
ax1.plot(dia, hmax, color=BLUE, lw=1.8, label=r"altura máxima $h_{\max}$")
i_dez = int(np.argmax(hmax))
ax1.plot(dia[i_dez], hmax[i_dez], "o", color=BLUE, ms=4)
ax1.text(20, 68, r"$h_{\max}=87{,}1^\circ$ no solstício de dezembro:"
                 "\n" r"o Sol nunca chega ao zênite aqui, porque $|\varphi|>\varepsilon$",
         fontsize=6.6, color=MUTED, ha="left", linespacing=1.4)
ax1.axhline(0, color=LINE, lw=0.8)
ax1.set_ylabel("graus", fontsize=8.5)
ax1.set_ylim(-32, 100)
ax1.legend(fontsize=7.2, frameon=False, loc="center left", ncol=1)
ax1.set_title("(a) o Sol ao longo do ano", fontsize=9.5, color=NAVY)

ax2.plot(dia, duracao, color=BLUE, lw=1.8)
ax2.set_ylabel("duração do dia (h)", fontsize=8.5, color=BLUE)
ax2.tick_params(axis="y", labelcolor=BLUE)
ax2b = ax2.twinx()
ax2b.plot(dia, insol, color=GOLD, lw=1.8)
ax2b.set_ylabel(r"$\sin h_{\max}$  (fluxo por área ao meio-dia)",
                fontsize=8.5, color=GOLD)
ax2b.tick_params(axis="y", labelcolor=GOLD)
ax2.set_title("(b) os dois efeitos somam-se", fontsize=9.5, color=NAVY)

for ax in (ax1, ax2):
    ax.set_xlim(1, 365)
    ax.set_xticks([1, 80, 172, 266, 355])
    ax.set_xticklabels(["1 jan", "eq.\nmar", "sol.\njun", "eq.\nset", "sol.\ndez"],
                       fontsize=7.5)
    ax.grid(True, color=LINE, lw=0.6)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
ax2b.spines["top"].set_visible(False)
salvar(fig, "sol_joinville.pdf")


# ==================================================== 3. equação do tempo
lam = r(np.linspace(0, 360, 721))                    # longitude eclíptica
Man = lam - r(282.94)               # anomalia média (periélio em 282,94 graus)
e = 0.016709
comp_e = -2 * e * np.sin(Man) * 1440 / (2 * np.pi)
comp_o = np.tan(r(EPS / 2)) ** 2 * np.sin(2 * lam) * 1440 / (2 * np.pi)
total = comp_e + comp_o
dia_lam = (np.degrees(lam) / 360 * 365.24 + 80) % 365.24

ordem = np.argsort(dia_lam)
fig, ax = plt.subplots(figsize=(7.1, 2.9))
ax.plot(dia_lam[ordem], comp_e[ordem], color=BLUE, lw=1.3, ls=(0, (5, 2)),
        label=r"excentricidade  ($\pm7{,}7$ min, período anual)")
ax.plot(dia_lam[ordem], comp_o[ordem], color=CYAN, lw=1.3, ls=(0, (2, 2)),
        label=r"obliquidade  ($\pm9{,}9$ min, período semestral)")
ax.plot(dia_lam[ordem], total[ordem], color=GOLD, lw=2.2, label="soma: equação do tempo")
ax.axhline(0, color=LINE, lw=0.8)
i_max, i_min = np.argmax(total), np.argmin(total)
for i, txt, dy in ((i_max, "%+.1f min" % total[i_max], 1.4),
                   (i_min, "%+.1f min" % total[i_min], -3.6)):
    ax.plot(dia_lam[i], total[i], "o", color=GOLD, ms=4.5)
    ax.annotate(txt, (dia_lam[i], total[i] + dy), fontsize=7.5, color=NAVY,
                ha="center")
ax.set_xlim(1, 365); ax.set_ylim(-19, 24)
ax.set_xticks([1, 80, 172, 266, 355])
ax.set_xticklabels(["1 jan", "eq. mar", "sol. jun", "eq. set", "sol. dez"], fontsize=8)
ax.set_ylabel("Sol verdadeiro $-$ Sol médio (min)", fontsize=8.5)
ax.legend(fontsize=7.4, frameon=False, loc="upper left", ncol=1)
ax.grid(True, color=LINE, lw=0.6); ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
salvar(fig, "equacao_tempo.pdf")


# ========================================================= 4. precessão
def eq_para_ecl(ra, dec):
    a, d, ep = r(ra), r(dec), r(EPS)
    x = np.cos(d) * np.cos(a)
    y = np.cos(d) * np.sin(a) * np.cos(ep) + np.sin(d) * np.sin(ep)
    z = -np.cos(d) * np.sin(a) * np.sin(ep) + np.sin(d) * np.cos(ep)
    return np.degrees(np.arctan2(y, x)) % 360, np.degrees(np.arcsin(z))


ESTRELAS = [("Polaris", 37.9529, 89.2641, 1.98), ("Vega", 279.2347, 38.7837, 0.03),
            ("Thuban", 211.0973, 64.3758, 3.65), ("Deneb", 310.3580, 45.2803, 1.25),
            ("Kochab", 222.6764, 74.1555, 2.08), ("Alderamin", 319.6449, 62.5856, 2.45)]
PERIODO = 25772.0
fig, ax = plt.subplots(figsize=(4.6, 4.3))
th = np.linspace(0, 2 * np.pi, 400)
lon_polo = np.degrees(th)
lat_polo = np.full_like(lon_polo, 90 - EPS)


def plano(lon, lat):
    """projeção azimutal equidistante centrada no polo eclíptico norte."""
    raio = 90 - np.asarray(lat, float)
    a = r(np.asarray(lon, float))
    return raio * np.sin(a), raio * np.cos(a)


ax.plot(*plano(lon_polo, lat_polo), color=BLUE, lw=1.6, zorder=3)
for ano, rot in ((2000, "hoje"), (-2800, "2800 a.C."), (7500, "7500"),
                 (10200, "10 200"), (13700, "13 700")):
    lon = (90.0 - 50.3 / 3600 * (ano - 2000)) % 360
    x, y = plano(lon, 90 - EPS)
    ax.plot(x, y, "o", color=BLUE, ms=4.5, zorder=5)
    ax.annotate(rot, (x, y), textcoords="offset points", xytext=(5, 4),
                fontsize=7.5, color=BLUE)
for nome, ra, dec, mag in ESTRELAS:
    lo, la = eq_para_ecl(ra, dec)
    x, y = plano(lo, la)
    ax.plot(x, y, "*", color=GOLD, ms=16 - 2.6 * mag, zorder=6,
            markeredgecolor=NAVY, markeredgewidth=0.4)
    ax.annotate(nome, (x, y), textcoords="offset points", xytext=(6, -9),
                fontsize=7.5, color=NAVY)
ax.plot(0, 0, "+", color=MUTED, ms=9)
ax.annotate("polo da eclíptica", (0, 0), textcoords="offset points",
            xytext=(6, 4), fontsize=7.5, color=MUTED)
lim = EPS + 12
ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
ax.set_aspect("equal"); ax.axis("off")
ax.set_title("o polo celeste norte em 26 000 anos", fontsize=9.5, color=NAVY)
ax.text(0, -lim + 1.0, r"raio do círculo $=\varepsilon=23{,}44^\circ$;"
                       r"  $50{,}3''$ por ano", fontsize=7.6, color=MUTED, ha="center")
salvar(fig, "precessao.pdf")


# ========================================================== 5. paralaxe
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.1, 3.0),
                               gridspec_kw=dict(width_ratios=[1.0, 1.15]))
# (a) geometria
ax1.plot([0], [0], "o", color=GOLD, ms=11, zorder=4)
ax1.annotate("Sol", (0, 0), textcoords="offset points", xytext=(-16, -6),
             fontsize=8, color=NAVY, ha="right")
orb = np.linspace(0, 2 * np.pi, 200)
ax1.plot(np.cos(orb), 0.30 * np.sin(orb), color=LINE, lw=0.9)
for sinal, rot in ((1, "junho"), (-1, "dezembro")):
    ax1.plot(sinal, 0, "o", color=BLUE, ms=5, zorder=5)
    ax1.annotate(rot, (sinal, 0), textcoords="offset points",
                 xytext=(0, 9), fontsize=7.5, color=BLUE, ha="center")
ax1.annotate("", xy=(1, -0.42), xytext=(0, -0.42),
             arrowprops=dict(arrowstyle="<->", color=NAVY, lw=1.0))
ax1.text(0.5, -0.90, r"$a_\oplus=1$ UA", fontsize=8.5, color=NAVY, ha="center")
EST = (0.15, 3.5)
ax1.plot(*EST, "*", color=RED, ms=13, zorder=5)
ax1.annotate("estrela", EST, textcoords="offset points", xytext=(8, -2),
             fontsize=8, color=RED)
for sinal in (1, -1):
    ax1.plot([sinal, EST[0]], [0, EST[1]], color=MUTED, lw=0.8, ls=(0, (4, 3)))
ax1.plot([0, EST[0]], [0, EST[1]], color=NAVY, lw=1.0)
ax1.add_patch(Arc(EST, 2.2, 2.2, theta1=249, theta2=268, color=CYAN, lw=1.8))
ax1.text(EST[0] - 0.30, EST[1] - 1.42, "$p$", fontsize=11, color=CYAN)
ax1.text(0.9, 2.2, r"$\tan p=\dfrac{a_\oplus}{d}\simeq p$" "\n"
                   r"$d\,[\mathrm{pc}]=1/p\,['']$",
         fontsize=8.5, color=NAVY, ha="left")
ax1.set_xlim(-1.7, 2.7); ax1.set_ylim(-1.25, 4.2)
ax1.axis("off"); ax1.set_aspect("equal")
ax1.set_title("(a) a geometria", fontsize=9.5, color=NAVY)

# (b) distância x paralaxe, com marcos reais
p = np.logspace(-2, 3, 400)
ax2.plot(p, 1000 / p, color=BLUE, lw=1.8)
MARCOS = [(768.07, "Proxima", 6, 5), (379.21, "Sirius", -8, -14),
          (7.36, "Plêiades", 6, 5), (0.122, "centro galáctico", 8, 4),
          (5.89, "Antares", -8, -14)]
for pi, nome, dx, dy in MARCOS:
    ax2.plot(pi, 1000 / pi, "o", color=GOLD, ms=5, zorder=4)
    ax2.annotate(nome, (pi, 1000 / pi), textcoords="offset points",
                 xytext=(dx, dy), fontsize=7.5, color=NAVY,
                 ha="right" if dx < 0 else "left")
ax2.axvspan(1e-2, 0.02, color=RED, alpha=0.10)
ax2.text(0.0115, 1.3e2, "abaixo do\nlimite do Gaia", fontsize=7.0, color=RED)
ax2.set_xscale("log"); ax2.set_yscale("log")
ax2.set_xlabel("paralaxe $p$ (mas)", fontsize=8.5)
ax2.set_ylabel("distância $d$ (pc)", fontsize=8.5)
ax2.grid(True, which="major", color=LINE, lw=0.6); ax2.set_axisbelow(True)
for s in ("top", "right"):
    ax2.spines[s].set_visible(False)
ax2.set_title("(b) a régua e seus limites", fontsize=9.5, color=NAVY)
salvar(fig, "paralaxe.pdf")


# ========================================================== 6. extinção
BANDAS = [("U", 0.365, 1.531), ("B", 0.445, 1.324), ("V", 0.551, 1.000),
          ("R", 0.658, 0.748), ("I", 0.806, 0.482), ("J", 1.220, 0.282),
          ("H", 1.630, 0.175), ("K", 2.190, 0.112)]
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.1, 3.0))
inv = np.array([1 / b[1] for b in BANDAS])
raz = np.array([b[2] for b in BANDAS])
ax1.plot(inv, raz, "o-", color=BLUE, lw=1.4, ms=5)
for (nome, lam_b, _), x, y in zip(BANDAS, inv, raz):
    ax1.annotate(nome, (x, y), textcoords="offset points", xytext=(4, -9),
                 fontsize=8, color=NAVY)
ax1.axhline(1, color=MUTED, lw=0.8, ls=(0, (4, 3)))
ax1.set_xlabel(r"$1/\lambda\ (\mu\mathrm{m}^{-1})$", fontsize=8.5)
ax1.set_ylabel(r"$A_\lambda/A_V$", fontsize=8.5)
ax1.set_title(r"(a) a extinção cresce para o azul  ($R_V=3{,}1$)",
              fontsize=9.0, color=NAVY)
ax1.grid(True, color=LINE, lw=0.6); ax1.set_axisbelow(True)
for s in ("top", "right"):
    ax1.spines[s].set_visible(False)

linhas = list(csv.DictReader(open(DADOS)))
par = np.array([float(x["paralaxe_mas"]) for x in linhas])
Gm = np.array([float(x["G_mag"]) for x in linhas])
BR = np.array([float(x["BP_RP"]) for x in linhas])
dist = 1000 / par
MG = Gm - 5 * np.log10(dist) + 5
ax2.scatter(BR, MG, s=3, color=BLUE, alpha=0.35, lw=0)
AV = 3.0                                   # exagerado para ficar visível
E = 0.42 * AV                              # E(BP-RP)/A_V no sistema Gaia
ax2.add_patch(FancyArrowPatch((0.95, 5.9), (0.95 + E, 5.9 + 0.86 * AV),
                              arrowstyle="-|>", color=GOLD, lw=2.4,
                              mutation_scale=18, zorder=5))
ax2.text(0.95 + E + 0.18, 5.9 + 0.86 * AV, r"$A_V=3$ mag", fontsize=8.5,
         color=GOLD, va="center")
ax2.invert_yaxis()
ax2.set_xlabel(r"$G_{BP}-G_{RP}$", fontsize=8.5)
ax2.set_ylabel(r"$M_G$", fontsize=8.5)
ax2.set_title("(b) para onde a poeira desloca uma estrela", fontsize=9.0, color=NAVY)
ax2.grid(True, color=LINE, lw=0.6); ax2.set_axisbelow(True)
for s in ("top", "right"):
    ax2.spines[s].set_visible(False)
salvar(fig, "extincao.pdf")
print("pronto")
