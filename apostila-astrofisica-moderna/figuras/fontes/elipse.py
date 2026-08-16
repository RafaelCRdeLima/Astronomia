"""A geometria da elipse, antes da fisica.

Painel (a): a definicao focal. Para qualquer ponto P da curva, FP + F'P = 2a.
            Marca o semieixo maior a, o semieixo menor b e a distancia
            focal c = ae, e a relacao b^2 = a^2(1-e^2).
Painel (b): o Sol em um dos focos, o perielio e o afelio, e o par (r, theta)
            usado na deducao da equacao polar da orbita.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NAVY, BLUE, CYAN, GOLD, MUTED, LINE = "#14213D", "#2F6690", "#35A7B8", "#F2A541", "#667085", "#D8E2EC"
plt.rcParams.update({"font.family": "serif", "font.serif": ["DejaVu Serif"],
                     "mathtext.fontset": "cm"})

a, e = 1.0, 0.66
b = a * np.sqrt(1 - e**2)
c = a * e
t = np.linspace(0, 2*np.pi, 600)
X, Y = a*np.cos(t), b*np.sin(t)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.5),
                               gridspec_kw={"width_ratios": [1, 1]})

# ------------------------------------------------ (a) a definicao focal
ax1.plot(X, Y, color=NAVY, lw=1.6)
ax1.axhline(0, color=LINE, lw=0.8, zorder=0)
ax1.axvline(0, color=LINE, lw=0.8, zorder=0)
for xf, nome, dx in [(-c, "$F$", -0.07), (c, "$F'$", 0.07)]:
    ax1.plot([xf], [0], "o", ms=5.5, color=BLUE, zorder=4)
    ax1.text(xf + dx, -0.13, nome, fontsize=10, color=BLUE, ha="center", va="top")

thP = 1.15
Px, Py = a*np.cos(thP), b*np.sin(thP)
ax1.plot([Px], [Py], "o", ms=5, color=GOLD, zorder=5)
ax1.text(Px, Py + 0.07, "$P$", fontsize=10, color=GOLD, ha="center", va="bottom")
for xf in (-c, c):
    ax1.plot([xf, Px], [0, Py], color=GOLD, lw=1.3, zorder=3)

# semieixos
ax1.annotate("", xy=(a, -0.30), xytext=(0, -0.30),
             arrowprops=dict(arrowstyle="<->", color=MUTED, lw=0.9))
ax1.text(a/2, -0.36, "$a$", fontsize=10, color=MUTED, ha="center", va="top")
ax1.annotate("", xy=(0, b), xytext=(0, 0),
             arrowprops=dict(arrowstyle="<->", color=CYAN, lw=0.9))
ax1.text(0.045, b/2, "$b$", fontsize=10, color=CYAN, ha="left", va="center")
ax1.annotate("", xy=(c, 0.13), xytext=(0, 0.13),
             arrowprops=dict(arrowstyle="<->", color=BLUE, lw=0.9))
ax1.text(c/2, 0.17, "$c=ae$", fontsize=9, color=BLUE, ha="center", va="bottom")

ax1.text(0, 1.32, "(a) a definição focal", fontsize=10, color=NAVY, ha="center")
ax1.text(0, 1.10, r"$FP+F'P=2a$  para todo $P$", fontsize=9.5, color=NAVY, ha="center")
ax1.text(0, -0.80, r"$b^{2}=a^{2}(1-e^{2})$", fontsize=10.5, color=MUTED,
         ha="center", va="top")

# ------------------------------------------------ (b) o Sol, o perielio e (r, theta)
# o Sol esta no foco DIREITO (x=+c): logo o perielio e o extremo direito,
# a distancia a(1-e), e o afelio o esquerdo, a distancia a(1+e)
ax2.plot(X, Y, color=NAVY, lw=1.6)
ax2.axhline(0, color=LINE, lw=0.8, zorder=0)
ax2.plot([-c], [0], "o", ms=4, color=MUTED, zorder=4)
ax2.text(-c, -0.16, "foco vazio", fontsize=7.5, color=MUTED, ha="center", va="top")

ax2.plot([a], [0], "o", ms=5, color=BLUE, zorder=5)
ax2.plot([-a], [0], "o", ms=5, color=BLUE, zorder=5)
# rotulos fora da curva: em x = +/-a a elipse tem altura zero, entao o
# texto so nao a invade se comecar depois do vertice
ax2.text(a + 0.07, 0.20, "periélio", fontsize=9, color=BLUE, ha="left", va="bottom")
ax2.text(a + 0.07, 0.02, "$R_p=a(1-e)$", fontsize=8.5, color=BLUE, ha="left", va="bottom")
ax2.text(-a - 0.07, 0.20, "afélio", fontsize=9, color=BLUE, ha="right", va="bottom")
ax2.text(-a - 0.07, 0.02, "$R_a=a(1+e)$", fontsize=8.5, color=BLUE, ha="right", va="bottom")

thQ = 2.1
Qx, Qy = a*np.cos(thQ), b*np.sin(thQ)
ax2.plot([c, Qx], [0, Qy], color=GOLD, lw=1.4, zorder=3)
ax2.plot([Qx], [Qy], "o", ms=4.5, color=GOLD, zorder=5)
ax2.text((c+Qx)/2, (Qy)/2 + 0.09, "$r$", fontsize=11, color="#8a6a20", ha="center")
ang = np.linspace(0, np.arctan2(Qy, Qx - c), 60)
ax2.plot(c + 0.26*np.cos(ang), 0.26*np.sin(ang), color=MUTED, lw=1.0)
ax2.text(c + 0.06, 0.30, r"$\theta$", fontsize=11, color=MUTED)

ax2.plot([c], [0], "o", ms=20, color=GOLD, alpha=0.22, zorder=4)
ax2.plot([c], [0], "o", ms=11, color=GOLD, zorder=5)
ax2.text(c, -0.16, "Sol", fontsize=9, color="#8a6a20", ha="center", va="top")

ax2.text(0, 1.32, "(b) o Sol em um dos focos", fontsize=10, color=NAVY, ha="center")
ax2.text(0, -0.80, r"$r(\theta)=\dfrac{a(1-e^{2})}{1+e\cos\theta}$",
         fontsize=10.5, color=NAVY, ha="center", va="top")

for ax in (ax1, ax2):
    ax.set_aspect("equal")
    ax.set_xlim(-1.75, 1.75); ax.set_ylim(-1.15, 1.50)
    ax.axis("off")

fig.tight_layout(w_pad=0.6)
fig.savefig("../elipse.pdf")
fig.savefig("../elipse.png", dpi=190)
print("ok  b =", round(b,4), " c =", round(c,4), " b^2 =", round(b*b,4), " a^2(1-e^2) =", round(a*a*(1-e*e),4))
