# -*- coding: utf-8 -*-
"""Figuras da Aula 6 (Capitulo 6 -- radiacao, corpo negro e espectros).

Mesma paleta e mesmo tratamento grafico das figuras da apostila; formato
largo, para projecao em 1280x720.
"""
import csv, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.special import wofz

NAVY, BLUE, CYAN, GOLD, MUTED, LINE, INK = ("#14213D", "#2F6690", "#35A7B8",
                                            "#F2A541", "#667085", "#D8E2EC", "#232323")
ROSA = "#C1666B"
H, C, KB, ME, EV = 6.62607015e-34, 2.99792458e8, 1.380649e-23, 9.1093837015e-31, 1.602176634e-19
R_SUN, AU, SIGMA = 6.957e8, 1.495978707e11, 5.670374419e-8
T_SUN = 5772.0

SAIDA = "/home/rafael/Codes/Astronomia/slides/assets/fig"
DADOS = "/home/rafael/Codes/Astronomia/apostila-astrofisica-moderna/dados/03_espectro_solar.csv"

plt.rcParams.update({"font.family": "serif", "font.serif": ["DejaVu Serif"],
                     "mathtext.fontset": "cm"})


def enfeita(ax):
    ax.tick_params(labelsize=10, colors=MUTED)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
        ax.spines[s].set_linewidth(0.8)
    ax.grid(True, color=LINE, lw=0.6)
    ax.set_axisbelow(True)


def salva(fig, nome, dpi=112):
    fig.savefig(os.path.join(SAIDA, nome + ".png"), dpi=dpi,
                facecolor="white", bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)
    print("  ->", nome + ".png")


def planck_l(lam_m, T):
    return (2 * H * C**2 / lam_m**5) / np.expm1(H * C / (lam_m * KB * T))


# ============================================================ 1. lei de Planck
def fig_planck():
    fig, ax = plt.subplots(figsize=(10.0, 5.0))
    lam = np.logspace(np.log10(20e-9), np.log10(200e-6), 2000)
    for T, col, rot in [(30000, NAVY, "30 000 K"), (10000, BLUE, "10 000 K"),
                        (5772, GOLD, "5772 K  (Sol)"), (3000, ROSA, "3000 K")]:
        ax.plot(lam * 1e9, planck_l(lam, T) * 1e-9, color=col, lw=2.2, label=rot, zorder=3)
    ax.axvspan(380, 750, color=GOLD, alpha=0.13, lw=0, zorder=0)
    ax.text(535, 4e-2, "visível", ha="center", va="bottom", fontsize=9, color=MUTED, rotation=90)
    Tw = np.logspace(np.log10(1500), np.log10(60000), 200)
    lm = 2.897771955e-3 / Tw
    ax.plot(lm * 1e9, planck_l(lm, Tw) * 1e-9, color=MUTED, lw=1.5, ls="--", zorder=4,
            label=r"picos: $\lambda_{\max}T=2{,}898\times10^{-3}$ m K")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(30, 3e4); ax.set_ylim(1e-2, 3e7)
    ax.set_xlabel(r"comprimento de onda  $\lambda$  (nm)", fontsize=12, color=INK)
    ax.set_ylabel(r"$B_\lambda(T)$   (W m$^{-2}$ sr$^{-1}$ nm$^{-1}$)", fontsize=12, color=INK)
    enfeita(ax)
    leg = ax.legend(loc="lower left", fontsize=10, frameon=True, edgecolor=LINE, facecolor="white")
    for t in leg.get_texts():
        t.set_color(INK)
    ax.annotate("nenhuma curva cruza outra:\na estrela mais quente emite mais\nem TODO comprimento de onda",
                xy=(3200, 1.1e2), xytext=(2600, 2.0e5), fontsize=10, color=INK, ha="left",
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0))
    salva(fig, "a6_planck")


# ====================================================== 2. Sol real x corpo negro
def fig_solar():
    lam, irr = [], []
    with open(DADOS) as f:
        r = csv.reader(f); next(r)
        for a, b in r:
            lam.append(float(a)); irr.append(float(b))
    lam = np.array(lam); irr = np.array(irr)
    bb = planck_l(lam * 1e-9, T_SUN) * np.pi * (R_SUN / AU) ** 2 * 1e-9

    fig, ax = plt.subplots(figsize=(10.0, 5.0))
    ax.fill_between(lam, 0, irr, color=GOLD, alpha=0.20, lw=0)
    ax.plot(lam, irr, color=GOLD, lw=0.8, zorder=3, label="Sol medido (acima da atmosfera)")
    ax.plot(lam, bb, color=NAVY, lw=2.0, zorder=4, label="corpo negro de 5772 K, mesmo $R_\\odot/d$")
    ax.set_xlim(200, 2400); ax.set_ylim(0, 2.4)
    ax.set_xlabel(r"comprimento de onda  $\lambda$  (nm)", fontsize=12, color=INK)
    ax.set_ylabel(r"irradiância espectral  (W m$^{-2}$ nm$^{-1}$)", fontsize=12, color=INK)
    enfeita(ax)
    leg = ax.legend(loc="upper right", fontsize=11, frameon=True, edgecolor=LINE, facecolor="white")
    for t in leg.get_texts():
        t.set_color(INK)
    ax.annotate("déficit no ultravioleta:\nsó 65% do previsto", xy=(330, 0.72), xytext=(233, 2.16),
                fontsize=10, color=INK, ha="left",
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0))
    ax.annotate("linhas de Fraunhofer", xy=(620, 1.92), xytext=(840, 1.66),
                fontsize=10, color=INK, ha="left",
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0))
    ax.annotate("no infravermelho o Sol real\nsupera o ideal em 19%", xy=(1500, 0.30),
                xytext=(1380, 0.95), fontsize=10, color=INK, ha="left",
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0))
    salva(fig, "a6_solar")


# ============================================== 3. atmosfera cinza + escurecimento
def fig_atmosfera():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.6, 4.5))

    tau = np.linspace(0, 4, 400)
    a1.plot(tau, (0.75 * (tau + 2.0 / 3.0)) ** 0.25, color=NAVY, lw=2.4, zorder=3)
    a1.axhline(1.0, color=MUTED, lw=1.0, ls=":", zorder=2)
    a1.axvline(2.0 / 3.0, color=GOLD, lw=1.6, ls="--", zorder=2)
    a1.plot([2.0 / 3.0], [1.0], "o", color=GOLD, ms=9, zorder=5)
    a1.text(1.15, 0.975, r"$\tau=2/3$:  $T=T_{ef}$", fontsize=11, color=INK, va="top")
    a1.plot([0], [0.5 ** 0.25], "o", color=ROSA, ms=8, zorder=5)
    a1.annotate(r"$T(0)=0{,}84\,T_{ef}$", xy=(0.05, 0.846), xytext=(0.92, 0.878),
                fontsize=11, color=ROSA, va="center",
                arrowprops=dict(arrowstyle="->", color=ROSA, lw=0.9))
    a1.set_xlim(0, 4); a1.set_ylim(0.75, 1.45)
    a1.set_xlabel(r"profundidade óptica  $\tau$", fontsize=12, color=INK)
    a1.set_ylabel(r"$T(\tau)\,/\,T_{ef}$", fontsize=12, color=INK)
    a1.set_title(r"(a) atmosfera cinza:  $T^4=\frac{3}{4}T_{ef}^4(\tau+\frac{2}{3})$",
                 fontsize=12, color=NAVY, pad=10)
    enfeita(a1)

    mu = np.linspace(0, 1, 300)
    a2.fill_between(mu, 1 - 0.6 * (1 - mu), 1 - 0.7 * (1 - mu), color=GOLD, alpha=0.30, lw=0,
                    label="Sol medido no visível  ($u=0{,}6$–$0{,}7$)")
    a2.plot(mu, (2 + 3 * mu) / 5, color=NAVY, lw=2.4, zorder=3,
            label=r"Eddington-Barbier:  $\frac{2+3\mu}{5}$")
    a2.set_xlim(0, 1); a2.set_ylim(0.3, 1.03)
    a2.set_xlabel(r"$\mu=\cos\theta$    (1 = centro do disco, 0 = borda)", fontsize=12, color=INK)
    a2.set_ylabel(r"$I(0,\mu)\,/\,I(0,1)$", fontsize=12, color=INK)
    a2.set_title("(b) escurecimento de bordo", fontsize=12, color=NAVY, pad=10)
    enfeita(a2)
    leg = a2.legend(loc="upper left", fontsize=10, frameon=True, edgecolor=LINE, facecolor="white")
    for t in leg.get_texts():
        t.set_color(INK)
    fig.tight_layout(w_pad=3.0)
    salva(fig, "a6_atmosfera")


# ==================================================== 4. perfis de linha
def fig_perfis():
    x = np.linspace(-6, 6, 1400)
    g = np.exp(-x**2 / 2) / np.sqrt(2 * np.pi)
    lo = (1 / np.pi) * 0.5 / (x**2 + 0.5**2)
    vo = np.real(wofz((x + 1j * 0.5) / np.sqrt(2))) / (np.sqrt(2 * np.pi))

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.6, 4.5))
    for ax, esc in ((a1, "linear"), (a2, "log")):
        ax.plot(x, g / g.max(), color=BLUE, lw=2.2, label="gaussiano — Doppler térmico")
        ax.plot(x, lo / lo.max(), color=ROSA, lw=2.2, label="lorentziano — colisões, natural")
        ax.plot(x, vo / vo.max(), color=NAVY, lw=2.6, ls="--", label="Voigt — a convolução dos dois")
        ax.set_xlim(-6, 6)
        ax.set_xlabel(r"$(\lambda-\lambda_0)$  em larguras Doppler", fontsize=12, color=INK)
        enfeita(ax)
        if esc == "log":
            ax.set_yscale("log"); ax.set_ylim(3e-5, 1.6)
            ax.set_title("(b) em escala log: as asas", fontsize=12, color=NAVY, pad=10)
            ax.annotate("as asas lorentzianas\nsobrevivem; a gaussiana\ndesaba",
                        xy=(5.0, 2.4e-2), xytext=(3.9, 8.0e-5), ha="right", fontsize=10, color=INK,
                        arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0))
        else:
            ax.set_ylim(0, 1.30)
            ax.set_ylabel("perfil normalizado", fontsize=12, color=INK)
            ax.set_title("(a) o núcleo da linha", fontsize=12, color=NAVY, pad=10)
            leg = ax.legend(loc="upper left", fontsize=9.5, frameon=True, edgecolor=LINE,
                            facecolor="white")
            for t in leg.get_texts():
                t.set_color(INK)
    fig.tight_layout(w_pad=3.0)
    salva(fig, "a6_perfis")


# ======================================= 5. Boltzmann x Saha: as linhas de Balmer
def fig_balmer():
    T = np.linspace(3000, 25000, 1200)
    Pe = 20.0                      # Pa, tipico de fotosfera
    ne = Pe / (KB * T)
    ZI, ZII = 2.0, 1.0
    chi, E2 = 13.6 * EV, 10.2 * EV
    saha = (2 * ZII / (ne * ZI)) * (2 * np.pi * ME * KB * T / H**2) ** 1.5 * np.exp(-chi / (KB * T))
    frac_neutro = 1.0 / (1.0 + saha)              # N_I / N_total
    boltz = (8.0 / ZI) * np.exp(-E2 / (KB * T))   # N_2 / N_I
    n2 = boltz * frac_neutro
    pico = T[np.argmax(n2)]

    fig, ax = plt.subplots(figsize=(10.0, 5.0))
    ax.plot(T, n2 / n2.max(), color=NAVY, lw=2.6, zorder=4, label=r"$N_2/N_{total}$  (força de Balmer)")
    ax.plot(T, frac_neutro, color=BLUE, lw=1.8, ls="--", zorder=3,
            label=r"Saha: fração ainda neutra")
    ax.plot(T, boltz / boltz.max(), color=ROSA, lw=1.8, ls=":", zorder=3,
            label=r"Boltzmann: fração excitada em $n=2$")
    ax.plot([pico, pico], [0, 1.02], color=GOLD, lw=1.6, ls="--", zorder=2)
    ax.text(pico, 1.055, "máximo em %.0f K" % (round(pico / 100.0) * 100),
            fontsize=11, color=INK, ha="center")
    for x, rot in [(3500, "M"), (4800, "K"), (5900, "G"), (7000, "F"), (9500, "A"),
                   (15000, "B"), (23000, "O")]:
        ax.text(x, 1.22, rot, ha="center", fontsize=12, color=MUTED, fontweight="bold")
    ax.set_xlim(3000, 25000); ax.set_ylim(0, 1.30)
    ax.set_xlabel("temperatura efetiva  (K)", fontsize=12, color=INK)
    ax.set_ylabel("fração relativa", fontsize=12, color=INK)
    enfeita(ax)
    leg = ax.legend(loc="upper right", bbox_to_anchor=(1.0, 0.94), fontsize=10.5,
                    frameon=True, edgecolor=LINE, facecolor="white")
    for t in leg.get_texts():
        t.set_color(INK)
    ax.annotate("frio demais:\nnada excitado", xy=(4200, 0.03), xytext=(4400, 0.30),
                fontsize=10, color=INK, arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0))
    ax.annotate("quente demais:\ntudo ionizado", xy=(14500, 0.05), xytext=(15200, 0.36),
                fontsize=10, color=INK, arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0))
    salva(fig, "a6_balmer")
    print("     pico de Balmer calculado: %.0f K" % pico)


# ============================================ 6. termico x nao termico
def fig_termico():
    """Como se distingue emissao termica de nao termica olhando so o espectro."""
    nu = np.logspace(8, 15.4, 900)
    T = 1e4
    bb = (2 * H * nu**3 / C**2) / np.expm1(H * nu / (KB * T))
    esc = bb.max()
    bb = bb / esc
    rj = (2 * nu**2 * KB * T / C**2) / esc          # Rayleigh-Jeans: diverge
    pl = (nu / 1e8) ** (-0.7)
    pl = pl / pl.max() * 0.9

    fig, ax = plt.subplots(figsize=(10.0, 5.0))
    ax.plot(nu, rj, color=MUTED, lw=1.6, ls="--", zorder=2,
            label=r"Rayleigh-Jeans:  $F_\nu\propto\nu^{2}$  (diverge)")
    ax.plot(nu, bb, color=GOLD, lw=2.8, zorder=4, label=r"térmico: corpo negro de $10^4$ K")
    ax.plot(nu, pl, color=CYAN, lw=2.8, zorder=3,
            label=r"não térmico: síncrotron,  $F_\nu\propto\nu^{-0{,}7}$")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(1e8, 2e15); ax.set_ylim(1e-8, 3e2)
    ax.set_xlabel(r"frequência  $\nu$  (Hz)", fontsize=12, color=INK)
    ax.set_ylabel(r"$F_\nu$  (normalizado)", fontsize=12, color=INK)
    enfeita(ax)
    leg = ax.legend(loc="lower left", fontsize=10.5, frameon=True, edgecolor=LINE, facecolor="white")
    for t in leg.get_texts():
        t.set_color(INK)
    for x, rot in [(4e8, "rádio"), (3e12, "infravermelho"), (5e14, "visível")]:
        ax.text(x, 1.1e2, rot, ha="center", fontsize=10.5, color=MUTED)
    ax.annotate("sobe como $\\nu^{2}$ e depois\ndespenca: há um pico,\ne o pico marca a temperatura",
                xy=(3.5e14, 0.55), xytext=(9e12, 1.5e-4), fontsize=10.5, color=INK, ha="left",
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0))
    ax.annotate("reta descendente em todo o intervalo:\nnenhuma temperatura produz isso",
                xy=(2e10, 1.2e-1), xytext=(3e9, 8e-4), fontsize=10.5, color=INK, ha="left",
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0))
    ax.annotate("a catástrofe do ultravioleta", xy=(1.2e14, 6e1), xytext=(2.0e9, 6e0),
                fontsize=10.5, color=INK, ha="left",
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0))
    salva(fig, "a6_termico")


if __name__ == "__main__":
    os.makedirs(SAIDA, exist_ok=True)
    for f in (fig_planck, fig_solar, fig_atmosfera, fig_perfis, fig_balmer, fig_termico):
        f()
    print("ok")
