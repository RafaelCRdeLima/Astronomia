# -*- coding: utf-8 -*-
"""Equacoes da Aula 6 em SVG, no mesmo padrao das aulas 1-5:
mathtext 'cm', 34 pt, cor #f4f4f1, fundo transparente, bbox tight."""
import os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({"mathtext.fontset": "cm"})
SAIDA = "/home/rafael/Codes/Astronomia/slides/assets/eq"
COR, TAM, PAD = "#f4f4f1", 34, 0.1

EQ = {
# ---------------------------------------------------------- travessia 1
"a6_foton":      r"$E=h\nu=\frac{hc}{\lambda}$",
"a6_wien":       r"$\lambda_{\mathrm{max}}\,T\simeq 2{,}898\times10^{-3}\ \mathrm{m\,K}$",
"a6_wien_nm":    r"$T\simeq\frac{2{,}898\times10^{6}}{\lambda_{\mathrm{max}}\,(\mathrm{nm})}\ \mathrm{K}$",
"a6_wien_ex":    r"$\lambda_{\mathrm{max}}=520\,\mathrm{nm}\ \Longrightarrow\ T\simeq 5570\,\mathrm{K}$",
"a6_wien_ex2":   r"$\lambda_{\mathrm{max}}=610\,\mathrm{nm}\ \Longrightarrow\ T\simeq 4750\,\mathrm{K}$",
"a6_planck_l":   r"$B_\lambda(T)=\frac{2hc^{2}}{\lambda^{5}}\,\frac{1}{e^{hc/\lambda kT}-1}$",
"a6_sb":         r"$F=\sigma T^{4}$",
"a6_fbol":       r"$f_{\mathrm{bol}}=\sigma T^{4}\left(\frac{R}{d}\right)^{2}$",
"a6_contagens":  r"$C_{\mathrm{bruto}}(\lambda)=t\,R_{\mathrm{inst}}(\lambda)\,F_\lambda(\lambda)+D(\lambda)+N(\lambda)$",
"a6_reducao":    r"$F_\lambda(\lambda)\ \propto\ \frac{C_{\mathrm{bruto}}(\lambda)-D(\lambda)}{t\,R_{\mathrm{inst}}(\lambda)}$",
"a6_filtro":     r"$F_X=\frac{\int F_\lambda(\lambda)\,S_X(\lambda)\,d\lambda}{\int S_X(\lambda)\,d\lambda}$",
"a6_bv":         r"$B-V\simeq-2{,}5\,\log_{10}\!\left(\frac{F_B}{F_V}\right)$",
"a6_bv_ex":      r"$B-V=-2{,}5\log_{10}(0{,}70)\simeq 0{,}39$",
"a6_ebv":        r"$E(B-V)=(B-V)_{\mathrm{obs}}-(B-V)_{\mathrm{intr}}\,,\qquad R_V=\frac{A_V}{E(B-V)}\simeq 3{,}1$",
"a6_doppler":    r"$\frac{\Delta\lambda}{\lambda_{0}}\simeq\frac{v_r}{c}$",
"a6_vr_ex":      r"$v_r\simeq 299792\,\frac{-0{,}23}{656{,}28}\simeq-105\ \mathrm{km\,s^{-1}}$",
"a6_fint":       r"$f_{\mathrm{faixa}}\simeq\sum_i F_{\lambda,i}\,\Delta\lambda_i$",
"a6_abertura":   r"$C_{\mathrm{estrela}}=C_{\mathrm{ap}}-\frac{A_{\mathrm{ap}}}{A_{\mathrm{fundo}}}\,C_{\mathrm{fundo}}$",
"a6_abert_ex":   r"$C_{\mathrm{estrela}}=18500-\frac{1}{4}(4200)=17450$",
# ---------------------------------------------------------- travessia 2
"a6_int":        r"$dE=I_\nu\cos\theta\,dA\,d\Omega\,d\nu\,dt$",
"a6_fnu":        r"$F_\nu=\int I_\nu\cos\theta\,d\Omega$",
"a6_unu":        r"$u_\nu=\frac{1}{c}\int I_\nu\,d\Omega\,,\qquad P_\nu=\frac{1}{c}\int I_\nu\cos^{2}\theta\,d\Omega$",
"a6_pu3":        r"$u=\frac{4\pi}{c}I\,,\qquad P=\frac{1}{3}u$",
"a6_transp":     r"$\frac{dI_\nu}{ds}=-\kappa_\nu\rho\,I_\nu+j_\nu$",
"a6_tau_s":      r"$d\tau_\nu=\kappa_\nu\rho\,ds\,,\qquad S_\nu=\frac{j_\nu}{\kappa_\nu\rho}$",
"a6_transp_tau": r"$\frac{dI_\nu}{d\tau_\nu}=-I_\nu+S_\nu$",
"a6_solform":    r"$I_\nu(\tau_\nu)=I_\nu(0)\,e^{-\tau_\nu}+\int_0^{\tau_\nu}\!S_\nu(t)\,e^{-(\tau_\nu-t)}dt$",
"a6_fino":       r"$\tau_\nu\ll1:\quad I_\nu\simeq I_\nu(0)+\tau_\nu S_\nu$",
"a6_espesso":    r"$\tau_\nu\gg1:\quad I_\nu\to S_\nu=B_\nu(T)$",
"a6_modos":      r"$N(k)=2\cdot\frac{1}{8}\cdot\frac{4}{3}\pi\left(\frac{kL}{\pi}\right)^{3}=\frac{k^{3}L^{3}}{3\pi^{2}}$",
"a6_gnu":        r"$g(\nu)=\frac{1}{L^{3}}\frac{dN}{d\nu}=\frac{8\pi\nu^{2}}{c^{3}}$",
"a6_rjclass":    r"$\langle E\rangle=kT\ \Longrightarrow\ u_\nu=\frac{8\pi\nu^{2}kT}{c^{3}}$",
"a6_emedia":     r"$\langle E\rangle=\frac{\sum_{n}nh\nu\,e^{-nh\nu/kT}}{\sum_{n}e^{-nh\nu/kT}}=\frac{h\nu}{e^{h\nu/kT}-1}$",
"a6_planck_nu":  r"$B_\nu(T)=\frac{2h\nu^{3}}{c^{2}}\,\frac{1}{e^{h\nu/kT}-1}$",
"a6_rj":         r"$h\nu\ll kT:\quad B_\nu\to\frac{2\nu^{2}kT}{c^{2}}$",
"a6_cauda":      r"$h\nu\gg kT:\quad B_\nu\to\frac{2h\nu^{3}}{c^{2}}\,e^{-h\nu/kT}$",
"a6_wien_ded":   r"$\frac{d}{d\lambda}\!\left[\frac{\lambda^{-5}}{e^{x}-1}\right]=0\ \Longrightarrow\ 5\left(1-e^{-x}\right)=x$",
"a6_wien_raiz":  r"$x_{\mathrm{max}}=4{,}965\,,\qquad \lambda_{\mathrm{max}}T=\frac{hc}{4{,}965\,k}=2{,}898\times10^{-3}\ \mathrm{m\,K}$",
"a6_sb_int":     r"$F=\pi\!\int_0^\infty\!\!B_\nu\,d\nu=\frac{2\pi h}{c^{2}}\left(\frac{kT}{h}\right)^{4}\!\int_0^{\infty}\!\frac{x^{3}}{e^{x}-1}dx$",
"a6_zeta":       r"$\int_0^{\infty}\frac{x^{3}}{e^{x}-1}dx=\Gamma(4)\,\zeta(4)=\frac{\pi^{4}}{15}$",
"a6_sigma":      r"$\sigma=\frac{2\pi^{5}k^{4}}{15\,c^{2}h^{3}}=5{,}670\times10^{-8}\ \mathrm{W\,m^{-2}\,K^{-4}}$",
"a6_arad":       r"$u=aT^{4}\,,\qquad a=\frac{4\sigma}{c}=7{,}566\times10^{-16}\ \mathrm{J\,m^{-3}\,K^{-4}}$",
"a6_prad":       r"$P_{\mathrm{rad}}=\frac{1}{3}aT^{4}$",
"a6_einstein":   r"$n_1B_{12}\bar{J}=n_2A_{21}+n_2B_{21}\bar{J}$",
"a6_einst_rel":  r"$g_1B_{12}=g_2B_{21}\,,\qquad A_{21}=\frac{2h\nu_0^{3}}{c^{2}}B_{21}$",
"a6_boltz":      r"$\frac{n_2}{n_1}=\frac{g_2}{g_1}\,e^{-(E_2-E_1)/kT}$",
"a6_saha":       r"$\frac{n_{i+1}}{n_i}=\frac{2Z_{i+1}}{n_e Z_i}\left(\frac{2\pi m_e kT}{h^{2}}\right)^{3/2}\!e^{-\chi_i/kT}$",
"a6_dop_rel":    r"$\frac{\lambda_{\mathrm{obs}}}{\lambda_0}=\sqrt{\frac{1+\beta}{1-\beta}}\,,\qquad \beta=\frac{v}{c}$",
"a6_dop_tr":     r"$\frac{\lambda_{\mathrm{obs}}}{\lambda_0}=\gamma\qquad(\mathrm{Doppler\ transversal})$",
"a6_z":          r"$1+z=\frac{1}{a(t_{\mathrm{emis}})}$",
"a6_natural":    r"$\Delta E\simeq\frac{\hbar}{\Delta t}\ \Longrightarrow\ \Delta\nu\simeq\frac{1}{2\pi\Delta t}$",
"a6_dopwidth":   r"$\frac{\Delta\lambda}{\lambda_0}=\frac{1}{c}\sqrt{\frac{2kT}{m}}$",
"a6_mu":         r"$\mu\,\frac{dI}{d\tau}=I-S\,,\qquad \mu=\cos\theta$",
"a6_JHK":        r"$J=\frac{1}{2}\!\int_{-1}^{1}\!I\,d\mu\,,\quad H=\frac{1}{2}\!\int_{-1}^{1}\!I\mu\,d\mu\,,\quad K=\frac{1}{2}\!\int_{-1}^{1}\!I\mu^{2}d\mu$",
"a6_mom0":       r"$\frac{dH}{d\tau}=J-S\ \ \Longrightarrow\ \ J=S$",
"a6_mom1":       r"$\frac{dK}{d\tau}=H$",
"a6_edd":        r"$K=\frac{J}{3}\ \Longrightarrow\ \frac{dJ}{d\tau}=3H\ \Longrightarrow\ J(\tau)=H(3\tau+2)$",
"a6_Ttau":       r"$T^{4}(\tau)=\frac{3}{4}T_{\mathrm{ef}}^{4}\left(\tau+\frac{2}{3}\right)$",
"a6_eb":         r"$I(0,\mu)=\int_0^{\infty}\!S(\tau)\,e^{-\tau/\mu}\frac{d\tau}{\mu}\ \ \Longrightarrow\ \ I(0,\mu)=a+b\mu$",
"a6_limbo":      r"$\frac{I(0,\mu)}{I(0,1)}=\frac{2+3\mu}{5}\ \ \Longrightarrow\ \ u=\frac{3}{5}=0{,}6$",
"a6_thomson":    r"$\kappa_{\mathrm{es}}=\frac{\sigma_T n_e}{\rho}=0{,}02\,(1+X)\ \mathrm{m^{2}\,kg^{-1}}$",
"a6_kramers":    r"$\kappa_{\mathrm{ff}}\ \propto\ \rho\,T^{-7/2}$",
"a6_rosseland":  r"$\frac{1}{\kappa_R}=\frac{\int_0^{\infty}\kappa_\nu^{-1}\,(\partial B_\nu/\partial T)\,d\nu}{\int_0^{\infty}(\partial B_\nu/\partial T)\,d\nu}$",
"a6_sinc_P":     r"$P_{\mathrm{sinc}}=\frac{4}{3}\sigma_T c\,\gamma^{2}\beta^{2}u_B\,,\qquad u_B=\frac{B^{2}}{2\mu_0}$",
"a6_sinc_nu":    r"$\nu_c\simeq\frac{3}{4\pi}\,\gamma^{2}\,\frac{eB}{m_e}$",
"a6_sinc_F":     r"$N(\gamma)\propto\gamma^{-p}\ \Longrightarrow\ F_\nu\propto\nu^{-(p-1)/2}$",
"a6_sinc_07":    r"$p\simeq2{,}4\ \Longrightarrow\ F_\nu\propto\nu^{-0{,}7}$",
"a6_lab3":       r"$\lambda_{\mathrm{max}}T=2{,}898\times10^{-3}\,,\quad F=\int\! F_\lambda\,d\lambda\,,\quad F=\left(\frac{R_\odot}{d}\right)^{2}\!\sigma T_{\mathrm{ef}}^{4}$",
}

os.makedirs(SAIDA, exist_ok=True)
erros = []
for nome, tex in EQ.items():
    try:
        fig = plt.figure(figsize=(0.01, 0.01))
        fig.text(0, 0, tex, fontsize=TAM, color=COR)
        fig.savefig(os.path.join(SAIDA, nome + ".svg"), format="svg",
                    transparent=True, bbox_inches="tight", pad_inches=PAD)
        plt.close(fig)
    except Exception as e:
        erros.append((nome, str(e)[:160]))
print("geradas: %d/%d" % (len(EQ) - len(erros), len(EQ)))
for n, e in erros:
    print("  ERRO %s: %s" % (n, e))
sys.exit(1 if erros else 0)
