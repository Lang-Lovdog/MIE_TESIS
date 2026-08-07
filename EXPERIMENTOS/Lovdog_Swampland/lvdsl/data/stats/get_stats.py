## Este script tiene la finalidad de hacer un conteo de las soluciones obtenidas en las carpetas VacuaFound.
## Las estadísticas relevantes al momento serán
##   - Número de soluciones totales
##   - Número de soluciones taquiónicas
##   - Número de valores V_eff definidos negativos
##   - Número de valores V_eff semidefinidos positivos
##   - Número de valores A3N3 definidos negativos
##   - Número de valores A3N3 semidefinidos positivos
##   - Valor promedio por archivo de cada campo
##   - Valor promedio por directorio de cada campo

### Para hacer funcionar este script tendrá una función que recibirá el directorio a analizar


from   lvdsl.xp                    import xp
from   lvdsl.data.from_csv         import read_native_format
from   lvdsl.data.stats.dir_handle import DirHandle
from   natsort                     import humansorted
import pandas #type: ignore
import os
import re
import matplotlib.pyplot                                     as plt
import seaborn                                               as sns

sns.set_theme(style="white", context="paper")
plt.rcParams['font.family'] = 'sans-serif'

dryRun=False

class StatAnalysis:

    #### Banderas
    ## Posibles valores para AnalysisBatch
    ## per_run, per_model, per_path
    ## per_run hace un análisis por cada csv de cada modelo,
    ## per_model hace un análisis de todos los csv de un mismo
    ##  modelo,
    ## per_path hace un análisis de todos los modelos dentro de
    ##  un mismo VacuaFound
    ## El valor por defecto (y más recomendado) es per_model

    AnalysisBatch="per_model"
    AvailableAnalysis={
        "general":[
            "total_solutions",
            "tachyonic_solutions",
        ],
        "V":[
            "min",
            "max",
            "mean",
            "std_dev",
            "variance",
            "negatives",
            "semidef_positives",
        ],
        "A3N3":[
            "min",
            "max",
            "mean",
            "std_dev",
            "variance",
            "negatives",
            "semidef_positives",
        ],
        "vacua":[
            "tachyonic",
            "dS",
            "AdS",
            "stable_ratio", ## Stables Found/Total Found
        ],
    }

    AnalysisToPerform={ str:any }
    data_d = { str:any }
    stats_d = { str:any }
    columns = [ "V" ]

    dir_handle = DirHandle

    ###########################################################
    def __init__(self, DirHandle):
        self.dir_handle = DirHandle
        self.dir_handle.get_test_dirs()
        self.dir_handle.get_test_files()
        self.AnalysisToPerform=self.AvailableAnalysis
        self.outlier_methods = {
            "iqr": self._filter_iqr,
            "percentile": self._filter_percentile,
            "none": lambda series, **kwargs: series  # Identity function (devuelve la serie intacta)
        }

    ###########################################################


    ###########################################################
    def columns_to_analyze(self, columns, append=False):
        if type(columns) is not list:
            columns = [columns]
        if append:
            self.columns.extend(columns)
            return
        self.columns = columns
    ###########################################################


    ###########################################################
    # Regresa el diccionario de estadísticas
    def stats(self):
        return self.stats_d
    ###########################################################


    ###########################################################
    # Esta función es una auxiliar que provee los datos en
    # dataframe de los archivos csv obtenidos.
    # por cuestiones de memoria RAM, los archivos son cargados
    # según son necesarios.
    # existe una bandera en la que se indica si se deben cargar
    # todos los csv especificados (por ejemplo de un modelo) en
    # un mismo dataframe.
    # La carga se hace a través de la utilidad definida en
    # lvdsl
    def load_csv_from_model(self, parent, model, bulk=True):
        dataframes=[]
        # Get all dataframes
        for f in self.dir_handle.get(parent, model, "csv"):
            _f=os.path.join(parent, model, f)
            dataframes.append(read_native_format(_f,0))
        # Unify dataframes
        if bulk:
            return pandas.concat(dataframes)
        return dataframes
    ###########################################################


    ###########################################################
    # Obtiene los datos de los CSV y los guarda en un
    # diccionario catalogado por parent, por parent/model o por
    # parent/model/file
    def get_data(self):
        if self.AnalysisBatch == "per_model":
            self.data_d = {}
            for p in  self.dir_handle.list():
               self.data_d[p]={}
               for n in self.dir_handle.list(p=p):
                   self.data_d[p][n]=self.load_csv_from_model(p,n)
        return self.data_d
    ###########################################################


    ###########################################################
    # Obtiene las estadísticas de la columna dada
    def get_stats(self, outlier_handle:dict={}):
        columns=self.columns
        for p in self.data_d:
            self.stats_d[p]={}
            for n in self.data_d[p]:
                self.stats_d[p][n]={}
                ## Set columns as long double
                for c in columns:
                    self.data_d[p][n][c]= \
                        self.data_d[p][n][c].astype('float64')
                self.get_column_stats(p, n, columns, outlier_handle)
                self.get_vacua_stats(p, n)

    ###########################################################
    # Obtiene las estadísticas de la columna dada
    def get_column_stats(self, p, n, columns, outlier_handle:dict={}):
        for c in columns:
            ## Tratamiento de datos
            series_raw = self.data_d[p][n][c]
            config = outlier_handle.get(c, {})
            method_name = config.get("method", "none")
            params = config.get("params", {})
            if method_name in self.outlier_methods:
                series_clean = self.outlier_methods[method_name](series_raw, **params)
            else:
                series_clean = series_raw
            ## Skewness
            std_dev_clean = xp.std(series_clean)
            mean_clean = xp.mean(series_clean)
            m3 = xp.mean((series_clean - xp.mean(series_clean)) ** 3)
            skewness_val = (m3 / (std_dev_clean ** 3)) if std_dev_clean != 0 else 0
            ## Kurtosis
            variance_clean = xp.var(series_clean)
            diff = series_clean - mean_clean
            mask_pos = diff > 0
            mask_neg = diff < 0
            m4_pos = xp.mean(diff[mask_pos] ** 4) if mask_pos.sum() > 0 else 0
            m4_neg = xp.mean(diff[mask_neg] ** 4) if mask_neg.sum() > 0 else 0
            kurt_pos_val = (m4_pos / (variance_clean ** 2)) - 3 if variance_clean != 0 else 0
            kurt_neg_val = (m4_neg / (variance_clean ** 2)) - 3 if variance_clean != 0 else 0

            # Calcular las estadísticas de forma individual para la columna 'c'
            col_stats={
                "mean": mean_clean,
                "std_dev": std_dev_clean,
                "variance": variance_clean,
                "skewness": skewness_val,
                "kurtosis_pos": kurt_pos_val,
                "kurtosis_neg": kurt_neg_val,
                "min": xp.min(series_clean),
                "max": xp.max(series_clean),
                "min_raw": xp.min(series_raw),
                "max_raw": xp.max(series_raw),
                "negatives": (series_raw < 0).sum(),
                "semidef_positives": (series_raw >= 0).sum()
            }
            # Guardar en el diccionario usando el escalar extraído limpiamente
            self.stats_d[p][n][c]={
                key: col_stats[key].item()
                  for key in col_stats.keys()
            }
    ###########################################################


    ###########################################################
    # Función para obtener las estadísticas de vacío
    def get_vacua_stats(self, parent, model, file=None):
        self.data_d[parent][model]["taquiónico"]=\
            self.data_d[parent][model]["taquiónico"].astype('int')

        ## Bulk operations on datafrme usando xupy xp
        self.stats_d[parent][model]["total_solutions"] = \
            self.data_d[parent][model].shape[0]

        # Evalúa cuántos son de Sitter
        self.stats_d[parent][model]["dS"] = \
            (self.data_d[parent][model]["V"]>0).sum().item()

        # Evalúa cuántos son Anti de Sitter
        self.stats_d[parent][model]["AdS"] = \
            (self.data_d[parent][model]["V"]<0).sum().item()

        #Evalúa cuántos son taquiónicos
        self.stats_d[parent][model]["tachyonic"] = \
            (self.data_d[parent][model]["taquiónico"]==1)\
                .sum().item()

        #Evalúa cuántos son estables
        self.stats_d[parent][model]["stable"] = \
            (self.data_d[parent][model]["taquiónico"]==0)\
                .sum().item()

        # Evalúa cuántos son de Sitter estables
        self.stats_d[parent][model]["dS_stable"] = \
            ((self.data_d[parent][model]["V"]>0) & \
             (self.data_d[parent][model]["taquiónico"]==0))\
                .sum().item()

        # Evalúa cuántos son Anti de Sitter estables
        self.stats_d[parent][model]["AdS_stable"] = \
            ((self.data_d[parent][model]["V"]<0) & \
             (self.data_d[parent][model]["taquiónico"]==0))\
                .sum().item()

        # Evalúa dS/total encontrados
        self.stats_d[parent][model]["dS_ratio"] = \
            self.stats_d[parent][model]["dS"] / \
            self.stats_d[parent][model]["total_solutions"]

        # Evalúa AdS/total encontrados
        self.stats_d[parent][model]["AdS_ratio"] = \
            self.stats_d[parent][model]["AdS"] / \
            self.stats_d[parent][model]["total_solutions"]

        # Evalúa total estables/total encontrados
        self.stats_d[parent][model]["stable_ratio"] = \
            self.stats_d[parent][model]["stable"] / \
            self.stats_d[parent][model]["total_solutions"]

        # Evalúa AdS estables/total AdS
        self.stats_d[parent][model]["AdS_stable_ratio"] = \
            self.stats_d[parent][model]["AdS_stable"] / \
            self.stats_d[parent][model]["AdS"]

        # Evalúa  dS estables/total dS
        self.stats_d[parent][model]["dS_stable_ratio"] = \
            self.stats_d[parent][model]["dS_stable"] / \
            self.stats_d[parent][model]["dS"]
    ###########################################################


    ###########################################################
    # Función para obtener las estadísticas de vacío
    # def export_to(self, name : str, format : str="json"):
    #    for d in DirHandle.
    def export_to(self, name : str="stats", format : str="json"):
        if format.lower() != "json":
            raise NotImplementedError(f"El formato '{format}' no está soportado.")

        import json
        # Asegurar extensión .json en el nombre
        filename = name if name.endswith(".json") else f"{name}.json"

        # d.list() devuelve las rutas base de los directorios procesados (ej: 'lvdsl_outputs/BENCHMARK_01/OFICIAL/')
        for parent_path in self.dir_handle.list():
            if parent_path in self.stats_d:
                # Construir la ruta completa combinando el directorio base y el nombre de archivo
                full_path = os.path.join(parent_path, filename)

                # Exportar solo las estadísticas pertenecientes a esta ruta raíz
                if not dryRun:
                    with open(full_path, "w", encoding="utf-8") as f:
                        json.dump(self.stats_d[parent_path], f, indent=4, ensure_ascii=False)
                else:
                    print("Dry Run")

                print(f"Estadísticas exportadas a: {full_path}")
    ###########################################################


    ###########################################################
    # Graficación de las distribuciones por modelo
    def plot_by_model(self, export:bool=False, name:str="plot_for_"):

        # Validar que los datos existan en memoria
        if not hasattr(self, 'data_d') or not self.data_d:
            print("No hay datos cargados. Ejecuta primero get_data().")
            return

        # Iterar sobre las rutas raíz (parents)
        for parent_path in self.data_d.keys():
            # Iterar sobre cada modelo indexado en esa ruta
            for model, df_model in self.data_d[parent_path].items():

                # Iterar dinámicamente sobre la lista de columnas configuradas en la clase
                for col in self.columns:

                    # Comprobar que la columna exista en el DataFrame actual
                    if col in df_model.columns:
                        # Configurar un lienzo individual para esta combinación Modelo-Columna
                        fig, ax = plt.subplots(figsize=(8, 5))

                        # Graficar el violín de forma agnóstica usando el nombre de la columna
                        sns.violinplot(
                            data=df_model, y=col, ax=ax,
                            color="skyblue", inner="quartile", cut=0
                        )

                        # Configuración estética utilizando estrictamente la nomenclatura del dataset
                        ax.set_title(f"{col} - {model}", fontsize=12, fontweight='bold')
                        ax.set_ylabel(col)
                        ax.set_xlabel(model)

                        plt.tight_layout()

                        # Guardado o muestra respetando el nombre de la variable analizada
                        if export:
                            out_name = f"{name}{model}_{col}.png"
                            full_path = os.path.join(parent_path, out_name)
                            plt.savefig(full_path, dpi=300, bbox_inches='tight')
                            print(f"📉 Gráfico exportado: {full_path}")
                        else:
                            plt.show()

                        plt.close()
    ###########################################################

    ###########################################################
    # Graficación comparativa selectiva entre modelos (Fight)
    def plot_compare_model(self, fight:dict={}, export:bool=False, name:str="plot_for_", horizontal=False, outlier_handle:dict={}):
        # Validar que los datos existan en memoria
        if not hasattr(self, 'data_d') or not self.data_d:
            print("⚠️ No hay datos cargados. Ejecuta primero get_data().")
            return

        # Iterar sobre las rutas raíz (parents)
        for parent_path in self.data_d.keys():

            # Si el diccionario está vacío, genera dinámicamente un grupo con todos los modelos del directorio
            fight_working = fight if fight else { "∀m": list(self.data_d[parent_path].keys()) }

            # Un plot por cada grupo comparativo (fight_key)
            for fight_key, models_list in fight_working.items():

                # Cada variable de self.columns genera un archivo e imagen independiente
                for col in self.columns:
                    data_fight = []

                    # Recolectar datos de los modelos solicitados para esta batalla
                    for model in models_list:
                        if model in self.data_d[parent_path]:
                            df_model = self.data_d[parent_path][model]

                            if col in df_model.columns:
                                df_tmp = df_model[[col]].copy()
                                df_tmp["Modelo"] = model  # Etiqueta para el eje X
                                data_fight.append(df_tmp)

                    if not data_fight:
                        print(f"Sin datos para la comparativa '{fight_key}' usando '{col}' en {parent_path}")
                        continue

                    # Consolidar datos para el plot
                    df_total = pandas.concat(data_fight, ignore_index=True)
                    order = humansorted(df_total["Modelo"].unique())

                    # Configurar lienzo vanilla para este "fight" específico y su variable
                    fig, ax = plt.subplots(figsize=(10, 6))

                    # Mapear x como la variable categórica (Modelo) e y como el valor continuo (col)
                    x_var, y_var = (col, "Modelo") if horizontal else ("Modelo", col)

                    # Graficar el violín estilizado
                    sns.violinplot(
                        data=df_total, x=x_var, y=y_var, ax=ax, order=order,
                        palette="viridis",      # Una paleta secuencial/perceptual más sobria y elegante
                        inner="quartile",
                        cut=0,
                        linewidth=1.0,          # Contorno más delgado para evitar saturación
                        alpha=0.85              # Ligera transparencia para suavizar el lienzo
                    )

                    # Remover las líneas de los ejes sobrantes (Spines)
                    sns.despine(ax=ax, left=True, bottom=False)

                    # Asegurar que el fondo del subplot no dibuje rejillas negras pesadas
                    ax.grid(True, axis='x', linestyle='--', alpha=0.5, color='gray') # Rejilla vertical sutil para la métrica
                    ax.grid(False, axis='y') # Apagar por completo las líneas horizontales divisoria

                    # ---------------------------------------------------------
                    # Artificio Visual Agnóstico: Límites del eje basados en la serie limpia
                    config = outlier_handle.get(col, {})
                    method_name = config.get("method", "none")
                    params = config.get("params", {})

                    if method_name in self.outlier_methods:
                        series_clean = self.outlier_methods[method_name](df_total[col], **params)

                        if not series_clean.empty:
                            lim_inf, lim_sup = series_clean.min(), series_clean.max()

                            # Holgura sutil del 3% para evitar colisiones estéticas con los bordes
                            rango = lim_sup - lim_inf
                            lim_inf -= 0.03 * rango if rango != 0 else 1
                            lim_sup += 0.03 * rango if rango != 0 else 1

                            if horizontal:
                                ax.set_xlim(lim_inf, lim_sup)
                            else:
                                ax.set_ylim(lim_inf, lim_sup)
                    # ---------------------------------------------------------

                    # Título descriptivo usando la clave del grupo (fight_key) y el parámetro analizado
                    ax.set_title(f"{fight_key} : {col}", fontsize=12, fontweight='bold')
                    ax.set_ylabel(y_var)
                    ax.set_xlabel(x_var)
                    if not horizontal:
                        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

                    plt.tight_layout()

                    # Guardar o mostrar respetando tu estructura de salida dinámica
                    if export:
                        if not dryRun:
                            out_name = f"{name}{fight_key}_{col}.png"
                            full_path = os.path.join(parent_path, out_name)
                            plt.savefig(full_path, dpi=300, bbox_inches='tight')
                        print(f"Gráfico comparativo exportado: {full_path}")
                    else:
                        if not dryRun:
                            plt.show()
                        else:
                            print("Created plot")

                    plt.close()
    ###########################################################


    ###########################################################
    # Opción Global, Para que nada se exporte si no es deseable
    def set_dry_run(self, dryRun:bool=True):
        self.dryRun=dryRun
    ###########################################################


    ###########################################################
    ## Manejo de outliers
    def _filter_iqr(self, series, factor=1.5, **kwargs):
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        mask = (series >= q1 - factor * iqr) & (series <= q3 + factor * iqr)
        return series[mask]
    def _filter_percentile(self, series, lower=0.005, upper=0.995, **kwargs):
        lim_inf = series.quantile(lower)
        lim_sup = series.quantile(upper)
        mask = (series >= lim_inf) & (series <= lim_sup)
        return series[mask]
    ###########################################################


###############################################################


if __name__ == "__main__":
    import sys
    from pprint import pprint
    #dryRun=True
    dir = sys.argv[1:]
    d=DirHandle(dir)
    stat=StatAnalysis(d)
    s=stat.get_data()
    stat.columns_to_analyze("A3N3",True)
    for p in d.list():
        for n in d.list(p=p):
            print(f"Procesando {p}{n}")
            print(s[p][n])

    print("Estadísticas:")
    stat.get_stats()
    pprint(stat.stats_d)
    stat.export_to()
    #stat.plot_by_model()
    stat.plot_compare_model(horizontal=True)

