"""Figura de corpo negro: lei de Planck (teoria) e espectro solar real (medido).

Painel (a): B_lambda(T) = 2hc^2/lambda^5 / (exp(hc/(lambda k T)) - 1), calculado
            diretamente da equacao, com o lugar geometrico dos picos (lei de Wien).
Painel (b): irradiancia solar espectral medida (Whole Heliosphere Interval reference
            spectrum, LASP/LISIRD; SORCE SIM + SOLSTICE + TIMED) comparada a um corpo
            negro de 5772 K escalado por (R_sol/1 UA)^2.
"""
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NAVY, BLUE, CYAN, GOLD, MUTED, LINE = "#14213D", "#2F6690", "#35A7B8", "#F2A541", "#667085", "#D8E2EC"

H, C, KB = 6.62607015e-34, 2.99792458e8, 1.380649e-23
R_SUN, AU = 6.957e8, 1.495978707e11
T_SUN = 5772.0


def planck_lambda(lam_m, T):
    """B_lambda em W m^-2 sr^-1 m^-1."""
    return (2 * H * C**2 / lam_m**5) / (np.expm1(H * C / (lam_m * KB * T)))


plt.rcParams.update({"font.family": "serif", "font.serif": ["DejaVu Serif"],
                     "mathtext.fontset": "cm"})
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.6, 7.4))

# ---------------------------------------------------------------- painel (a)
lam = np.logspace(np.log10(20e-9), np.log10(200e-6), 2000)
temps = [(30000, NAVY, "30 000 K"), (10000, BLUE, "10 000 K"),
         (5772, GOLD, "5772 K (Sol)"), (3000, "#C1666B", "3000 K")]

ax1.axvspan(380, 750, color=GOLD, alpha=0.13, lw=0, zorder=0)
ax1.text(530, 3e-2, "visível", ha="center", va="bottom", fontsize=8,
         color=MUTED, rotation=90)

for T, col, lab in temps:
    ax1.plot(lam * 1e9, planck_lambda(lam, T) * 1e-9, color=col, lw=2.0,
             label=lab, zorder=3)

# lugar geometrico dos picos: lei do deslocamento de Wien
Tw = np.logspace(np.log10(1500), np.log10(60000), 200)
lam_max = 2.897771955e-3 / Tw
ax1.plot(lam_max * 1e9, planck_lambda(lam_max, Tw) * 1e-9, color=MUTED, lw=1.4,
         ls="--", zorder=4, label=r"picos: $\lambda_{\max}T=2{,}90\times10^{-3}$ m$\,$K")

ax1.set_xscale("log")
ax1.set_yscale("log")
ax1.set_xlim(30, 3e4)
ax1.set_ylim(1e-2, 3e7)
ax1.set_xlabel(r"comprimento de onda  $\lambda$  (nm)", fontsize=10, color="#232323")
ax1.set_ylabel(r"$B_\lambda(T)$  (W m$^{-2}$ sr$^{-1}$ nm$^{-1}$)", fontsize=10, color="#232323")
ax1.set_title(r"(a) lei de Planck: $B_\lambda(T)=\dfrac{2hc^2/\lambda^5}"
              r"{e^{hc/\lambda k T}-1}$", fontsize=10.5, color=NAVY, pad=10)
ax1.grid(True, which="major", color=LINE, lw=0.6)
ax1.set_axisbelow(True)
leg1 = ax1.legend(loc="lower left", fontsize=8, frameon=True, edgecolor=LINE,
                  framealpha=0.92)
leg1.get_frame().set_linewidth(0.6)
for t in leg1.get_texts():
    t.set_color("#232323")
ax1.annotate("mais quente $\\Rightarrow$ pico\nmais azul e mais intenso",
             xy=(240, 2.0e6), xytext=(1500, 3e5), fontsize=8, color=MUTED,
             ha="left", va="center",
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9,
                             connectionstyle="arc3,rad=0.15"))

# ---------------------------------------------------------------- painel (b)
w, f = [], []
with open("whi_ref_spectra.csv") as fh:
    for row in csv.reader(fh):
        try:
            w.append(float(row[0]))
            f.append(float(row[3]))   # 10-16 abr 2008, Sol calmo
        except (ValueError, IndexError):
            continue
w, f = np.array(w), np.array(f)
m = (w >= 200) & (w <= 2400)
w, f = w[m], f[m]

# corpo negro de 5772 K visto da Terra: F = B * pi * (R_sol/1UA)^2
bb = planck_lambda(w * 1e-9, T_SUN) * np.pi * (R_SUN / AU) ** 2 * 1e-9

ax2.fill_between(w, 0, f, color=BLUE, alpha=0.13, lw=0, zorder=1)
ax2.plot(w, f, color=BLUE, lw=0.6, zorder=3, label="Sol (espectro medido, WHI 2008)")
ax2.plot(w, bb, color=GOLD, lw=2.0, zorder=4, label="corpo negro de 5772 K")

ax2.axvspan(380, 750, color=GOLD, alpha=0.10, lw=0, zorder=0)
ax2.set_xlim(200, 2400)
ax2.set_ylim(0, 2.35)
ax2.set_xlabel(r"comprimento de onda  $\lambda$  (nm)", fontsize=10, color="#232323")
ax2.set_ylabel(r"irradiância espectral (W m$^{-2}$ nm$^{-1}$)", fontsize=10, color="#232323")
ax2.set_title("(b) o Sol real comparado ao corpo negro ideal", fontsize=10.5,
              color=NAVY, pad=10)
ax2.grid(True, color=LINE, lw=0.6)
ax2.set_axisbelow(True)
leg2 = ax2.legend(loc="upper right", fontsize=8, frameon=True, edgecolor=LINE,
                  framealpha=0.92)
leg2.get_frame().set_linewidth(0.6)
for t in leg2.get_texts():
    t.set_color("#232323")

ax2.annotate("déficit no ultravioleta\n(opacidade da atmosfera solar)", xy=(315, 0.62),
             xytext=(208, 2.02), fontsize=8, color=MUTED, ha="left",
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
ax2.annotate("linhas de absorção\nde Fraunhofer", xy=(640, 1.52), xytext=(960, 1.45),
             fontsize=8, color=MUTED, ha="left",
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
ax2.annotate("no infravermelho o Sol real\nsupera o corpo negro ideal", xy=(1400, 0.31),
             xytext=(1330, 0.72), fontsize=8, color=MUTED, ha="left",
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))

for ax in (ax1, ax2):
    ax.tick_params(labelsize=9, colors=MUTED)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
        ax.spines[s].set_linewidth(0.8)

fig.tight_layout(h_pad=2.4)
fig.savefig("corpo_negro.pdf")
fig.savefig("corpo_negro.png", dpi=170)
print("ok")
