"""O transito de Venus e a escala do Sistema Solar.

Dois observatorios separados por uma base b veem Venus projetado sobre
pontos diferentes do disco solar. Os raios se cruzam em Venus, de modo que
o observador do norte ve a corda mais ao sul e vice-versa. A separacao das
duas cordas, medida em angulo da Terra, vale k.b/a_T com k = a_V/(a_T-a_V).
Fora de escala: a figura exagera a base e os angulos.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

NAVY, BLUE, CYAN, GOLD, MUTED, LINE = "#14213D", "#2F6690", "#35A7B8", "#F2A541", "#667085", "#D8E2EC"
plt.rcParams.update({"font.family": "serif", "font.serif": ["DejaVu Serif"],
                     "mathtext.fontset": "cm"})

fig, ax = plt.subplots(figsize=(7.2, 3.4))
xT, xV, xS = 0.0, 3.6, 10.0          # posicoes horizontais (fora de escala)
bN, bS = 0.62, -0.62                 # os dois observatorios
Rsol, Rterra = 1.35, 0.42

# Sol
ax.add_patch(Circle((xS, 0), Rsol, facecolor="#FFE49A", edgecolor="#E0A93B", lw=1.2, zorder=1))
# Terra
ax.add_patch(Circle((xT, 0), Rterra, facecolor="#B9CBDD", edgecolor=BLUE, lw=1.2, zorder=3))
ax.plot([xT, xT], [-Rterra, Rterra], color=BLUE, lw=1.0, zorder=4)
for y, nome in [(bN, "N"), (bS, "S")]:
    ax.plot([xT], [y], "o", ms=5, color=NAVY, zorder=5)
    ax.text(xT - 0.30, y, nome, fontsize=10, color=NAVY, ha="right", va="center")
ax.annotate("", xy=(xT-0.62, bN), xytext=(xT-0.62, bS),
            arrowprops=dict(arrowstyle="<->", color=CYAN, lw=1.3))
ax.text(xT-0.78, 0, "$b$", fontsize=11, color=CYAN, ha="right", va="center")
ax.text(xT + 0.02, Rterra + 0.62, "Terra", fontsize=10, color=NAVY, ha="center")

# raios: de cada observatorio, passando por Venus, ate o Sol.
# eles se CRUZAM em Venus -- quem observa ao norte ve a corda ao sul
for y0, cor in [(bN, BLUE), (bS, "#B4623F")]:
    m = (0 - y0)/(xV - xT)
    yS = y0 + m*(xS - xT)
    ax.plot([xT, xS+0.2], [y0, y0 + m*(xS+0.2 - xT)], color=cor, lw=1.2, zorder=2)
    meia = np.sqrt(max(Rsol**2 - yS**2, 0.01))          # meia-corda real do disco
    ax.plot([xS - meia, xS + meia], [yS, yS], color=cor, lw=2.4, ls="--", zorder=4)

mN = (0-bN)/(xV-xT); ySN = bN + mN*(xS-xT)
mS = (0-bS)/(xV-xT); ySS = bS + mS*(xS-xT)
ax.text(xS + Rsol + 0.18, ySN, "trânsito visto de N", fontsize=8.5, color=BLUE, va="center")
ax.text(xS + Rsol + 0.18, ySS, "trânsito visto de S", fontsize=8.5, color="#B4623F", va="center")
ax.annotate("", xy=(xS - Rsol - 0.30, ySN), xytext=(xS - Rsol - 0.30, ySS),
            arrowprops=dict(arrowstyle="<->", color=NAVY, lw=1.2))
ax.text(xS - Rsol - 0.42, (ySN+ySS)/2, r"$\Delta$", fontsize=11, color=NAVY, ha="right", va="center")

# Venus
ax.add_patch(Circle((xV, 0), 0.17, facecolor=MUTED, edgecolor=NAVY, lw=1.0, zorder=5))
ax.text(xV, -0.52, "Vênus", fontsize=10, color=NAVY, ha="center")

# distancias
ax.annotate("", xy=(xV, -1.55), xytext=(xT, -1.55), arrowprops=dict(arrowstyle="<->", color=MUTED, lw=0.9))
ax.text((xT+xV)/2, -1.75, r"$a_\oplus-a_V\simeq0{,}277\,a_\oplus$", fontsize=9, color=MUTED, ha="center", va="top")
ax.annotate("", xy=(xS, -1.55), xytext=(xV, -1.55), arrowprops=dict(arrowstyle="<->", color=MUTED, lw=0.9))
ax.text((xV+xS)/2, -1.75, r"$a_V\simeq0{,}723\,a_\oplus$", fontsize=9, color=MUTED, ha="center", va="top")

ax.text(xS, Rsol + 0.26, "Sol", fontsize=10, color="#8a6a20", ha="center")
ax.text((xT+xS)/2, 2.02, "[fora de escala]", fontsize=8.5, color=MUTED, ha="center", style="italic")

ax.set_xlim(-1.8, 13.8); ax.set_ylim(-2.45, 2.35)
ax.set_aspect("equal"); ax.axis("off")
fig.tight_layout()
fig.savefig("../transito_venus.pdf")
fig.savefig("../transito_venus.png", dpi=190)
print("ok")
