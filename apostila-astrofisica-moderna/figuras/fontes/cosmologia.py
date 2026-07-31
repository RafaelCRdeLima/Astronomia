"""Historia da expansao: fator de escala em funcao do tempo cosmico.

Integra a equacao de Friedmann para o modelo LCDM plano,

    H(a) = H0 sqrt( Omega_r a^-4 + Omega_m a^-3 + Omega_L ),
    t(a) = int_0^a da' / (a' H(a')),

com parametros de Planck 2018: H0 = 67,4 km/s/Mpc, Omega_m = 0,315,
Omega_r = 9,14e-5 (fotons + neutrinos), Omega_L = 1 - Omega_m - Omega_r.

Nenhum evento marcado tem posicao escolhida a mao: cada um entra pelo seu
desvio para o vermelho e o tempo correspondente sai da integracao. A idade
do Universo tambem sai da conta, nao e imposta.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NAVY, BLUE, CYAN, GOLD, MUTED, LINE = "#14213D", "#2F6690", "#35A7B8", "#F2A541", "#667085", "#D8E2EC"

H0 = 67.4 * 1e3 / 3.0856775814913673e22      # s^-1
OM, ORAD = 0.315, 9.14e-5
OL = 1.0 - OM - ORAD
ANO = 3.15576e7


def E(a):
    return np.sqrt(ORAD * a**-4 + OM * a**-3 + OL)


# t(a) por integracao cumulativa em log a
loga = np.linspace(np.log(1e-12), np.log(3.0), 400000)
a = np.exp(loga)
integrando = 1.0 / (a * E(a)) / H0 * a          # da/(a H) = dloga /H
t = np.concatenate([[0.0], np.cumsum(np.diff(loga) * (integrando[1:] + integrando[:-1]) / 2)])
t_ano = t / ANO

t0 = np.interp(1.0, a, t_ano)
print("idade do Universo hoje: %.3f Gano" % (t0 / 1e9))
for z, nome in [(3400, "igualdade matéria-radiação"), (1100, "recombinação"),
                (20, "primeiras estrelas"), (6, "fim da reionização"),
                (2, "pico de formação estelar"), (0.63, "início da aceleração"),
                (0.0, "hoje")]:
    print("   z=%7.2f  ->  t = %11.4g anos   (%s)" % (z, np.interp(1 / (1 + z), a, t_ano), nome))

# (tempo em anos ou None, z ou None, rotulo do quadro)
EVENTOS = [
    (None, 1100, "recombinação: o Universo fica transparente\n"
                 r"$z=1100$, 366 mil anos"),
    (None, 20, "primeiras estrelas acendem\n" + r"$z\simeq20$, 180 milhões de anos"),
    (None, 2, "auge da formação estelar no Universo\n" + r"$z\simeq2$, 3,3 bilhões de anos"),
    (9.22e9, None, "formação do Sistema Solar\n9,2 bilhões de anos"),
    (None, 0.0, "hoje\n13,79 bilhões de anos"),
]

plt.rcParams.update({"font.family": "serif", "font.serif": ["DejaVu Serif"],
                     "mathtext.fontset": "cm"})
fig, ax = plt.subplots(figsize=(6.9, 4.6))

# eras dominadas por cada componente
a_eq_rm = ORAD / OM                                   # radiação = matéria
a_eq_ml = (OM / OL) ** (1 / 3)                        # matéria = energia escura
t_eq_rm = np.interp(a_eq_rm, a, t_ano)
t_eq_ml = np.interp(a_eq_ml, a, t_ano)
print("   igualdade rad-mat em t = %.4g anos (a=%.3g)" % (t_eq_rm, a_eq_rm))
print("   igualdade mat-Lambda em t = %.4g anos (a=%.3g)" % (t_eq_ml, a_eq_ml))

T_MIN, T_MAX = 3e-7, 6e10
for t1, t2, cor, rot in [(T_MIN, t_eq_rm, CYAN, "radiação"),
                         (t_eq_rm, t_eq_ml, BLUE, "matéria"),
                         (t_eq_ml, T_MAX, GOLD, "energia escura")]:
    ax.axvspan(t1, t2, color=cor, alpha=0.10, lw=0, zorder=0)
    ax.text(np.sqrt(max(t1, T_MIN) * min(t2, T_MAX)), 3.2, rot, fontsize=8.5,
            color=MUTED, ha="center", va="top", zorder=6)

m = (t_ano > T_MIN / 10) & (a < 2.5)
ax.plot(t_ano[m], a[m], color=NAVY, lw=2.0, zorder=4)

linhas = []
for i, (tev, z, texto) in enumerate(EVENTOS, start=1):
    if tev is None:
        aa = 1 / (1 + z)
        tt = np.interp(aa, a, t_ano)
    else:
        tt = tev
        aa = np.interp(tt, t_ano, a)
    ax.scatter([tt], [aa], s=52, facecolor=GOLD, edgecolor=NAVY, lw=1.0, zorder=7)
    dx, dy, hal = ((-9, -2, "right") if i == 4 else
                   (9, -2, "left") if i == 5 else (0, 9, "center"))
    ax.annotate(str(i), xy=(tt, aa), xytext=(dx, dy), textcoords="offset points",
                fontsize=8, color=NAVY, ha=hal,
                va="center" if i in (4, 5) else "bottom", zorder=8)
    linhas.append("%d.  %s" % (i, texto.replace("\n", "  ")))

ax.text(2.0e-6, 0.20, "\n".join(linhas), fontsize=8.0, color=NAVY, ha="left",
        va="top", linespacing=1.9, zorder=8)

# nucleossintese primordial: t ~ 3 min, fora do alcance de "a" util mas dentro do eixo
t_bbn = 3 * 60 / ANO
ax.axvline(t_bbn, color=MUTED, lw=0.9, ls=":", zorder=3)
ax.text(t_bbn * 1.6, 2.5e-10, "nucleossíntese primordial\n(3 minutos)", fontsize=8,
        color=MUTED, ha="left", va="bottom", zorder=8)

ax.axvline(t0, color=MUTED, lw=0.9, ls="--", zorder=3)
ax.text(t0 * 0.75, 2.5e-10, "idade do Universo que sai da integração:\n%.2f bilhões de anos" % (t0 / 1e9),
        fontsize=8, color=MUTED, ha="right", va="bottom", zorder=8)

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(T_MIN, T_MAX)
ax.set_ylim(1e-10, 4.5)
ax.set_xlabel("tempo desde o Big Bang (anos)", fontsize=10, color="#232323")
ax.set_ylabel(r"fator de escala  $a = 1/(1+z)$", fontsize=10, color="#232323")
ax.grid(True, which="major", color=LINE, lw=0.6)
ax.set_axisbelow(True)
ax.tick_params(labelsize=9, colors=MUTED)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(MUTED)
    ax.spines[s].set_linewidth(0.8)

fig.tight_layout()
fig.savefig("cosmologia.pdf")
fig.savefig("cosmologia.png", dpi=190)
print("ok")
