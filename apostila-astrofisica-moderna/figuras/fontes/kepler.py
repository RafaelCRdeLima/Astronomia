"""As leis de Kepler: a geometria da orbita e a terceira lei com dados reais.

Painel (a): orbita calculada resolvendo a equacao de Kepler M = E - e sen E,
            com x = a(cos E - e), y = a sqrt(1-e^2) sen E. Os dois setores
            sombreados correspondem ao mesmo intervalo de tempo P/8.
Painel (b): P^2 = 4 pi^2 a^3 / (G M) para os planetas do Sistema Solar e para
            os satelites galileanos de Jupiter. Semieixos e periodos: valores
            tabelados do JPL/NASA. A massa central sai do coeficiente da reta.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

NAVY, BLUE, CYAN, GOLD, MUTED, LINE = "#14213D", "#2F6690", "#35A7B8", "#F2A541", "#667085", "#D8E2EC"
G = 6.67430e-11
UA, ANO, DIA = 1.495978707e11, 3.15576e7, 86400.0
M_SOL = 1.98892e30

PLANETAS = [("Mercúrio", 0.38710, 0.240846), ("Vênus", 0.72333, 0.615198),
            ("Terra", 1.00000, 1.000017), ("Marte", 1.52368, 1.880848),
            ("Júpiter", 5.20260, 11.8618), ("Saturno", 9.55491, 29.4571),
            ("Urano", 19.21845, 84.0205), ("Netuno", 30.11039, 164.770)]
# satelites galileanos: semieixo em km, periodo em dias
LUAS = [("Io", 421800.0, 1.769138), ("Europa", 671100.0, 3.551181),
        ("Ganimedes", 1070400.0, 7.154553), ("Calisto", 1882700.0, 16.689017)]

plt.rcParams.update({"font.family": "serif", "font.serif": ["DejaVu Serif"],
                     "mathtext.fontset": "cm"})
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.5),
                               gridspec_kw=dict(width_ratios=[1.0, 1.1]))

# ------------------------------------------------------------------ painel (a)
a, e = 1.0, 0.55
b = a * np.sqrt(1 - e**2)


def pos(Mano):
    """resolve E - e sen E = M por Newton e devolve (x, y)"""
    E = np.array(Mano, dtype=float)
    for _ in range(60):
        E = E - (E - e * np.sin(E) - Mano) / (1 - e * np.cos(E))
    return a * (np.cos(E) - e), b * np.sin(E)


th = np.linspace(0, 2 * np.pi, 600)
ax1.plot(*pos(th), color=BLUE, lw=1.8, zorder=3)

for M0, cor in [(0.0, GOLD), (np.pi, CYAN)]:
    Ms = np.linspace(M0, M0 + 2 * np.pi / 6, 120)
    xs, ys = pos(Ms)
    setor = [(0, 0)] + list(zip(xs, ys))
    ax1.add_patch(Polygon(setor, closed=True, facecolor=cor, alpha=0.35,
                          edgecolor="none", zorder=2))

ax1.scatter([0], [0], s=110, facecolor=GOLD, edgecolor=NAVY, lw=1.0, zorder=6)
ax1.text(0.0, -0.16, "foco (Sol)", fontsize=8.5, color=NAVY, ha="center", va="top")
ax1.scatter([-2 * a * e], [0], s=16, facecolor="white", edgecolor=MUTED, lw=1.0, zorder=6)
ax1.text(-2 * a * e, 0.10, "foco vazio", fontsize=7.5, color=MUTED, ha="center", va="bottom")

# semieixo maior
ax1.annotate("", xy=(a - a * e, 0.0), xytext=(-a - a * e, 0.0),
             arrowprops=dict(arrowstyle="<->", color=MUTED, lw=0.9))
ax1.text(-0.52, 0.06, "$2a$", fontsize=9, color=MUTED, ha="center", va="bottom")

ax1.text(-0.5, -1.12, "os dois setores correspondem ao mesmo\nintervalo de tempo: áreas iguais",
         fontsize=8.5, color=MUTED, ha="center", va="top")
ax1.set_xlim(-2.05, 1.05)
ax1.set_ylim(-1.62, 1.0)
ax1.set_aspect("equal")
ax1.axis("off")
ax1.set_title("(a) órbita elíptica e a lei das áreas", fontsize=10, color=NAVY, pad=6)

# ------------------------------------------------------------------ painel (b)
ap = np.array([p[1] for p in PLANETAS])
Pp = np.array([p[2] for p in PLANETAS])
al = np.array([l[1] * 1e3 / UA for l in LUAS])
Pl = np.array([l[2] * DIA / ANO for l in LUAS])


def massa_central(a_ua, P_ano):
    """M = 4 pi^2 a^3 / (G P^2), media geometrica sobre os corpos"""
    m = 4 * np.pi**2 * (a_ua * UA) ** 3 / (G * (P_ano * ANO) ** 2)
    return np.exp(np.mean(np.log(m)))


Ms, Mj = massa_central(ap, Pp), massa_central(al, Pl)
print("massa central pelos planetas: %.4e kg  (%.3f M_sol)" % (Ms, Ms / M_SOL))
print("massa central pelas luas:     %.4e kg  (1/%.0f M_sol)" % (Mj, M_SOL / Mj))

for a_ua, P_ano, cor, lab, M in [(ap, Pp, BLUE, "planetas: $M=1{,}00\\,M_\\odot$", Ms),
                                 (al, Pl, GOLD, "luas de Júpiter: $M=M_\\odot/1047$", Mj)]:
    xx = np.logspace(np.log10(a_ua.min() / 2.2), np.log10(a_ua.max() * 2.2), 50)
    yy = np.sqrt(4 * np.pi**2 * (xx * UA) ** 3 / (G * M)) / ANO
    ax2.plot(xx, yy, color=cor, lw=1.4, ls="--", zorder=3)
    ax2.scatter(a_ua, P_ano, s=40, facecolor=cor, edgecolor=NAVY, lw=0.8,
                zorder=5, label=lab)

for (nome, a_ua, P_ano) in [("Mercúrio", 0.3871, 0.240846), ("Terra", 1.0, 1.000017),
                            ("Júpiter", 5.2026, 11.8618), ("Netuno", 30.11, 164.77)]:
    ax2.annotate(nome, xy=(a_ua, P_ano), xytext=(6, -9), textcoords="offset points",
                 fontsize=7.8, color=NAVY)
ax2.annotate("Io", xy=(al[0], Pl[0]), xytext=(-6, 4), textcoords="offset points",
             fontsize=7.8, color=NAVY, ha="right")
ax2.annotate("Calisto", xy=(al[3], Pl[3]), xytext=(6, -8), textcoords="offset points",
             fontsize=7.8, color=NAVY)

ax2.text(0.03, 0.97, "mesma inclinação $3/2$ nas duas famílias:\n"
         "$P^2\\propto a^3$.\nO coeficiente é que mede\na massa central",
         transform=ax2.transAxes, fontsize=8, color=MUTED, ha="left", va="top")

ax2.set_xscale("log")
ax2.set_yscale("log")
ax2.set_xlabel(r"semieixo maior  $a$ (UA)", fontsize=9.5, color="#232323")
ax2.set_ylabel(r"período  $P$ (anos)", fontsize=9.5, color="#232323")
ax2.set_title("(b) terceira lei com dados reais", fontsize=10, color=NAVY, pad=6)
ax2.grid(True, which="major", color=LINE, lw=0.6)
ax2.set_axisbelow(True)
ax2.tick_params(labelsize=8.5, colors=MUTED)
for s in ("top", "right"):
    ax2.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax2.spines[s].set_color(MUTED)
    ax2.spines[s].set_linewidth(0.8)
leg = ax2.legend(loc="lower right", fontsize=7.6, frameon=True, edgecolor=LINE,
                 framealpha=0.93)
leg.get_frame().set_linewidth(0.6)
for t in leg.get_texts():
    t.set_color("#232323")

fig.tight_layout(w_pad=1.6)
fig.savefig("kepler.pdf")
fig.savefig("kepler.png", dpi=190)
print("ok")
