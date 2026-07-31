"""Diagrama massa-raio de exoplanetas com massa e raio medidos.

Dados: NASA Exoplanet Archive, tabela pscomppars (consulta TAP), planetas com
massa verdadeira (nao M sin i) e raio medidos, ambos com precisao melhor que
25% em massa e 10% em raio. As curvas de densidade constante vem apenas de
R = (3M/4 pi rho)^(1/3), sem nenhum modelo de interior.
"""
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NAVY, BLUE, CYAN, GOLD, MUTED, LINE = "#14213D", "#2F6690", "#35A7B8", "#F2A541", "#667085", "#D8E2EC"
M_TERRA, R_TERRA = 5.9722e24, 6.371e6      # kg, m

nome, M, R = [], [], []
with open("massa_raio.csv") as fh:
    for row in csv.DictReader(fh):
        try:
            m, r = float(row["pl_bmasse"]), float(row["pl_rade"])
            em = abs(float(row["pl_bmasseerr1"] or 0))
            er = abs(float(row["pl_radeerr1"] or 0))
        except ValueError:
            continue
        if row["discoverymethod"] not in ("Transit", "Radial Velocity"):
            continue
        if em == 0 or er == 0 or em / m > 0.25 or er / r > 0.10:
            continue
        nome.append(row["pl_name"])
        M.append(m)
        R.append(r)
M, R = np.array(M), np.array(R)
print("planetas no grafico:", len(M))

SISTEMA_SOLAR = [
    ("Mercúrio", 0.0553, 0.383, (9, -2)), ("Vênus", 0.815, 0.949, (-6, 8)),
    ("Terra", 1.0, 1.0, (8, -3)), ("Marte", 0.107, 0.532, (8, -3)),
    ("Urano", 14.54, 3.98, (-8, 7)), ("Netuno", 17.15, 3.86, (7, -9)),
    ("Saturno", 95.16, 9.14, (-6, 8)), ("Júpiter", 317.8, 11.21, (8, 2)),
]

plt.rcParams.update({"font.family": "serif", "font.serif": ["DejaVu Serif"],
                     "mathtext.fontset": "cm"})
fig, ax = plt.subplots(figsize=(6.6, 5.0))

# curvas de densidade constante: R = (3M / 4 pi rho)^(1/3)
mm = np.logspace(np.log10(0.03), np.log10(6000), 200)
for rho, rot in [(10.0, r"$\rho=10$"), (5.51, r"$\rho=5{,}5$ (Terra)"),
                 (1.0, r"$\rho=1$ g/cm$^3$ (água)")]:
    rr = ((3 * mm * M_TERRA) / (4 * np.pi * rho * 1000)) ** (1 / 3) / R_TERRA
    ax.plot(mm, rr, color=MUTED, lw=0.9, ls=":", zorder=2)
    xl = 0.30
    yl = ((3 * xl * M_TERRA) / (4 * np.pi * rho * 1000)) ** (1 / 3) / R_TERRA
    ax.text(xl, yl * 1.06, rot, fontsize=7.5, color=MUTED, ha="left",
            va="bottom", rotation=33, rotation_mode="anchor", zorder=5)

ax.scatter(M, R, s=13, color=BLUE, alpha=0.45, lw=0, zorder=3,
           label="exoplanetas com massa e raio medidos ($n=%d$)" % len(M))

for nm, m, r, off in SISTEMA_SOLAR:
    ax.scatter([m], [r], s=52, marker="o", facecolor=GOLD, edgecolor=NAVY,
               lw=0.9, zorder=6)
    ax.annotate(nm, xy=(m, r), xytext=off, textcoords="offset points",
                fontsize=8, color=NAVY,
                ha="right" if off[0] < 0 else "left", zorder=7)
ax.scatter([], [], s=52, marker="o", facecolor=GOLD, edgecolor=NAVY, lw=0.9,
           label="planetas do Sistema Solar")

ax.annotate("acima de $\\sim\\!100\\,M_\\oplus$ o raio quase não cresce:\n"
            "a matéria degenerada resiste à compressão",
            xy=(1800, 12.2), xytext=(4.0, 22.0), fontsize=8, color=MUTED, ha="left",
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9,
                            connectionstyle="arc3,rad=-0.12"))

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(0.04, 8000)
ax.set_ylim(0.35, 30)
ax.set_xlabel(r"massa  $M/M_\oplus$", fontsize=10.5, color="#232323")
ax.set_ylabel(r"raio  $R/R_\oplus$", fontsize=10.5, color="#232323")
ax.grid(True, which="major", color=LINE, lw=0.6)
ax.set_axisbelow(True)

from matplotlib.ticker import FixedLocator, FuncFormatter
fmt = FuncFormatter(lambda v, _: ("%g" % v).replace(".", ","))
ax.xaxis.set_major_locator(FixedLocator([0.1, 1, 10, 100, 1000]))
ax.yaxis.set_major_locator(FixedLocator([0.5, 1, 2, 5, 10, 20]))
ax.yaxis.set_minor_locator(FixedLocator([]))
ax.xaxis.set_major_formatter(fmt)
ax.yaxis.set_major_formatter(fmt)
ax.tick_params(labelsize=9, colors=MUTED)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(MUTED)
    ax.spines[s].set_linewidth(0.8)

leg = ax.legend(loc="lower right", fontsize=8.5, frameon=True, edgecolor=LINE,
                framealpha=0.93)
leg.get_frame().set_linewidth(0.6)
for t in leg.get_texts():
    t.set_color("#232323")

fig.tight_layout()
fig.savefig("massa_raio.pdf")
fig.savefig("massa_raio.png", dpi=190)
print("ok")
