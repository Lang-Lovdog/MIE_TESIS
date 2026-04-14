## Este archivo leerá los directorios VacuaFound y generará un
## resumen de vacíos encontrados junto a un histograma 2d
## obteniendo la cantidad de vacíos dS y AdS, dividiendo las
## Barras en estables e inestables.

import os
import sys
venv_path = os.environ.get('VIRTUAL_ENV')
if venv_path:
    cuda_lib_path = os.path.join(venv_path, 'lib', f'python{sys.version_info.major}.{sys.version_info.minor}', 'site-packages', 'nvidia')
    if os.path.exists(cuda_lib_path):
        os.environ['CUDA_PATH'] = cuda_lib_path
        # Añadimos las subcarpetas de nvrtc y cuda_runtime al PATH del sistema
        os.environ['LD_LIBRARY_PATH'] = f"{cuda_lib_path}/cuda_runtime/lib:{cuda_lib_path}/nvrtc/lib:{cuda_lib_path}:{os.environ.get('LD_LIBRARY_PATH', '')}"
from sympy import lambdify
import pandas
import json
import datetime
import matplotlib.pyplot as plt
#import numpy as np
import cupy as np
from MetastableVacua import V, AH3 , AF3 , AF5 , A3N3, AD5 , tau , s
v_gpu_func = lambdify((AH3, AF3, AF5, A3N3, AD5, tau, s), V, modules='cupy')


## Los archivos serán almacenados en un directorio
# | pwd/
# |- SolutionsCounter.py
# |- SolutionsCounter_Resumen/
# |=-
# |-- ResumenDel[DDMMAAAA].json     > El archivo tendrá la forma:
# |                                  "post lift"{
# |                                     "dS":  { "stable": [int], "unstable": [int] },
# |                                     "AdS": { "stable": [int], "unstable": [int] },
# |                                  }
# |                                  "pre lifting"{
# |                                     "dS":  { "stable": [int], "unstable": [int] },
# |                                     "AdS": { "stable": [int], "unstable": [int] },
# |                                  }
# |                                 ||
# |-- HistogramaDel[DDMMAAAA].eps   > Histograma de barra dividida con base en dS AdS y división por estabilidad ||
# |-- DescripcionDeResumen.txt      > El archivo tendrá la forma:
# |                                   [DDMMAAAA]
# |                                   Archivos:
# |                                   VacuaFoundXXYYZZZZ/
# |                                   VacuaFoundAABBCCCC/
# |                                   Registros ignorados
# |                                   a,b,c,... (int)
# |                                   ...
# |                                 ||
# |==

nombre_generico_directorio_guardado = "SolutionsCounter_Resumen/"
nombre_generico_archivo____guardado = "ResumenDelDATE.json"
nombre_generico_grafica1___guardado = "Histograma1DATE.eps"
nombre_generico_grafica2___guardado = "Histograma2DATE.eps"
nombre = {
    "directorio": nombre_generico_directorio_guardado,
    "resumen": nombre_generico_directorio_guardado + nombre_generico_archivo____guardado.replace("DATE", datetime.datetime.now().strftime("%d%m%Y")),
    "grafica1": nombre_generico_directorio_guardado + nombre_generico_grafica1___guardado.replace("DATE", datetime.datetime.now().strftime("%d%m%Y")),
    "grafica2": nombre_generico_directorio_guardado + nombre_generico_grafica2___guardado.replace("DATE", datetime.datetime.now().strftime("%d%m%Y")),
    "fecha": datetime.datetime.now().strftime("%d%m%Y"),
    "descripcion": nombre_generico_directorio_guardado + "DescripcionDeResumen.txt"
}

# LLNCS text width is approx 12.2cm (~4.8 inches)
# If using two side-by-side plots, each should be ~2.3 inches
fig_width_inches = 3.35
fig_height_inches = fig_width_inches * 0.8  # Slightly taller to accommodate bar labels

plt.rcParams.update({
    "font.size": 10,
    "axes.labelsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.figsize": (12.0, 12.0), # Más ancho para que respire el eje X
    "text.usetex": True,
    "font.family": "serif",
#    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.2    # Un poco más de borde para que nada se corte
})

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

def __crear_dir__():
    global nombre
    os.path.isdir(nombre["directorio"]) or os.mkdir(nombre["directorio"])
    return

def __leer_csv__(path:str, df:pandas.DataFrame=None):
    ## col index and header exists
    ndf = pandas.read_csv(path, index_col=0, sep=",", dtype=str)
    if df is None or df.empty:
        df = ndf
        return df
    df= pandas.concat([df, ndf])
    return df

def __comprueba_indice__(indices_excluidos:list, nombre:str):
    if indices_excluidos is None:
        return True
    nombre_generico="found_solutions_AdS_fv_"
    nombre_index=nombre.replace(nombre_generico, "").replace(".csv", "")
    try:
        if int(nombre_index) in indices_excluidos:
            return False
        return True
    except ValueError:
        # print("El archivo no es valido:", nombre)
        # print("Error provocado:", ValueError)
        # print("Ignorando entrada")
        return False

def __obtener_datos__(dir_list:list, indices_excluidos:list[int]):
    df = pandas.DataFrame()
    contador = 0
    for dir in dir_list:
       ## Get each file from the directory
       for root, dirs, files in os.walk(dir):
           for file in files:
               path = os.path.join(root, file)
               if __comprueba_indice__(indices_excluidos, file):
                   df = __leer_csv__(path, df)
                   contador = contador + 1
    print("Archivos leidos:", contador)
    print("Total de registros:", len(df))
    return df

def __get_eval_dataframe__(df:pandas.DataFrame):
    print("Evaluando potencial en GPU...")

    # Convert Pandas columns to CuPy arrays (Transfers data to VRAM once)
    # Use .values to get the raw underlying data
    v_values = v_gpu_func(
        np.array(pandas.to_numeric(df["AH3"], errors='coerce').values),
        np.array(pandas.to_numeric(df["AF3"], errors='coerce').values),
        np.array(pandas.to_numeric(df["AF5"], errors='coerce').values),
        np.array(pandas.to_numeric(df["A3N3"], errors='coerce').values),
        np.array(pandas.to_numeric(df["AD5"], errors='coerce').values),
        np.array(pandas.to_numeric(df["tau"], errors='coerce').values),
        np.array(pandas.to_numeric(df["s"], errors='coerce').values)
    )

    # Apply the same logic for the stability and pre-lift columns
    evaluaciones = pandas.DataFrame({
        "dS": np.where(v_values > 0, 1, -1).get(),
        "stable": np.where(np.array(pandas.to_numeric(df["taquiónico"], errors='coerce').values) > 0, 0, 1).get(),
        "dS_pre": np.where(np.array(pandas.to_numeric(df["V"], errors='coerce').values) > 0, 1, -1).get()
    })
    return evaluaciones

#def __get_eval_dataframe_legacy__(df:pandas.DataFrame):
#    # Se obtendrá un dataframe con las características de cada solución
#    # Al evaluarse se guardará el un valor de mayor o menor a 0
#    # si la evaluación es mayor a 0 (como 1) o menor a 0 (como -1)
#    # potencial_eval(_AH3, _AF3, _AF5, _A3N3, _tau, _s) > 0 // dS_pre
#    # Y se guardarán el valor de la columna taquiónico   // stable
#    # y si V es mayor a 0 (como 1) o menor a 0 (como -1) // dS
#    print("Evaluando potencial")
#    v_values = df.apply(
##        lambda r: potencial_eval(r["AH3"], r["AF3"], r["AF5"], r["A3N3"], r["tau"], r["s"]),
#        axis=1
#    )
#    evaluaciones = pandas.DataFrame({
#        "dS": np.where(v_values > 0, 1, -1),
#        "stable": np.where(df["taquiónico"].astype(float) > 0, 0, 1),
#        "dS_pre": np.where(df["V"].astype(float) > 0, 1, -1)
#    })
#    return evaluaciones

def __conteo__(df:pandas.DataFrame):
    global nombre
    df_eval = __get_eval_dataframe__(df)
    # Conteo de dS estables y ds no estables
    stable____dS =   ((df_eval["dS"    ] ==  1) & (df_eval["stable"] ==  1)).sum()
    unstable__dS =   ((df_eval["dS"    ] ==  1) & (df_eval["stable"] ==  0)).sum()
    # Conteo de AdS estables y ds no estables
    stable___AdS =   ((df_eval["dS"    ] == -1) & (df_eval["stable"] ==  1)).sum()
    unstable_AdS =   ((df_eval["dS"    ] == -1) & (df_eval["stable"] ==  0)).sum()
    # Conteo de dS previos al levantamiento
    dS_previo__dS =  ((df_eval["dS_pre"] ==  1) & (df_eval["dS"    ] ==  1)).sum()
    dS_previo_AdS =  ((df_eval["dS_pre"] ==  1) & (df_eval["dS"    ] == -1)).sum()
    # Conteo de AdS previos al levantamiento
    AdS_previo__dS = ((df_eval["dS_pre"] == -1) & (df_eval["dS"    ] ==  1)).sum()
    AdS_previo_AdS = ((df_eval["dS_pre"] == -1) & (df_eval["dS"    ] == -1)).sum()
    print("Armando concentrado de resultados")
    resultados = {
        "lifted": {
            "dS": {
                "stable": stable____dS,
                "unstable": unstable__dS
            },
            "AdS": {
                "stable": stable___AdS,
                "unstable": unstable_AdS
            }
        },
        "unlifted":{
            "dS": {
                "to dS":  dS_previo__dS,
                "to AdS": dS_previo_AdS
            },
            "AdS": {
                "to dS":  AdS_previo__dS,
                "to AdS": AdS_previo_AdS
            }
        },
        "total": len(df),
    }
    print("Guardando resultados en JSON")
    with open(nombre["resumen"], "w") as f:
        json.dump(resultados, f, cls=NpEncoder, indent=4)
    return resultados

def __plot_registros_estabilidad__(resultados:dict):
    global nombre
    # Plot dS vs AdS histogram, with stability coloring per bar
    # Configuración estética para tesis

    # Extracción de datos del diccionario
    categorias = ['de Sitter (dS)', 'Anti-de Sitter (AdS)']
    estables = [
        resultados["lifted"]["dS"]["stable"],
        resultados["lifted"]["AdS"]["stable"]
    ]
    inestables = [
        resultados["lifted"]["dS"]["unstable"],
        resultados["lifted"]["AdS"]["unstable"]
    ]

    x = np.arange(len(categorias)).get()  # Localización de las etiquetas
    width = 0.25  # Ancho de las barras

    fig, ax = plt.subplots(figsize=(fig_width_inches, fig_height_inches))

    # Creación de las barras
    rects1 = ax.bar(x - width/2, estables, width, label='Estables',
                    color='#2ecc71', edgecolor='black', alpha=0.8)
    rects2 = ax.bar(x + width/2, inestables, width, label='Inestables',
                    color='#e74c3c', edgecolor='black', alpha=0.8)

    # Etiquetas y títulos profesionales
    ax.set_ylabel(r'$N$')
    #ax.set_title(r'\textbf{Análisis de Estabilidad en el Paisaje de Cuerdas}')
    ax.set_xticks(x)
    ax.set_xticklabels(categorias)
    ax.legend()

    # Añadir etiquetas de valor sobre las barras
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    plt.tight_layout()
    max_val = max(max(estables), max(inestables))
    ax.set_ylim(0, max_val * 1.29)

    # Guardar en PDF para insertar en LaTeX sin pérdida de calidad
    print("Guardando gráfica1: Categorías por estabilidad")
    plt.savefig(nombre["grafica1"], bbox_inches="tight")
    # plt.show()

def __plot_registros_levantamiento__(resultados:dict):
    global nombre
    # Extraemos los datos del diccionario 'unlifted'
    # ds_previo_* -> Eran dS antes del uplift
    # AdS_previo_* -> Eran AdS antes del uplift
    categorias_originales = [r'$dS_{pre}$', r'$AdS_{pre}$']

    final_ds = [
        resultados["unlifted"]["dS"]["to dS"],
        resultados["unlifted"]["AdS"]["to dS"]
    ]
    final_ads = [
        resultados["unlifted"]["dS"]["to AdS"],
        resultados["unlifted"]["AdS"]["to AdS"]
    ]

    x = np.arange(len(categorias_originales)).get()
    width = 0.25

    fig, ax = plt.subplots(figsize=(fig_width_inches, fig_height_inches))

    # Barras de destino
    rects1 = ax.bar(x - width/2, final_ds, width, label='dS',
                    color='#3498db', edgecolor='black', alpha=0.8)
    rects2 = ax.bar(x + width/2, final_ads, width, label='AdS',
                    color='#95a5a6', edgecolor='black', alpha=0.8)

    # Configuración de ejes
    ax.set_ylabel(r'$N$')
#    ax.set_xlabel(r'Estado Original (Sin Levantamiento)')
    #ax.set_title(r'\textbf{Transiciones de Vacío post-Levantamiento}')
    ax.set_xticks(x)
    ax.set_xticklabels(categorias_originales)
    ax.legend(title="Final State")

    # Añadir etiquetas de conteo
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    plt.tight_layout()
    max_val = max(max(final_ds), max(final_ads))
    ax.set_ylim(0, max_val * 1.29)

    print("Guardando gráfica2: Transcisiones de Vacío post-Levantamiento")
    plt.savefig(nombre["grafica2"], bbox_inches="tight")
    # plt.show()

if __name__ == "__main__":
    print(f"CUDA Device: {np.cuda.runtime.getDeviceCount()} detected")
    print(f"Using Device: {np.cuda.Device(0)}")
    dirs = [
        "VacuaFound_17022026",
        "VacuaFound_11032026",
        "VacuaFound_10032026",
        "VacuaFound_09032026",
    ]
    #excluded = [ x for x in np.arange(50,100) ]
    excluded:list[int] = []
    df = __obtener_datos__(dirs, excluded)
    __crear_dir__()
    print("Conteo de soluciones:")
    res=__conteo__(df)
    json_res = json.dumps(res, cls=NpEncoder, indent=4)
    print(json_res)
    np.get_default_memory_pool().free_all_blocks()
    __plot_registros_estabilidad__(res)
    __plot_registros_levantamiento__(res)
    print("Guardando log")
    with open(nombre["descripcion"], "w") as f:
        f.write("["+nombre["fecha"]+"]\n")
        f.write("Archivos analizados:\n")
        f.write("\n".join(dirs))
        if len(excluded) > 0:
            f.write("\nArchivos excluidos:\n")
            f.write("\n".join([str(x) for x in excluded]))

