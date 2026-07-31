"""Curvas de luz de transito reais, do Kepler (cadencia curta, 1 minuto).

HAT-P-7 b  (KIC 10666592, Q3): Jupiter quente em torno de uma estrela de 2 R_sol.
Kepler-10 b (KIC 11904151, Q3): planeta rochoso de 1,5 R_terra.

Cada evento e normalizado por uma reta ajustada aos pontos fora do transito na
propria janela, o que remove variabilidade estelar e, no caso do HAT-P-7, a
curva de fase do planeta. Depois os dados sao dobrados no periodo orbital.
Efemerides: NASA Exoplanet Archive (pscomppars).

Os arquivos FITS (cadencia curta, ~4 MB cada) nao acompanham este diretorio.
Para baixa-los:
  curl -O https://archive.stsci.edu/pub/kepler/lightcurves/0106/010666592/kplr010666592-2009259162342_slc.fits
  curl -O https://archive.stsci.edu/pub/kepler/lightcurves/0119/011904151/kplr011904151-2009291181958_slc.fits
Requer numpy, matplotlib e astropy.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from astropy.io import fits

NAVY, BLUE, GOLD, MUTED, LINE = "#14213D", "#2F6690", "#F2A541", "#667085", "#D8E2EC"
BKJD = 2454833.0

ALVOS = [
    dict(arq="kplr010666592-2009259162342_slc.fits", P=2.20474, T0=2454954.358572,
         nome="HAT-P-7 b", rror=0.075408, rade=16.926, srad=2.000,
         dur=0.16, jan=0.55, nbin=90, ylim=(0.9915, 1.0025), unidade="frac"),
    dict(arq="kplr011904151-2009291181958_slc.fits", P=0.8374907, T0=2455034.08687,
         nome="Kepler-10 b", rror=0.01268, rade=1.47, srad=1.065,
         dur=0.075, jan=0.20, nbin=55, ylim=(-330, 160), unidade="ppm"),
]


def curva_dobrada(alvo):
    d = fits.open(alvo["arq"])[1].data
    t, f, e = d["TIME"], d["PDCSAP_FLUX"], d["PDCSAP_FLUX_ERR"]
    ok = np.isfinite(t) & np.isfinite(f)
    t, f = t[ok], f[ok]
    P, t0 = alvo["P"], alvo["T0"] - BKJD
    n0, n1 = int(np.floor((t.min() - t0) / P)), int(np.ceil((t.max() - t0) / P))

    fase, flux = [], []
    for n in range(n0, n1 + 1):
        tc = t0 + n * P
        jan = np.abs(t - tc) < alvo["jan"]
        if jan.sum() < 100:
            continue
        tt, ff = t[jan] - tc, f[jan]
        fora = np.abs(tt) > alvo["dur"]
        if fora.sum() < 50 or (~fora).sum() < 20:
            continue
        base = np.polyval(np.polyfit(tt[fora], ff[fora], 1), tt)   # reta local
        fase.append(tt)
        flux.append(ff / base)
    return np.concatenate(fase), np.concatenate(flux)


plt.rcParams.update({"font.family": "serif", "font.serif": ["DejaVu Serif"],
                     "mathtext.fontset": "cm"})
fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.5))

for ax, alvo in zip(axes, ALVOS):
    fase, flux = curva_dobrada(alvo)
    h = fase * 24.0                                    # horas
    ppm = alvo["unidade"] == "ppm"
    y = (flux - 1.0) * 1e6 if ppm else flux

    # binagem
    lim = alvo["jan"] * 24
    bordas = np.linspace(-lim, lim, alvo["nbin"] + 1)
    idx = np.digitize(h, bordas) - 1
    xb = np.array([h[idx == i].mean() if (idx == i).sum() else np.nan
                   for i in range(alvo["nbin"])])
    yb = np.array([y[idx == i].mean() if (idx == i).sum() else np.nan
                   for i in range(alvo["nbin"])])
    nb = np.array([(idx == i).sum() for i in range(alvo["nbin"])])
    eb = np.array([y[idx == i].std() / max(np.sqrt(n), 1) if n else np.nan
                   for i, n in enumerate(nb)])

    ax.scatter(h, y, s=1.2, color=MUTED, alpha=0.18, lw=0, zorder=2,
               label="cadências individuais (1 min)")
    ax.errorbar(xb, yb, yerr=eb, fmt="o", ms=3.4, color=BLUE, ecolor=BLUE,
                elinewidth=0.8, capsize=0, zorder=4, label="média em intervalos")

    prof = alvo["rror"] ** 2
    ylin = -prof * 1e6 if ppm else 1 - prof
    ax.axhline(ylin, color=GOLD, lw=1.6, ls="--", zorder=5,
               label=r"$(R_p/R_\star)^2 = %.4f$" % prof if not ppm
               else r"$(R_p/R_\star)^2 = %.0f$ ppm" % (prof * 1e6))
    ax.axhline(0 if ppm else 1.0, color=LINE, lw=1.0, zorder=1)

    ax.set_xlim(-lim, lim)
    ax.set_ylim(*alvo["ylim"])
    ax.set_xlabel("tempo desde o meio do trânsito (h)", fontsize=9.5, color="#232323")
    ax.set_ylabel("variação de fluxo (ppm)" if ppm else "fluxo relativo",
                  fontsize=9.5, color="#232323")
    titulo = ("(a) %s: $R_p=%.1f\\,R_{\\rm Jup}$" % (alvo["nome"], alvo["rade"] / 11.209)
              if not ppm else
              "(b) %s: $R_p=%.2f\\,R_\\oplus$" % (alvo["nome"], alvo["rade"]))
    ax.set_title(titulo, fontsize=10, color=NAVY, pad=8)
    ax.grid(True, color=LINE, lw=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=8.5, colors=MUTED)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
        ax.spines[s].set_linewidth(0.8)
    leg = ax.legend(loc="lower center", fontsize=7.2, frameon=True, edgecolor=LINE,
                    framealpha=0.92, ncol=1)
    leg.get_frame().set_linewidth(0.6)
    for tx in leg.get_texts():
        tx.set_color("#232323")
    print(alvo["nome"], "pontos:", len(h), "| profundidade teorica ppm:", prof * 1e6)

fig.tight_layout(w_pad=2.0)
fig.savefig("transito.pdf")
fig.savefig("transito.png", dpi=190)
print("ok")
