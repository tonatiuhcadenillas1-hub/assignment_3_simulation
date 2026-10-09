"""Analisis estadistico de los experimentos del PA3.

Uso:  python analisis.py   (desde la carpeta experimentos/)
Requiere: pandas, numpy, scipy, statsmodels, matplotlib
Lee resultados_crudos/*.csv y genera resumen/*.csv y graficos/*.png
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf

os.makedirs("resumen", exist_ok=True)
os.makedirs("graficos", exist_ok=True)
m = pd.read_csv("resultados_crudos/resultados_matriz.csv")
d = pd.read_csv("resultados_crudos/resultados_demanda.csv")
for df in (m, d):
    df["pct_terminadas"] = df.terminadas / df.llegadas * 100

INDICADORES = ["llegadas", "terminadas", "wip", "pct_terminadas", "cola_ensamblaje_media",
               "cola_pruebas_media", "tiempo_medio_sistema_min", "produccion_hora",
               "utilizacion_operarios", "utilizacion_mesas"]

def resumen(df, claves):
    filas = []
    for k, g in df.groupby(claves):
        k = k if isinstance(k, tuple) else (k,)
        fila = dict(zip(claves, k), n=len(g))
        n = len(g); t = stats.t.ppf(0.975, n - 1)
        for c in INDICADORES:
            s = g[c].std(ddof=1)
            fila[c + "_media"] = round(g[c].mean(), 4)
            fila[c + "_de"] = round(s, 4)
            fila[c + "_ic95"] = round(t * s / np.sqrt(n), 4)
        filas.append(fila)
    return pd.DataFrame(filas)

resumen(m, ["operarios", "mesas"]).to_csv("resumen/resumen_variacion_recursos.csv", index=False)
resumen(d, ["factor_demanda"]).to_csv("resumen/resumen_sensibilidad_demanda.csv", index=False)

# Pruebas estadisticas
pruebas = []
for c in ["pct_terminadas", "tiempo_medio_sistema_min"]:
    tabla = sm.stats.anova_lm(smf.ols(f"{c} ~ C(operarios) * C(mesas)", data=m).fit(), typ=2)
    for factor, r in tabla.dropna().iterrows():
        pruebas.append(dict(prueba="ANOVA 2 factores", indicador=c, comparacion=factor,
                            estadistico=round(r.F, 3), p_valor=round(r["PR(>F)"], 4)))
sel = lambda o, me, c: m[(m.operarios == o) & (m.mesas == me)][c]
for (o, me) in [(3, 1), (2, 3), (3, 2), (3, 3), (4, 2), (4, 3)]:
    for c in ["pct_terminadas", "tiempo_medio_sistema_min"]:
        r = stats.ttest_ind(sel(o, me, c), sel(2, 2, c), equal_var=False)
        pruebas.append(dict(prueba="t de Welch", indicador=c, comparacion=f"{o}x{me} vs 2x2",
                            diferencia=round(sel(o, me, c).mean() - sel(2, 2, c).mean(), 3),
                            estadistico=round(r.statistic, 3), p_valor=round(r.pvalue, 4)))
for c in ["tiempo_medio_sistema_min", "pct_terminadas", "wip"]:
    r = stats.f_oneway(*[d[d.factor_demanda == f][c] for f in (0.8, 1.0, 1.2)])
    pruebas.append(dict(prueba="ANOVA 1 factor (demanda)", indicador=c, comparacion="0.8 / 1.0 / 1.2",
                        estadistico=round(r.statistic, 3), p_valor=round(r.pvalue, 4)))
pd.DataFrame(pruebas).to_csv("resumen/pruebas_estadisticas.csv", index=False)

# Graficos
plt.rcParams.update({"font.size": 10})
t9 = stats.t.ppf(0.975, 9)
fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
for a, (c, tit, cmap) in zip(ax, [("pct_terminadas", "Placas terminadas / llegadas (%)", "RdYlGn"),
                                  ("tiempo_medio_sistema_min", "Tiempo medio en el sistema (min)", "RdYlGn_r")]):
    p = m.groupby(["operarios", "mesas"])[c].mean().unstack()
    a.imshow(p.values, cmap=cmap, aspect="auto", alpha=0.75)
    a.set_xticks(range(3)); a.set_xticklabels([1, 2, 3]); a.set_yticks(range(3)); a.set_yticklabels([2, 3, 4])
    a.set_xlabel("Mesas de pruebas"); a.set_ylabel("Operarios de ensamblaje"); a.set_title(tit, fontsize=11)
    for i in range(3):
        for j in range(3):
            a.text(j, i, f"{p.values[i, j]:.1f}".replace(".", ","), ha="center", va="center", fontsize=12, fontweight="bold")
fig.tight_layout(); fig.savefig("graficos/Fig_Mapa_Calor_Recursos.png", dpi=170); plt.close()

cfg = [(2, 2), (2, 3), (3, 2), (3, 3), (4, 2), (4, 3)]
datos = [sel(o, me, "tiempo_medio_sistema_min") for o, me in cfg]
fig, a = plt.subplots(figsize=(9, 4))
b = a.boxplot(datos, patch_artist=True, widths=0.55, showfliers=False)
for caja, (o, me) in zip(b["boxes"], cfg):
    caja.set_facecolor("#A9D18E" if (o, me) == (2, 2) else "#9DC3E6")
rng = np.random.default_rng(1)
for k, x in enumerate(datos, 1):
    a.scatter(rng.normal(k, 0.05, len(x)), x, s=12, color="#404040", zorder=3)
a.set_xticklabels([f"{o} op.\n{me} mesas" for o, me in cfg]); a.set_ylabel("Tiempo medio en el sistema (min)")
a.grid(axis="y", alpha=0.3)
fig.tight_layout(); fig.savefig("graficos/Fig_Boxplot_Tiempo_Sistema.png", dpi=170); plt.close()

g = d.groupby("factor_demanda"); f = [0.8, 1.0, 1.2]
fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
for c, lab, col in [("utilizacion_operarios", "Operarios", "#00B0B0"), ("utilizacion_mesas", "Mesas de pruebas", "#8064E6")]:
    ax[0].errorbar(f, g[c].mean() * 100, yerr=t9 * g[c].std() * 100 / np.sqrt(10), marker="o", capsize=4, label=lab, color=col)
ax[0].axhline(90, ls="--", color="gray"); ax[0].set_ylim(40, 100)
ax[0].set_xticks(f); ax[0].set_xlabel("Factor de demanda"); ax[0].set_ylabel("Utilización (%)")
ax[0].legend(loc="lower right"); ax[0].set_title("Utilización de recursos (IC 95 %)", fontsize=11); ax[0].grid(alpha=0.3)
c = "tiempo_medio_sistema_min"
ax[1].errorbar(f, g[c].mean(), yerr=t9 * g[c].std() / np.sqrt(10), marker="o", capsize=4, color="#C55A11")
ax[1].set_xticks(f); ax[1].set_xlabel("Factor de demanda"); ax[1].set_ylabel("Minutos")
ax[1].set_title("Tiempo medio en el sistema (IC 95 %)", fontsize=11); ax[1].grid(alpha=0.3); ax[1].set_ylim(0, 8)
fig.tight_layout(); fig.savefig("graficos/Fig_Sensibilidad_Demanda.png", dpi=170); plt.close()
print("Listo: resumen/ y graficos/ actualizados")
