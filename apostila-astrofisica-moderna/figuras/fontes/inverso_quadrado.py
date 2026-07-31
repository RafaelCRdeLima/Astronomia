"""Lei do inverso do quadrado: a geometria e o caso solar.

Painel (a): construcao geometrica. A mesma energia atravessa areas que crescem
            com d^2, entao o fluxo cai com 1/d^2.
Painel (b): F = L_sol / (4 pi d^2) com L_sol = 3,828e26 W (IAU 2015), avaliado
            nas distancias medias dos planetas. O valor na Terra reproduz a
            constante solar medida, 1361 W/m^2.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

NAVY, BLUE, CYAN, GOLD, MUTED, LINE = "#14213D", "#2F6690", "#35A7B8", "#F2A541", "#667085", "#D8E2EC"
L_SOL, UA = 3.828e26, 1.495978707e11

PLANETAS = [("Mercúrio", 0.3871), ("Vênus", 0.7233), ("Terra", 1.0),
            ("Marte", 1.5237), ("Júpiter", 5.2026), ("Saturno", 9.5549),
            ("Urano", 19.2184), ("Netuno", 30.1104)]

plt.rcParams.update({"font.family": "serif", "font.serif": ["DejaVu Serif"],
                     "mathtext.fontset": "cm"})
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.4),
                               gridspec_kw=dict(width_ratios=[1.0, 1.15]))

# ------------------------------------------------------------------ painel (a)
def proj(x, y, z):
    """projecao obliqua simples de (x,y,z) no plano da pagina"""
    return x + 0.90 * y, z + 0.45 * y


def quadrado(d, k=0.28):
    w = k * d
    cantos = [(d, -w, -w), (d, w, -w), (d, w, w), (d, -w, w)]
    return [proj(*c) for c in cantos]


for d, cor, rot in [(3, CYAN, "$F/9$"), (2, BLUE, "$F/4$"), (1, GOLD, "$F$")]:
    pts = quadrado(d)
    ax1.add_patch(Polygon(pts, closed=True, facecolor=cor, alpha=0.22,
                          edgecolor=cor, lw=1.4, zorder=4 - d * 0.1))
    xs = [p[0] for p in pts]
    ax1.text(np.mean(xs), max(p[1] for p in pts) + 0.08, rot, ha="center",
             va="bottom", fontsize=9.5, color=NAVY, zorder=8)

for c in quadrado(3):
    ax1.plot([0, c[0]], [0, c[1]], color=MUTED, lw=0.7, ls="-", alpha=0.8, zorder=1)

ax1.scatter([0], [0], s=90, color=GOLD, edgecolor=NAVY, lw=1.0, zorder=9)
ax1.text(0, 0.22, "fonte", fontsize=8.5, color=NAVY, ha="center", va="bottom")

# regua de distancia
y0 = -1.45
ax1.annotate("", xy=(3.55, y0), xytext=(0, y0),
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
for d in (1, 2, 3):
    ax1.plot([d, d], [y0 - 0.09, y0 + 0.09], color=MUTED, lw=0.9)
    ax1.text(d, y0 - 0.20, "%d" % d, fontsize=8.5, color=MUTED, ha="center", va="top")
ax1.text(3.62, y0, "$d$", fontsize=9, color=MUTED, ha="left", va="center")
ax1.set_xlim(-0.55, 4.1)
ax1.set_ylim(-2.0, 1.7)
ax1.set_aspect("equal")
ax1.axis("off")
ax1.set_title("(a) por que $F\\propto d^{-2}$", fontsize=10, color=NAVY, pad=6)

# ------------------------------------------------------------------ painel (b)
d = np.logspace(np.log10(0.25), np.log10(45), 300)
F = L_SOL / (4 * np.pi * (d * UA) ** 2)
ax2.plot(d, F, color=BLUE, lw=2.0, zorder=3,
         label=r"$F=L_\odot/4\pi d^{\,2}$")

for nome, a in PLANETAS:
    f = L_SOL / (4 * np.pi * (a * UA) ** 2)
    ax2.scatter([a], [f], s=42, facecolor=GOLD, edgecolor=NAVY, lw=0.9, zorder=6)
    dx, ha = (-9, "right") if nome in ("Vênus", "Marte", "Saturno", "Netuno") else (9, "left")
    ax2.annotate(nome, xy=(a, f), xytext=(dx, -3), textcoords="offset points",
                 fontsize=8, color=NAVY, ha=ha, zorder=7)

ax2.axhline(1361.0, color=MUTED, lw=0.9, ls="--", zorder=2)
ax2.text(2.6, 1600, "constante solar medida: 1361 W/m$^2$", fontsize=7.8,
         color=MUTED, ha="left", va="bottom")

ax2.set_xscale("log")
ax2.set_yscale("log")
ax2.set_xlim(0.25, 45)
ax2.set_ylim(1.0, 3e4)
ax2.set_xlabel(r"distância ao Sol  $d$ (UA)", fontsize=9.5, color="#232323")
ax2.set_ylabel(r"fluxo recebido  $F$ (W/m$^2$)", fontsize=9.5, color="#232323")
ax2.set_title("(b) o Sol visto de cada planeta", fontsize=10, color=NAVY, pad=6)
ax2.grid(True, which="major", color=LINE, lw=0.6)
ax2.set_axisbelow(True)

from matplotlib.ticker import FixedLocator, FuncFormatter
fmt = FuncFormatter(lambda v, _: ("%g" % v).replace(".", ","))
ax2.xaxis.set_major_locator(FixedLocator([0.3, 1, 3, 10, 30]))
ax2.xaxis.set_minor_locator(FixedLocator([]))
ax2.xaxis.set_major_formatter(fmt)
ax2.tick_params(labelsize=8.5, colors=MUTED)
for s in ("top", "right"):
    ax2.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax2.spines[s].set_color(MUTED)
    ax2.spines[s].set_linewidth(0.8)
leg = ax2.legend(loc="upper right", fontsize=8.5, frameon=True, edgecolor=LINE,
                 framealpha=0.92)
leg.get_frame().set_linewidth(0.6)
for t in leg.get_texts():
    t.set_color("#232323")

for nome, a in PLANETAS:
    print(f"  {nome:9s} d={a:7.3f} UA  F={L_SOL/(4*np.pi*(a*UA)**2):9.2f} W/m2")

fig.tight_layout(w_pad=1.6)
fig.savefig("inverso_quadrado.pdf")
fig.savefig("inverso_quadrado.png", dpi=190)
print("ok")
