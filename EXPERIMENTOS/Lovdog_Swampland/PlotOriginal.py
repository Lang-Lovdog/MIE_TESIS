import os
import sys

venv_path = os.environ.get('VIRTUAL_ENV')
if venv_path:
    cuda_lib_path = os.path.join(venv_path, 'lib', f'python{sys.version_info.major}.{sys.version_info.minor}', 'site-packages', 'nvidia')
    if os.path.exists(cuda_lib_path):
        os.environ['CUDA_PATH'] = cuda_lib_path
        # Añadimos las subcarpetas de nvrtc y cuda_runtime al PATH del sistema
        os.environ['LD_LIBRARY_PATH'] = f"{cuda_lib_path}/nvrtc/lib:{cuda_lib_path}/cuda_runtime/lib:{os.environ.get('LD_LIBRARY_PATH', '')}"

import matplotlib
matplotlib.use('Cairo')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.lines as mlines
from matplotlib.colors import LightSource
import numpy as np
try:
    import cupy
    HAS_GPU = True
    xp = cupy
except ImportError:
    print("No se pudo importar cupy. Usando numpy.")
    xp = np

from sympy import lambdify
from MetastableVacua import V_lifting, V, AH3 , AF3 , AF5 , A3N3, AD5 , tau , s
from test_fitness_function import datos_del_csv_mathematica, variables

# --- VARIABLES GLOBALES DE PREPARACIÓN ---
# Creamos la "plantilla" numérica una sola vez
SIMBOLOS_POTENCIAL  = (s, tau, AH3, AF3, AF5, A3N3, AD5)
SIMBOLOS_POTENCIAL1 = (s, tau, AH3, AF3, AF5, A3N3)
V_NUMERIC_BASE = lambdify(SIMBOLOS_POTENCIAL, V_lifting, "numpy")
V_NO_LIFTING   = lambdify(SIMBOLOS_POTENCIAL1, V, "numpy")

directory="OriginalSolutions/"
generic_name="Solution-XYZ.eps"

def calcular_malla_gpu(s0, tau0, params):
    """Calcula la superficie V(s, tau) usando la GPU."""
    # Generamos los vectores en la CPU y los subimos a la GPU
    s_vec = xp.linspace(0.01 * s0, 2.3 * s0, 150)
    tau_vec = xp.linspace(0.01 * tau0, 5.9 * tau0, 150)
    S, T = xp.meshgrid(s_vec, tau_vec)

    # Ejecución en paralelo en los núcleos CUDA de tu NVIDIA
    # V_NUMERIC_BASE acepta arreglos de CuPy porque son compatibles con la interfaz de NumPy
    Z_gpu = V_NUMERIC_BASE(S, T, *params)

    # Bajamos el resultado a la CPU para Matplotlib
    return T.get(), S.get(), Z_gpu.get()

def guardar_grafica_profesional(fig, nombre="Potencial_Final"):
    fig.set_size_inches(8, 6) # Un poco más grande ayuda a la claridad

    # Aseguramos que el nombre no duplique extensiones
    path_final = nombre if nombre.endswith(".eps") else f"{nombre}.eps"

    # El secreto del EPS profesional:
    fig.savefig(path_final, format='eps',
                bbox_inches='tight',
                dpi=1200, # DPI muy alto para que las texturas LightSource sean suaves
                transparent=False)

def generar_plot_3d(s0, tau0, AH3_val, AF3_val, AF5_val, A3N3_val, AD5_val, index:int):
    # --- [Cálculo de Malla con xp (GPU/CPU) ya definido] ---
    params  = [float(x) for x in [AH3_val, AF3_val, AF5_val, A3N3_val, AD5_val]]
    params2 = [float(x) for x in [AH3_val, AF3_val, AF5_val, A3N3_val]]

    # 1. Preparar datos para 3D (Superficie)
    s_vals   = xp.linspace(0.01 * s0, 2.3 * s0, 200)
    tau_vals = xp.linspace(0.01 * tau0, 5.9 * tau0, 200)
    S, T  = xp.meshgrid(s_vals, tau_vals)
    Z_3d = V_NUMERIC_BASE(S, T, *params)
    Z_3s = V_NO_LIFTING  (S, T, *params2)

    # 2. Preparar datos para 2D (Cortes en el punto de la solución)
    # Corte 1: Variando tau, fijando s = s0
    z_fixed_s    = V_NUMERIC_BASE(s0, tau_vals, *params)
    z_fixed_s_no = V_NO_LIFTING(s0, tau_vals, *params2)
    # Corte 2: Variando s, fijando tau = tau0
    z_fixed_tau    = V_NUMERIC_BASE(s_vals, tau0, *params)
    z_fixed_tau_no = V_NO_LIFTING(s_vals, tau0, *params2)

    if HAS_GPU:
        S, T, Z_3d, Z_3s = S.get(), T.get(), Z_3d.get(), Z_3s.get()
        z_fixed_s,    z_fixed_tau    = z_fixed_s.get(),    z_fixed_tau.get()
        z_fixed_s_no, z_fixed_tau_no = z_fixed_s_no.get(), z_fixed_tau_no.get()
        s_vals, tau_vals = s_vals.get(), tau_vals.get()

    # --- RENDERIZADO ---
    plt.rcParams.update({"text.usetex": True, "font.family": "serif"})
    fig = plt.figure(figsize=(14, 10))
    gs = gridspec.GridSpec(2, 2, height_ratios=[1, 2]) # 2 filas: arriba 2D, abajo 3D

    # Gráfica 2D Izquierda: Corte en tau (s fijo)
    ax_s = fig.add_subplot(gs[0, 0])
    ax_s.plot(tau_vals, z_fixed_s,    color='blue',  lw=1.5,          label='Lifting')
    ax_s.plot(tau_vals, z_fixed_s_no, color='black', lw=1,   ls='--', label='No Lifting')
    ax_s.legend(fontsize='small')

    ax_s.axvline(tau0, color='red', linestyle='--', alpha=0.5)
    ax_s.set_title(r"Sección $V(\tau)$ con $s$ fijo")
    ax_s.set_xlabel(r"$\tau$")
    ax_s.set_ylabel(r"$V_{eff}$")
    ax_s.set_ylim(-0.09, 0.09)

    # Gráfica 2D Derecha: Corte en s (tau fijo)
    ax_tau = fig.add_subplot(gs[0, 1])
    ax_tau.plot(s_vals, z_fixed_tau, color='green', lw=1.5, label='Lifting')
    ax_tau.plot(s_vals, z_fixed_tau_no, color='gray', lw=1, ls='--', label='No Lifting')

    ax_tau.legend(fontsize='small')
    ax_tau.axvline(s0, color='red', linestyle='--', alpha=0.5)
    ax_tau.set_title(r"$V(s)$, fixed $\tau$")
    ax_tau.set_xlabel(r"$s$")
    ax_tau.set_ylim(-0.09, 0.09)

    # Gráfica 3D (Perspectiva al Origen)
    ls = LightSource(azdeg=225, altdeg=45) # Ángulo estándar de literatura
    rgb_lift = ls.shade(Z_3d, cmap=plt.get_cmap('viridis'), blend_mode='soft')
    rgb_pre  = ls.shade(Z_3s, cmap=plt.get_cmap('viridis'), blend_mode='soft')

    Z_3d = np.clip(Z_3d, -1, 1)
    Z_3d[Z_3d >  0.9] = np.nan
    Z_3d[Z_3d < -0.9] = np.nan

    Z_3s = np.clip(Z_3s, -1, 1)
    Z_3s[Z_3s >  0.9] = np.nan
    Z_3s[Z_3s < -0.9] = np.nan

    ax_3s = fig.add_subplot(gs[1, 0], projection='3d') # Izquierda: Pre-lifting
    ax_3s.set_title(r"\textbf{Potential behaviour Pre-Lifting ($V$)}", pad=20)
    ax_3s.contour(T, S, Z_3s, zdir='z', offset=-2, cmap='plasma', alpha=0.5)

    ax_3d = fig.add_subplot(gs[1, 1], projection='3d') # Derecha: Post-lifting
    ax_3d.set_title(r"\textbf{Potential behaviour with Lifting ($V_{lift}$)}", pad=20)
    ax_3d.contour(T, S, Z_3d, zdir='z', offset=-2, cmap='plasma', alpha=0.5)

    surf2 = ax_3s.plot_surface(T, S, Z_3s, facecolors=rgb_pre,
                               rcount=100, ccount=100,
                               antialiased=False, linewidth=0, shade=False)
    surf = ax_3d.plot_surface(T, S, Z_3d, facecolors=rgb_lift,
                               rcount=100, ccount=100,
                               antialiased=False, linewidth=0, shade=False)
    ax_3s.plot_wireframe(T, S, Z_3s, color='black', lw=0.05, 
                         rstride=20, cstride=20, alpha=0.2)
    ax_3d.plot_wireframe(T, S, Z_3d, color='black', lw=0.05, 
                         rstride=20, cstride=20, alpha=0.2)

    # Configuración de cámara solicitada (Origen 0,0 en primer plano)
    ax_3d.view_init(elev=20, azim=225)
    ax_3s.view_init(elev=20, azim=225)
    # (Ancho tau, Ancho s, Altura V)
    #ax_3d.set_box_aspect((2, 2, 1))
    #ax_3s.set_box_aspect((2, 2, 1))

    # Recorte de energía para ver el vacío y no solo la pared infinita
    #z_min = np.nanmin(Z_3d)
    #z_max = np.nanmax(Z_3d)
    #ax_3d.set_zlim(z_min, z_min + (z_max - z_min) * 0.1)
    ##ax_3d.set_zlim(-0.99, 0.99)
    ##ax_3s.set_zlim(-0.99, 0.99)
    ##ax_3d.set_xlim( 0.00, 8.00)
    ##ax_3s.set_xlim( 0.00, 8.00)
    ##ax_3d.set_ylim( 0.00, 4.00)
    ##ax_3s.set_ylim( 0.00, 4.00)

    # Etiquetas Físicas
    ax_3d.set_xlabel(r'Volumen $\tau$')
    ax_3d.set_ylabel(r'Dilatón $s$')
    ax_3d.set_zlabel(r'$V_{eff}$')

    ax_3s.set_xlabel(r'Volumen $\tau$')
    ax_3s.set_ylabel(r'Dilatón $s$')
    ax_3s.set_zlabel(r'$V_{eff}$')

    titulo_flujos = (
        f"Fluxes contributions: $A_{{H3}}={AH3_val:.2e}, A_{{F3}}={AF3_val:.2e}, "
        f"A_{{F5}}={AF5_val:.2e}, A_{{3N3}}={A3N3_val:.2e}, A_{{D5}}={AD5_val:.2e}$"
    )
    fig.suptitle(titulo_flujos, fontsize=12, fontweight='bold', y=0.98)

    plt.tight_layout(rect=(0, 0.05, 1, 0.95))

    global directory, generic_name
    output_name=generic_name.replace("XYZ", str(index))
    output_name=directory+"/"+output_name
    print(f"Exporting {output_name}")
    #plt.savefig(f"{directory}/{output_name}")
    guardar_grafica_profesional(fig, output_name)
    #plt.show()

def plot_csv_elements(csv: str = "../CESAR-BRITO_ORIGINAL-DATA/Calibracion_lifting.csv", excluded: list[int] = []):
    df = datos_del_csv_mathematica(csv, True)
    print(f"Datos obtenidos de {csv}. Total: {len(df)} elementos.")

    global directory, generic_name
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Usamos .iterrows() para obtener el índice real y los datos de la fila
    for index, row in df.iterrows():
        # Saltamos los elementos que estén en tu lista de excluidos
        if index in excluded:
            continue

        print(f"Graficando elemento {index}...")

        # Accedemos a los datos usando el nombre de la columna de la fila 'row'
        generar_plot_3d(
            s0=float(row[variables["s"]]),
            tau0=float(row[variables["tau"]]),
            AH3_val=float(row[variables["AH3"]]),
            AF3_val=float(row[variables["AF3"]]),
            AF5_val=float(row[variables["AF5"]]),
            A3N3_val=float(row[variables["A3N3"]]),
            AD5_val=float(row[variables["AD5"]]),
            index=index
        )
        # Preguntamos al usuario si desea continuar
        #continue_or_not = input("¿Desea continuar al siguiente elemento? (y/n): ")
        #if continue_or_not.lower() == "n":
        #    break

if __name__ == '__main__':
    plot_csv_elements()

