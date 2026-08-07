import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# --- CONFIGURACIÓN GLOBAL DE ESTILOS PARA EL PAPER ---
plt.rcParams.update({
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 8.5,
    'legend.labelspacing': 0.45  # Espaciado base cómodo para la lectura vertical
})

archivos = [
    'lvdsl_k_theory_potentials_lifting_fitness_tictac_test.csv',
    'lvdsl_k_theory_potentials_lifting_fitness_tictac_test-1.csv',
    'lvdsl_k_theory_potentials_lifting_fitness_tictac_test-2.csv'
]

# --- DEFINICIÓN DE PALETAS DE COLORES PERSONALIZADAS POR RUN ---
estilos_runs = {
    0: {'puntos': '#fca5a5', 'l1': 'tomato', 'l2': 'red', 'l3': 'darkred'},          # Run 1: Gama Roja
    1: {'puntos': '#93c5fd', 'l1': 'deepskyblue', 'l2': 'royalblue', 'l3': 'navy'}, # Run 2: Gama Azul
    2: {'puntos': '#86efac', 'l1': 'lime', 'l2': 'forestgreen', 'l3': 'darkgreen'}  # Run 3: Gama Verde
}

# --- CREACIÓN DE LA FIGURA COMPACTA (1 fila, 2 columnas) ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.5))
sns.set_theme(style="whitegrid")

# Listas auxiliares para almacenar manualmente los handles y labels de las leyendas
handles_l, labels_l = [], []
handles_r, labels_r = [], []

# Procesar cada archivo de forma estrictamente independiente
for i, archivo in enumerate(archivos):
    try:
        # Cargar el CSV original
        data_raw = pd.read_csv(archivo)

        # CRUCIAL: Ordenar los datos explícitamente por 'N' de forma ascendente
        # para evitar sesgos estructurales y garantizar un flujo limpio
        data_run = data_raw.sort_values(by='N').reset_index(drop=True)

        run_num = i + 1
        cfg = estilos_runs[i]

        # Vectores de la corrida actual debidamente ordenados
        X_run = data_run['N'].values.reshape(-1, 1)
        y_t = data_run['t'].values
        y_tinv = 1.0 / y_t

        # Eje X denso para curvas suaves basadas en los límites reales ordenados
        X_line = np.logspace(np.log10(X_run.min()), np.log10(X_run.max()), 200).reshape(-1, 1)

        # Inicializar transformadores polinomiales
        poly2 = PolynomialFeatures(degree=2)
        poly3 = PolynomialFeatures(degree=3)

        # Separador ligero entre grupos en la leyenda vertical (excepto antes del primer grupo)
        if i > 0:
            proxy_space = plt.plot([], [], color='none')[0]
            handles_l.append(proxy_space); labels_l.append("")
            handles_r.append(proxy_space); labels_r.append("")

        # ---------------------------------------------------------------------
        # PANEL IZQUIERDO: N vs t
        # ---------------------------------------------------------------------
        # Puntos originales ordenados
        sc1 = ax1.scatter(X_run, y_t, color=cfg['puntos'], alpha=0.5, s=20)
        handles_l.append(sc1); labels_l.append(f'Run {run_num} Data')

        # Ajuste Lineal
        m1 = LinearRegression().fit(X_run, y_t)
        ln1 = ax1.semilogx(X_line, m1.predict(X_line), color=cfg['l1'], lw=1.2, linestyle=':')[0]
        handles_l.append(ln1); labels_l.append(f'  Lin: y={m1.coef_[0]:.1e}x')

        # Ajuste Cuadrático
        m2 = LinearRegression().fit(poly2.fit_transform(X_run), y_t)
        ln2 = ax1.semilogx(X_line, m2.predict(poly2.transform(X_line)), color=cfg['l2'], lw=1.4, linestyle='--')[0]
        handles_l.append(ln2); labels_l.append(f'  Quad')

        # Ajuste Cúbico
        m3 = LinearRegression().fit(poly3.fit_transform(X_run), y_t)
        ln3 = ax1.semilogx(X_line, m3.predict(poly3.transform(X_line)), color=cfg['l3'], lw=1.6, linestyle='-')[0]
        handles_l.append(ln3); labels_l.append(f'  Cubic')

        # ---------------------------------------------------------------------
        # PANEL DERECHO: N vs t^-1
        # ---------------------------------------------------------------------
        # Puntos originales inversos ordenados
        sc2 = ax2.scatter(X_run, y_tinv, color=cfg['puntos'], alpha=0.5, s=20)
        handles_r.append(sc2); labels_r.append(f'Run {run_num} Data')

        # Ajuste Lineal para t_inv
        m1_inv = LinearRegression().fit(X_run, y_tinv)
        ln1_inv = ax2.semilogx(X_line, m1_inv.predict(X_line), color=cfg['l1'], lw=1.2, linestyle=':')[0]
        handles_r.append(ln1_inv); labels_r.append(f'  Lin: y={m1_inv.coef_[0]:.1e}x')

        # Ajuste Cuadrático para t_inv
        m2_inv = LinearRegression().fit(poly2.transform(X_run), y_tinv)
        ln2_inv = ax2.semilogx(X_line, m2_inv.predict(poly2.transform(X_line)), color=cfg['l2'], lw=1.4, linestyle='--')[0]
        handles_r.append(ln2_inv); labels_r.append(f'  Quad')

        # Ajuste Cúbico para t_inv
        m3_inv = LinearRegression().fit(poly3.transform(X_run), y_tinv)
        ln3_inv = ax2.semilogx(X_line, m3_inv.predict(poly3.transform(X_line)), color=cfg['l3'], lw=1.6, linestyle='-')[0]
        handles_r.append(ln3_inv); labels_r.append(f'  Cubic')

    except FileNotFoundError:
        print(f"Advertencia: No se encontró {archivo}")

# Configuración final de ejes y despliegue de las leyendas alineadas
ax1.set_xscale('log')
ax1.set_title(r'$N$ vs. $t$')
ax1.set_xlabel(r'$N$ (log)')
ax1.set_ylabel(r'$t$ (seconds)')
ax1.legend(handles=handles_l, labels=labels_l, loc='upper left', frameon=True)

ax2.set_xscale('log')
ax2.set_title(r'$N$ vs. $t^{-1}$')
ax2.set_xlabel(r'$N$ (log)')
ax2.set_ylabel(r'$t^{-1}$')
ax2.legend(handles=handles_r, labels=labels_r, loc='upper right', frameon=True)

# --- GUARDAR EN FORMATO VECTORIAL PARA LATEX ---
plt.tight_layout()
plt.savefig('k_theory_sorted_independent_analysis.pdf', bbox_inches='tight', dpi=300)
plt.show()
