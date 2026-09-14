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


# ===================================================== 7-9. filtros fotometricos
#
# Curvas de transmissao aproximadas do sistema Johnson-Cousins: super-gaussianas
# de ordem 4 com o comprimento de onda efetivo e a largura a meia altura
# tabelados de cada banda. Sao representativas, nao os dados de um fabricante --
# as legendas das figuras dizem isso.
BANDAS = [("U", 365, 66, 0.60, "#8f5fd6"),
          ("B", 445, 94, 0.72, "#3d7dff"),
          ("V", 551, 88, 0.80, "#5fc25f"),
          ("R", 658, 138, 0.78, "#e4543f"),
          ("I", 806, 149, 0.55, "#8c2f2f")]


def transmissao(lam_nm, centro, fwhm, pico, ordem=4):
    w = fwhm / (2 * np.log(2) ** (1.0 / ordem))
    return pico * np.exp(-np.abs((lam_nm - centro) / w) ** ordem)


def fig_filtros_curvas():
    """Onde cada filtro deixa passar, com o espectro do Sol por tras."""
    lam = np.linspace(280, 1000, 2400)
    fig, ax = plt.subplots(figsize=(10.4, 4.8))

    sol = planck_l(lam * 1e-9, 5772.0)
    ax.fill_between(lam, 0, sol / sol.max() * 0.92, color=GOLD, alpha=0.13, lw=0, zorder=0)
    ax.plot(lam, sol / sol.max() * 0.92, color=GOLD, lw=1.3, zorder=1,
            label="espectro de uma estrela de 5772 K (escala arbitrária)")

    for nome, c, fw, pk, cor in BANDAS:
        t = transmissao(lam, c, fw, pk)
        ax.fill_between(lam, 0, t, color=cor, alpha=0.30, lw=0, zorder=2)
        ax.plot(lam, t, color=cor, lw=2.3, zorder=3)
        ax.text(c, pk + 0.035, nome, ha="center", fontsize=15, color=cor, fontweight="bold")
        ax.annotate("", xy=(c - fw / 2, pk * 0.5), xytext=(c + fw / 2, pk * 0.5),
                    arrowprops=dict(arrowstyle="<->", color=cor, lw=1.1, alpha=0.9))

    ax.set_xlim(280, 1000)
    ax.set_ylim(0, 1.0)
    ax.set_xlabel(r"comprimento de onda  $\lambda$  (nm)", fontsize=12, color=INK)
    ax.set_ylabel("transmissão do filtro", fontsize=12, color=INK)
    enfeita(ax)
    leg = ax.legend(loc="upper right", fontsize=10, frameon=True, edgecolor=LINE, facecolor="white")
    for t in leg.get_texts():
        t.set_color(INK)
    ax.text(551, 0.46, "largura a meia altura", ha="center", fontsize=9.5, color="#2f6b2f")
    salva(fig, "a6_filtros_curvas")


def fig_filtro_produto():
    """O diagrama: espectro vezes transmissao = o que o detector soma."""
    lam = np.linspace(300, 950, 1800)
    T = 5772.0
    F = planck_l(lam * 1e-9, T); F = F / F.max()
    S = transmissao(lam, 551, 88, 0.80)
    P = F * S

    fig, axs = plt.subplots(1, 3, figsize=(11.6, 3.5))
    for ax in axs:
        ax.set_xlim(300, 950); ax.set_xticks([400, 600, 800])
        enfeita(ax)
        ax.set_xlabel(r"$\lambda$ (nm)", fontsize=10.5, color=INK)

    axs[0].fill_between(lam, 0, F, color=GOLD, alpha=0.28, lw=0)
    axs[0].plot(lam, F, color=GOLD, lw=2.2)
    axs[0].set_ylim(0, 1.08); axs[0].set_ylabel("normalizado", fontsize=10.5, color=INK)
    axs[0].set_title(r"$F_\lambda$  — o espectro que chega", fontsize=11.5, color=NAVY, pad=9)

    axs[1].fill_between(lam, 0, S, color="#5fc25f", alpha=0.30, lw=0)
    axs[1].plot(lam, S, color="#5fc25f", lw=2.2)
    axs[1].set_ylim(0, 1.08)
    axs[1].set_title(r"$S_V(\lambda)$  — o filtro V", fontsize=11.5, color=NAVY, pad=9)

    axs[2].fill_between(lam, 0, P, color=CYAN, alpha=0.38, lw=0)
    axs[2].plot(lam, P, color=BLUE, lw=2.2)
    axs[2].set_ylim(0, 1.08)
    axs[2].set_title(r"$F_\lambda\,S_V(\lambda)$  — o que o detector soma",
                     fontsize=11.5, color=NAVY, pad=9)
    axs[2].text(625, 0.46, "esta área\né a contagem", fontsize=10.5, color=INK, ha="left")

    for x, s in ((0.347, "×"), (0.655, "=")):
        fig.text(x, 0.52, s, fontsize=26, color=MUTED, ha="center", va="center")
    fig.tight_layout(w_pad=4.2)
    salva(fig, "a6_filtro_produto")


def fig_filtros_duas_estrelas():
    """A mesma dupla de filtros em duas estrelas: de onde sai o indice de cor."""
    lam = np.linspace(300, 800, 2000)
    SB = transmissao(lam, 445, 94, 0.72)
    SV = transmissao(lam, 551, 88, 0.80)

    fig, axs = plt.subplots(1, 2, figsize=(10.6, 4.3))
    for ax, (T, rot, cor) in zip(axs, [(3000, "estrela fria, 3000 K", ROSA),
                                       (15000, "estrela quente, 15 000 K", BLUE)]):
        F = planck_l(lam * 1e-9, T); F = F / F.max()
        ax.plot(lam, F, color=cor, lw=2.4, zorder=4)
        ax.fill_between(lam, 0, F * SB / 0.72, color="#3d7dff", alpha=0.42, lw=0, zorder=2)
        ax.fill_between(lam, 0, F * SV / 0.80, color="#5fc25f", alpha=0.42, lw=0, zorder=3)
        fb = np.trapz(F * SB, lam) / np.trapz(SB, lam)
        fv = np.trapz(F * SV, lam) / np.trapz(SV, lam)
        bv = -2.5 * np.log10(fb / fv)
        ax.set_xlim(300, 800); ax.set_ylim(0, 1.12)
        ax.set_xlabel(r"$\lambda$ (nm)", fontsize=11.5, color=INK)
        ax.set_title(rot, fontsize=12, color=cor, pad=9)
        enfeita(ax)
        ax.text(445, 1.04, "B", ha="center", fontsize=14, color="#3d7dff", fontweight="bold")
        ax.text(551, 1.04, "V", ha="center", fontsize=14, color="#3d9c3d", fontweight="bold")
        ax.text(0.97, 0.52,
                "$F_B/F_V$ = %.2f\n$-2{,}5\\,\\log_{10}(F_B/F_V)$ = %+.2f" % (fb / fv, bv),
                transform=ax.transAxes, ha="right", fontsize=11.5, color=INK,
                bbox=dict(boxstyle="round,pad=0.45", fc="white", ec=LINE))
    axs[0].set_ylabel(r"$F_\lambda$, normalizado no máximo do painel", fontsize=10.5, color=INK)
    fig.tight_layout(w_pad=3.0)
    salva(fig, "a6_filtros_duas_estrelas")


# ==================================================== 10. as cores de cada atomo
#
# Linhas de emissao no visivel, com intensidades relativas aproximadas -- elas
# dependem das condicoes da descarga, e a legenda da figura diz isso. Os
# comprimentos de onda, esses, sao os tabelados.
LINHAS = [
 ("Hidrogênio", "H", [(656.28,100),(486.13,42),(434.05,18),(410.17,9),(397.01,5)]),
 ("Hélio", "He", [(388.86,14),(447.15,28),(471.31,9),(492.19,11),(501.57,38),
                  (587.56,100),(667.82,42),(706.52,22)]),
 ("Sódio", "Na", [(498.28,1),(568.26,2),(568.82,3),(588.99,100),(589.59,52),(615.42,2)]),
 ("Cálcio", "Ca", [(393.37,30),(396.85,22),(422.67,100),(445.48,22),(487.81,8),
                   (610.27,12),(612.22,15),(616.22,18),(643.91,10)]),
 ("Mercúrio", "Hg", [(404.66,42),(407.78,10),(435.83,88),(491.60,6),(546.07,100),
                     (576.96,50),(579.07,55)]),
 ("Neônio", "Ne", [(585.25,100),(588.19,40),(594.48,45),(597.55,30),(603.00,35),
                   (607.43,30),(609.62,35),(614.31,50),(616.36,30),(621.73,35),
                   (626.65,40),(630.48,35),(633.44,60),(638.30,70),(640.22,90),
                   (650.65,60),(653.29,40),(659.90,45),(667.83,30),(671.70,40),
                   (692.95,35),(703.24,40)]),
]


def rgb_visivel(l):
    """Comprimento de onda -> RGB aproximado, com a queda de resposta do olho
    nas pontas. Aproximacao de Bruton."""
    if l < 440:   r, g, b = -(l-440)/60.0, 0.0, 1.0
    elif l < 490: r, g, b = 0.0, (l-440)/50.0, 1.0
    elif l < 510: r, g, b = 0.0, 1.0, -(l-510)/20.0
    elif l < 580: r, g, b = (l-510)/70.0, 1.0, 0.0
    elif l < 645: r, g, b = 1.0, -(l-645)/65.0, 0.0
    else:         r, g, b = 1.0, 0.0, 0.0
    if l < 420:   f = 0.30 + 0.70*(l-380)/40.0
    elif l > 700: f = 0.30 + 0.70*(750-l)/50.0
    else:         f = 1.0
    f = max(0.0, min(1.0, f))
    return np.array([max(r,0)*f, max(g,0)*f, max(b,0)*f])


def fig_cores_atomos():
    L0, L1, NX = 380.0, 750.0, 1500
    lam = np.linspace(L0, L1, NX)
    sig = 0.75                                  # nm: largura de desenho da linha

    fig, axs = plt.subplots(len(LINHAS), 2, figsize=(10.8, 5.9),
                            gridspec_kw={"width_ratios": [13, 1.25], "hspace": 0.38,
                                         "wspace": 0.035})
    for i, (nome, simb, linhas) in enumerate(LINHAS):
        faixa = np.zeros((NX, 3))
        mistura = np.zeros(3)
        for lc, inten in linhas:
            perfil = np.exp(-0.5*((lam-lc)/sig)**2)
            cor = rgb_visivel(lc)
            faixa += inten*perfil[:, None]*cor[None, :]
            mistura += inten*cor
        if faixa.max() > 0:
            faixa = (faixa/faixa.max())**(1/1.5)   # gama, para as linhas fracas aparecerem
        img = np.clip(faixa, 0, 1)[None, :, :].repeat(2, axis=0)

        ax = axs[i, 0]
        ax.imshow(img, extent=[L0, L1, 0, 1], aspect="auto", interpolation="bilinear")
        ax.set_yticks([])
        ax.set_ylabel("%s\n%s" % (nome, simb), rotation=0, ha="right", va="center",
                      fontsize=11.5, color=INK, labelpad=14)
        for s in ax.spines.values():
            s.set_color("#9aa5b1"); s.set_linewidth(0.8)
        if i == len(LINHAS)-1:
            ax.set_xticks([400, 450, 500, 550, 600, 650, 700, 750])
            ax.tick_params(labelsize=10, colors=MUTED)
            ax.set_xlabel(r"comprimento de onda  $\lambda$  (nm)", fontsize=11.5, color=INK)
        else:
            ax.set_xticks([])

        sw = axs[i, 1]
        mistura = mistura/mistura.max() if mistura.max() > 0 else mistura
        sw.imshow(np.clip(mistura, 0, 1)[None, None, :].repeat(2, 0).repeat(2, 1),
                  aspect="auto", interpolation="nearest")
        sw.set_xticks([]); sw.set_yticks([])
        for s in sw.spines.values():
            s.set_color("#9aa5b1"); s.set_linewidth(0.8)

    axs[0, 1].set_title("cor que\no olho vê", fontsize=9.5, color=MUTED, pad=7)
    fig.text(0.5, 0.005, "intensidades relativas aproximadas; os comprimentos de onda são os tabelados",
             ha="center", fontsize=9, color=MUTED)
    axs[0, 0].set_title("as linhas de emissão, nos comprimentos de onda tabelados",
                        fontsize=11.5, color=NAVY, pad=8)
    salva(fig, "a6_cores_atomos")


# ============================================ 11. emissao e absorcao (Kirchhoff)
#
# Linhas fortes do espectro solar, com a letra de Fraunhofer e a profundidade
# aproximada (fracao do continuo que some no nucleo da linha).
FRAUNHOFER = [
 (393.37, 0.95, "K",  "Ca II"),
 (396.85, 0.92, "H",  "Ca II"),
 (410.17, 0.50, "h",  "Hδ"),
 (422.67, 0.40, "g",  "Ca I"),
 (434.05, 0.58, "G'", "Hγ"),
 (438.35, 0.48, "d",  "Fe I"),
 (486.13, 0.62, "F",  "Hβ"),
 (516.73, 0.58, "b",  "Mg I"),
 (517.27, 0.55, "",   "Mg I"),
 (518.36, 0.52, "",   "Mg I"),
 (527.04, 0.48, "E",  "Fe I"),
 (588.99, 0.85, "D",  "Na I"),
 (589.59, 0.80, "",   "Na I"),
 (656.28, 0.68, "C",  "Hα"),
 (686.72, 0.38, "B",  "O₂"),
]


def fig_emissao_absorcao():
    """As tres situacoes de Kirchhoff, com as MESMAS linhas nas tres."""
    L0, L1, NX = 380.0, 750.0, 1600
    lam = np.linspace(L0, L1, NX)
    sig = 0.85
    base = np.array([rgb_visivel(l) for l in lam])

    cont = planck_l(lam * 1e-9, 5772.0)
    cont = (cont / cont.max()) ** 0.45                 # gama, para as pontas não sumirem

    perfis = np.zeros(NX)
    for lc, prof, _, _ in FRAUNHOFER:
        perfis = np.maximum(perfis, prof * np.exp(-0.5 * ((lam - lc) / sig) ** 2))
    emiss = np.zeros(NX)
    for lc, prof, _, _ in FRAUNHOFER:
        emiss += prof * np.exp(-0.5 * ((lam - lc) / sig) ** 2)
    emiss = (emiss / emiss.max()) ** 0.55

    faixas = [("fonte contínua\ncorpo denso e quente", base * cont[:, None]),
              ("emissão\ngás fino e quente, visto de lado", base * emiss[:, None]),
              ("absorção\no mesmo contínuo, visto através do gás",
               base * (cont * (1 - perfis))[:, None])]

    fig = plt.figure(figsize=(11.8, 5.2))
    gs = fig.add_gridspec(4, 1, height_ratios=[1.85, 1, 1, 1], hspace=0.44,
                          left=0.24, right=0.985, top=0.985, bottom=0.20)

    # ---------------------------------------------------- o desenho da situação
    ax = fig.add_subplot(gs[0]); ax.set_axis_off()
    ax.set_xlim(0, 10); ax.set_ylim(-1.15, 3.1)
    g = plt.Circle((1.35, 1.35), 0.62, color="#FFD873", zorder=3)
    ax.add_patch(plt.Circle((1.35, 1.35), 0.95, color="#FFD873", alpha=0.22, zorder=2))
    ax.add_patch(g)
    ax.text(1.35, 0.25, "corpo denso\ne quente", ha="center", fontsize=10, color=INK)
    nuvem = plt.matplotlib.patches.Ellipse((4.6, 1.35), 2.5, 1.7, color=CYAN, alpha=0.22, zorder=2)
    ax.add_patch(nuvem)
    ax.add_patch(plt.matplotlib.patches.Ellipse((4.6, 1.35), 2.5, 1.7, fill=False,
                 edgecolor=CYAN, lw=1.4, ls="--", zorder=3))
    ax.text(4.6, 0.25, "gás fino e mais frio", ha="center", fontsize=10, color=INK)
    ax.annotate("", xy=(8.6, 1.35), xytext=(2.1, 1.35),
                arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=2.6))
    ax.text(8.75, 1.35, "vê\nabsorção", ha="left", va="center", fontsize=11, color=INK)
    ax.annotate("", xy=(6.2, 2.85), xytext=(4.9, 1.9),
                arrowprops=dict(arrowstyle="-|>", color=CYAN, lw=2.2))
    ax.text(6.35, 2.85, "vê emissão", ha="left", va="center", fontsize=11, color=INK)
    ax.text(0.9, 2.62, "o gás reemite em todas as direções",
            ha="left", fontsize=9.5, color=MUTED, style="italic")

    # ---------------------------------------------------------- as três faixas
    eixos = []
    for i, (rot, img) in enumerate(faixas):
        a = fig.add_subplot(gs[i + 1]); eixos.append(a)
        a.imshow(np.clip(img, 0, 1)[None, :, :].repeat(2, axis=0),
                 extent=[L0, L1, 0, 1], aspect="auto", interpolation="bilinear")
        a.set_yticks([])
        a.set_ylabel(rot, rotation=0, ha="right", va="center", fontsize=10, color=INK, labelpad=12)
        for s in a.spines.values():
            s.set_color("#9aa5b1"); s.set_linewidth(0.8)
        if i == 0:
            a.set_xticks([400, 450, 500, 550, 600, 650, 700, 750])
            a.xaxis.set_ticks_position("top"); a.xaxis.set_label_position("top")
            a.tick_params(labelsize=10, colors=MUTED)
            a.set_xlabel(r"comprimento de onda  $\lambda$  (nm)", fontsize=11.5,
                         color=INK, labelpad=8)
        else:
            a.set_xticks([])

    # as letras de Fraunhofer, acima da faixa de absorção e escalonadas quando vizinhas
    ant, alto = -99.0, False
    for lc, _, letra, _ in FRAUNHOFER:
        if not letra:
            continue
        alto = (lc - ant) < 14.0 and not alto
        ant = lc
        eixos[2].annotate(letra, xy=(lc, 0.0), xytext=(lc, -0.90 if alto else -0.40),
                          ha="center", va="top", fontsize=10, color=INK,
                          annotation_clip=False,
                          arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7,
                                          shrinkA=1, shrinkB=0))
    fig.text(0.5, 0.008, "letras de Fraunhofer; profundidades aproximadas, comprimentos de onda tabelados",
             ha="center", fontsize=9, color=MUTED)
    salva(fig, "a6_emissao_absorcao")


# ================================================ 12. um espectro deslocado
def fig_doppler_espectro():
    """Em cima, o deslocamento visivel de uma galaxia; embaixo, o caso estelar,
    que e o exemplo do slide anterior: Halfa a -105 km/s."""
    L0, L1, NX = 370.0, 760.0, 1700
    lam = np.linspace(L0, L1, NX)
    sig = 0.9
    base = np.array([rgb_visivel(l) for l in lam])
    cont = planck_l(lam * 1e-9, 5772.0)
    cont = (cont / cont.max()) ** 0.45
    Z = 0.045                                  # ~13 500 km/s, um aglomerado proximo

    def faixa(z):
        perfis = np.zeros(NX)
        for lc, prof, _, _ in FRAUNHOFER:
            perfis = np.maximum(perfis, prof*np.exp(-0.5*((lam - lc*(1+z))/sig)**2))
        return base * (cont*(1 - perfis))[:, None]

    fig = plt.figure(figsize=(11.8, 5.35))
    gs = fig.add_gridspec(5, 1, height_ratios=[1, 1, 1, 0.66, 1.95], hspace=0.40,
                          left=0.135, right=0.985, top=0.925, bottom=0.085)

    casos = [(-Z, "aproximando", "para o azul", BLUE),
             (0.0, "em repouso", "o laboratório", MUTED),
             (+Z, "afastando", "para o vermelho", ROSA)]
    eixos = []
    for i, (z, rot, sub, cor) in enumerate(casos):
        a = fig.add_subplot(gs[i]); eixos.append(a)
        a.imshow(np.clip(faixa(z), 0, 1)[None, :, :].repeat(2, axis=0),
                 extent=[L0, L1, 0, 1], aspect="auto", interpolation="bilinear")
        a.set_yticks([]); a.set_xticks([])
        a.set_ylabel("%s\n%s" % (rot, sub), rotation=0, ha="right", va="center",
                     fontsize=10.5, color=cor, labelpad=12)
        for s in a.spines.values():
            s.set_color("#9aa5b1"); s.set_linewidth(0.8)
        if i == 0:
            a.set_xticks([400, 450, 500, 550, 600, 650, 700, 750])
            a.xaxis.set_ticks_position("top"); a.xaxis.set_label_position("top")
            a.tick_params(labelsize=10, colors=MUTED)
            a.set_xlabel(r"comprimento de onda  $\lambda$  (nm)", fontsize=11.5,
                         color=INK, labelpad=7)

    # o caminho de duas linhas atraves das tres faixas
    marcas = ((393.37, "#7b5cff", "Ca II K"), (656.28, "#f24b4b", r"H$\alpha$"))
    for lc, cor, nome in marcas:
        pts = [(lc*(1+z), eixos[i]) for i, (z, _, _, _) in enumerate(casos)]
        for (x0, a0), (x1, a1) in zip(pts[:-1], pts[1:]):
            fig.add_artist(plt.matplotlib.patches.ConnectionPatch(
                xyA=(x0, 0), coordsA=a0.transData, xyB=(x1, 1), coordsB=a1.transData,
                color=cor, lw=1.4, ls=(0, (4, 3)), alpha=0.95))

    # faixa propria para os rotulos, alinhada ao mesmo eixo de lambda
    rt = fig.add_subplot(gs[3]); rt.set_axis_off()
    rt.set_xlim(L0, L1); rt.set_ylim(0, 1)
    for lc, cor, nome in marcas:
        rt.text(lc*(1+Z), 1.02, nome, ha="center", va="top", fontsize=10.5, color=cor)
    rt.text((L0+L1)/2, 0.30,
            "as duas andam juntas: $\\Delta\\lambda/\\lambda$ é o mesmo nas duas, "
            "$\\Delta\\lambda$ não é",
            ha="center", va="center", fontsize=10.5, color=INK)

    # ------------------------------------- o caso estelar, com o numero do slide
    az = fig.add_subplot(gs[4])
    lz = np.linspace(654.2, 658.4, 1400)
    l_rep, l_obs = 656.28, 656.05
    perfil = lambda c: 1 - 0.70*np.exp(-0.5*((lz - c)/0.25)**2)
    az.plot(lz, perfil(l_rep), color=MUTED, lw=2.0, ls="--", label="repouso, 656,28 nm")
    az.plot(lz, perfil(l_obs), color=BLUE, lw=2.6, label="observado, 656,05 nm")
    az.set_xlim(654.2, 658.4); az.set_ylim(0.18, 1.14)
    az.set_xlabel(r"comprimento de onda  $\lambda$  (nm)", fontsize=11.5, color=INK)
    az.set_ylabel("fluxo\nnormalizado", fontsize=10.5, color=INK)
    enfeita(az)
    az.annotate("", xy=(l_obs, 0.245), xytext=(l_rep, 0.245),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.4))
    az.text(l_obs - 0.12, 0.245, r"$\Delta\lambda = 0{,}23$ nm",
            ha="right", va="center", fontsize=10.5, color=INK)
    az.text(654.35, 0.50, r"$v_r = c\,\Delta\lambda/\lambda_0 = -105$ km/s",
            ha="left", fontsize=12, color=BLUE)
    az.set_title("o caso estelar: a mesma H$\\alpha$, a 105 km/s", fontsize=11.5,
                 color=NAVY, pad=7)
    leg = az.legend(loc="lower right", fontsize=10, frameon=True, edgecolor=LINE,
                    facecolor="white")
    for t in leg.get_texts():
        t.set_color(INK)
    salva(fig, "a6_doppler_espectro")


# ================================ 13. as duas leis classicas contra a de Planck
def fig_wien_rj_planck():
    """Cada lei classica acerta uma metade do espectro. Precisa de dois paineis:
    no linear a catastrofe se ve, mas a convergencia de Rayleigh-Jeans so aparece
    no log, muito alem de 2,5 um."""
    T = 5772.0
    def curvas(lam):
        lm = lam * 1e-9
        p = (2 * H * C**2 / lm**5) / np.expm1(H * C / (lm * KB * T))
        w = (2 * H * C**2 / lm**5) * np.exp(-H * C / (lm * KB * T))
        r = 2 * C * KB * T / lm**4
        return p, w, r

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.4, 4.7))

    # ---------------------------------------- (a) linear: a catastrofe
    lam = np.linspace(40, 2500, 2400)
    p, w, r = curvas(lam)
    esc = p.max()
    a1.plot(lam, r/esc, color=ROSA, lw=2.6, label="Rayleigh-Jeans (1900)")
    a1.plot(lam, w/esc, color=BLUE, lw=2.2, ls="--", label="Wien (1896)")
    a1.plot(lam, p/esc, color=GOLD, lw=3.0, label="Planck (1900), e o medido")
    a1.axvspan(380, 750, color=GOLD, alpha=0.10, lw=0, zorder=0)
    a1.set_xlim(0, 2500); a1.set_ylim(0, 1.5)
    a1.set_xlabel(r"$\lambda$ (nm)", fontsize=11.5, color=INK)
    a1.set_ylabel(r"$B_\lambda$, em unidades do pico de Planck", fontsize=11, color=INK)
    a1.set_title("(a) a catástrofe, em escala linear", fontsize=12, color=NAVY, pad=9)
    enfeita(a1)
    leg = a1.legend(loc="upper right", fontsize=9.5, frameon=True, edgecolor=LINE,
                    facecolor="white")
    for t in leg.get_texts():
        t.set_color(INK)
    a1.annotate("continua subindo sem limite:\nem 200 nm, 20 000× o medido",
                xy=(1010, 1.47), xytext=(70, 1.41), fontsize=9.5, color=ROSA, va="top",
                arrowprops=dict(arrowstyle="->", color=ROSA, lw=1.2))

    # ---------------------------------------- (b) log-log: as duas metades
    lam = np.logspace(np.log10(80), np.log10(2e5), 2000)
    p, w, r = curvas(lam)
    esc = p.max()
    a2.plot(lam, r/esc, color=ROSA, lw=2.4, label="Rayleigh-Jeans")
    a2.plot(lam, w/esc, color=BLUE, lw=2.0, ls="--", label="Wien")
    a2.plot(lam, p/esc, color=GOLD, lw=2.8, label="Planck")
    a2.set_xscale("log"); a2.set_yscale("log")
    a2.set_xlim(80, 2e5); a2.set_ylim(1e-9, 1e4)
    a2.set_xticks([1e2, 1e3, 1e4, 1e5])
    a2.set_xticklabels(["100 nm", "1 µm", "10 µm", "100 µm"])
    a2.set_xlabel(r"$\lambda$", fontsize=11.5, color=INK)
    a2.set_title("(b) as duas metades, em log-log", fontsize=12, color=NAVY, pad=9)
    enfeita(a2)
    a2.annotate("Wien acerta aqui\ne despenca depois", xy=(160, 4e-3), xytext=(95, 8e-7),
                fontsize=10, color=BLUE,
                arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.1))
    a2.annotate("Rayleigh-Jeans só encosta\nem Planck além de ~13 µm",
                xy=(4e4, 2.5e-5), xytext=(2.2e2, 1.1e-8), fontsize=10, color=ROSA,
                arrowprops=dict(arrowstyle="->", color=ROSA, lw=1.1))
    fig.tight_layout(w_pad=2.6)
    salva(fig, "a6_wien_rj_planck")


if __name__ == "__main__":
    os.makedirs(SAIDA, exist_ok=True)
    for f in (fig_planck, fig_solar, fig_atmosfera, fig_perfis, fig_balmer, fig_termico,
              fig_filtros_curvas, fig_filtro_produto, fig_filtros_duas_estrelas,
              fig_cores_atomos, fig_emissao_absorcao, fig_doppler_espectro,
              fig_wien_rj_planck):
        f()
    print("ok")
