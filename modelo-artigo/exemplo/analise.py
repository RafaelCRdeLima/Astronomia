"""Análise do Laboratório de dados 1 -- Sicrano da Silva, AST0001 2026/2."""
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({"font.family": "serif", "font.size": 9,
                     "mathtext.fontset": "cm", "axes.linewidth": 0.7})
CSV = "/home/rafael/Dropbox/UDESC/CCT/Graduação/Astronomia/dados/01_gaia_estrelas_25pc.csv"

linhas = list(csv.DictReader(open(CSV)))
def coluna(nome):
    return np.array([np.nan if x[nome].strip() == "" else float(x[nome]) for x in linhas])

p   = coluna("paralaxe_mas");      ep = coluna("erro_paralaxe_mas")
pmra= coluna("pmra_mas_ano");      pmdec = coluna("pmdec_mas_ano")
vr  = coluna("vel_radial_km_s");   G = coluna("G_mag");  BR = coluna("BP_RP")

# passos 1 e 2
d  = 1000.0 / p
MG = G - 5*np.log10(d) + 5
# passo 5
erel = ep / p
# passo 8
mu = np.hypot(pmra, pmdec) / 1000.0
vt = 4.74 * mu * d
tem_vr = ~np.isnan(vr)
v = np.full(len(d), np.nan)
v[tem_vr] = np.hypot(vt[tem_vr], vr[tem_vr])
# passo 4
anab = (MG > 10) & (BR < 1.5)

N, R = len(d), d.max()
V = 4/3*np.pi*R**3
n, sn = N/V, np.sqrt(N)/V

print("N=%d  R=%.3f pc  V=%.0f pc3" % (N, R, V))
print("n = %.4f +- %.4f pc^-3   (%.0f%% de 0,10)" % (n, sn, 100*n/0.10))
print("erro rel: <1%%: %d ; max %.2f%%" % ((erel < 0.01).sum(), 100*erel.max()))
print("anãs brancas: %d (%.1f +- %.1f %%)" % (anab.sum(), 100*anab.sum()/N,
                                              100*np.sqrt(anab.sum())/N))
print("sequência principal: %d" % (~anab).sum())
print("com vr: %d ; v>100: %d" % (tem_vr.sum(), np.nansum(v > 100)))
j = np.nanargmax(mu)        # maior movimento próprio = estrela de Barnard
jv = np.nanargmax(vt)
print("maior mu: %.3f''/ano  d=%.3f pc  vt=%.1f km/s" % (mu[j], d[j], vt[j]))
print("maior vt: %.1f km/s a d=%.2f pc" % (vt[jv], d[jv]))
print("G mais brilhante: %.2f" % G.min())
print("\nN(<d)/d^3:")
raios = np.array([6, 8, 10, 12, 14, 16, 18, R])
for rr in raios:
    print("  %5.2f  %4d  %.4f" % (rr, (d < rr).sum(), (d < rr).sum()/rr**3))
sus = np.where(tem_vr & (np.abs(vr) > 300) & (vt < 60))[0]
print("\nsuspeitas (|vr|>300 e vt<60):")
for k in sus:
    print("   vr=%7.1f  vt=%5.1f  M_G=%5.2f  BP-RP=%5.2f  anã branca? %s"
          % (vr[k], vt[k], MG[k], BR[k], bool(anab[k])))

# ------------------------------------------------------------ figura 1: HR
fig, ax = plt.subplots(figsize=(3.3, 3.1))
ax.scatter(BR[~anab], MG[~anab], s=2.5, c="#2F6690", alpha=0.45, lw=0,
           label="sequência principal (1884)")
ax.scatter(BR[anab], MG[anab], s=7, c="#C1666B", alpha=0.85, lw=0,
           label="anãs brancas (116)")
ax.axhline(10, color="0.6", lw=0.6, ls=":")
ax.axvline(1.5, color="0.6", lw=0.6, ls=":")
ax.invert_yaxis()
ax.set_xlabel(r"$G_{\rm BP}-G_{\rm RP}$")
ax.set_ylabel(r"$M_G$")
ax.legend(fontsize=7, frameon=False, loc="lower left")
ax.grid(alpha=0.25, lw=0.5)
fig.tight_layout(pad=0.3); fig.savefig("fig_hr.pdf"); plt.close(fig)

# --------------------------------------------------- figura 2: completeza
fig, ax = plt.subplots(figsize=(3.3, 2.7))
dd = np.linspace(4, R, 200)
cont = np.array([(d < x).sum() for x in dd])
ax.plot(dd, cont/dd**3, color="#2F6690", lw=1.6)
ax.axhline(0.31, color="#C1666B", lw=1.0, ls="--", label=r"$0{,}31$ (patamar)")
ax.axvline(8, color="0.6", lw=0.8, ls=":")
ax.text(8.3, 0.20, "8 pc", fontsize=7.5, color="0.35")
ax.set_xlabel(r"$d$ (pc)")
ax.set_ylabel(r"$N(<d)\,/\,d^{3}$   (pc$^{-3}$)")
ax.set_ylim(0.15, 0.55)
ax.legend(fontsize=7, frameon=False)
ax.grid(alpha=0.25, lw=0.5)
fig.tight_layout(pad=0.3); fig.savefig("fig_completeza.pdf"); plt.close(fig)

# ------------------------------------------------- figura 3 (larga): cinemática
fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 2.5))
a1.scatter(d, vt, s=2.5, c="#2F6690", alpha=0.4, lw=0)
a1.scatter(d[j], vt[j], s=26, c="#F2A541", edgecolor="k", lw=0.4, zorder=5)
a1.annotate("estrela de Barnard\n(maior $\\mu$)", (d[j], vt[j]), xytext=(3.4, 140),
            fontsize=7.5, arrowprops=dict(arrowstyle="->", lw=0.7))
a1.set_xlabel(r"$d$ (pc)"); a1.set_ylabel(r"$v_t$ (km s$^{-1}$)")
a1.set_ylim(0, 200); a1.grid(alpha=0.25, lw=0.5)
vv = v[tem_vr]
a2.hist(vv, bins=np.arange(0, 320, 10), color="#2F6690", alpha=0.8)
a2.axvline(100, color="#C1666B", lw=1.0, ls="--")
a2.text(104, 155, r"$v>100$ km s$^{-1}$: 97 estrelas", fontsize=7.2, color="#C1666B")
for k in sus:
    a2.annotate("", xy=(min(v[k], 315), 6), xytext=(min(v[k], 315), 45),
                arrowprops=dict(arrowstyle="->", color="#C1666B", lw=1.0))
a2.text(300, 60, "descartadas", fontsize=7.2, color="#C1666B", ha="right")
a2.set_xlabel(r"$v=\sqrt{v_r^2+v_t^2}$ (km s$^{-1}$)")
a2.set_ylabel("número de estrelas"); a2.grid(alpha=0.25, lw=0.5)
fig.tight_layout(pad=0.4); fig.savefig("fig_velocidades.pdf"); plt.close(fig)
print("\nfiguras: fig_hr.pdf, fig_completeza.pdf, fig_velocidades.pdf")
