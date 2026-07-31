"""Relacao massa-luminosidade da sequencia principal.

Dados: Eker et al. (2018), MNRAS 479, 5491 - tabela 1 (VizieR J/MNRAS/479/5491/table1),
componentes de binarias eclipsantes destacadas com massas e raios medidos.
L/Lsun calculado por L = 4 pi R^2 sigma Teff^4, com Teff,sun = 5772 K (IAU 2015).
"""
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NAVY, BLUE, CYAN, GOLD, MUTED, LINE = "#14213D", "#2F6690", "#35A7B8", "#F2A541", "#667085", "#D8E2EC"
TEFF_SUN = 5772.0

rows = []
with open("eker2018.tsv") as fh:
    for line in fh:
        if line.startswith(("#", "\n")):
            continue
        parts = [p.strip() for p in line.split("\t")]
        if len(parts) < 5 or parts[0] in ("Name", "") or parts[0].startswith("---"):
            continue
        try:
            rows.append((float(parts[2]), float(parts[3]), float(parts[4])))
        except ValueError:
            continue

M, R, T = np.array(rows).T
sel = (M >= 0.179) & (M <= 31.0)          # faixa de sequencia principal de Eker et al. (2018)
M, R, T = M[sel], R[sel], T[sel]
L = R**2 * (T / TEFF_SUN) ** 4
print(f"{len(M)} estrelas | M: {M.min():.3f}-{M.max():.1f} Msun | L: {L.min():.2e}-{L.max():.1e} Lsun")

x, y = np.log10(M), np.log10(L)

# faixas de massa de Eker et al. (2018)
RANGES = [(0.179, 0.45), (0.45, 2.0), (2.0, 7.0), (7.0, 31.0)]
fits = []
for lo, hi in RANGES:
    m = (M >= lo) & (M <= hi)
    a, b = np.polyfit(x[m], y[m], 1)
    fits.append((lo, hi, a, b, m.sum()))
    print(f"  {lo:5.3f}-{hi:5.1f} Msun: alpha = {a:.2f}  (n={m.sum()})")

plt.rcParams.update({"font.family": "serif", "font.serif": ["DejaVu Serif"],
                     "mathtext.fontset": "cm"})
fig, ax = plt.subplots(figsize=(6.4, 5.0))

ax.set_xscale("log")
ax.set_yscale("log")
ax.grid(True, which="major", color=LINE, lw=0.6, zorder=0)
ax.grid(True, which="minor", color=LINE, lw=0.3, alpha=0.6, zorder=0)
ax.set_axisbelow(True)

ax.scatter(M, L, s=11, facecolor=BLUE, edgecolor="none", alpha=0.55,
           zorder=2, label=f"estrelas de sequência principal ($n={len(M)}$)")

# lei de potencia unica L ~ M^3.5, ancorada no Sol
mm = np.logspace(np.log10(0.15), np.log10(35), 200)
ax.plot(mm, mm**3.5, color=NAVY, lw=1.6, ls="--", zorder=3,
        label=r"$L\propto M^{3{,}5}$ (aproximação única)")

# ajuste por faixas
for i, (lo, hi, a, b, n) in enumerate(fits):
    seg = np.logspace(np.log10(lo), np.log10(hi), 60)
    ax.plot(seg, 10**b * seg**a, color=GOLD, lw=2.4, zorder=4,
            label="ajuste por faixa de massa" if i == 0 else None)
    xm = 0.62 if i == 1 else np.sqrt(lo * hi)
    ym = 10**b * xm**a
    lab = rf"$\alpha={a:.2f}$".replace(".", "{,}")
    dy = 12 if i == 1 else -17
    ax.annotate(lab, xy=(xm, ym),
                xytext=(-6 if i == 1 else 0, dy), textcoords="offset points",
                ha="right" if i == 1 else "center",
                fontsize=8.5, color=NAVY,
                bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none", alpha=0.85))

ax.scatter([1.0], [1.0], s=70, marker="o", facecolor=GOLD, edgecolor=NAVY, lw=1.0, zorder=6)
ax.annotate("Sol", xy=(1.0, 1.0), xytext=(11, -4), textcoords="offset points",
            fontsize=9, color=NAVY, ha="left")

ax.set_xlabel(r"massa  $M/M_\odot$", fontsize=10.5, color="#232323")
ax.set_ylabel(r"luminosidade  $L/L_\odot$", fontsize=10.5, color="#232323")
ax.set_xlim(0.13, 40)
ax.set_ylim(1.5e-3, 6e6)
from matplotlib.ticker import FixedLocator, FuncFormatter
ax.xaxis.set_major_locator(FixedLocator([0.2, 0.5, 1, 2, 5, 10, 20]))
ax.xaxis.set_minor_locator(FixedLocator([]))
ax.xaxis.set_major_formatter(FuncFormatter(
    lambda v, _: ("%g" % v).replace(".", ",")))
ax.tick_params(labelsize=9, colors=MUTED)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(MUTED)
    ax.spines[s].set_linewidth(0.8)

leg = ax.legend(loc="upper left", fontsize=8.5, frameon=True, framealpha=0.9,
                edgecolor=LINE, borderpad=0.6, handletextpad=0.6)
leg.get_frame().set_linewidth(0.6)
for t in leg.get_texts():
    t.set_color("#232323")

fig.tight_layout()
fig.savefig("relacao_massa_luminosidade.pdf")
fig.savefig("relacao_massa_luminosidade.png", dpi=200)
print("ok")
