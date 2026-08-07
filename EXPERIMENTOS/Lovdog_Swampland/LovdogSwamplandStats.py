from    lvdsl.data.stats.dir_handle import DirHandle
from    lvdsl.data.stats.get_stats  import StatAnalysis
from    pprint                      import pprint
from    itertools                   import combinations
import  pandas                                          as pd
import  sys
import  os

# Recibir directorios por argumento de terminal
dir_args = sys.argv[1:]

if not dir_args:
    print("Error: Debes proporcionar al menos un directorio de datos.")
    sys.exit(1)

d = DirHandle(dir_args)
stat = StatAnalysis(d)
s = stat.get_data()

# Configurar columnas a analizar
stat.columns_to_analyze(["V", "fitness", "A3N3"])

# Configuración de filtros topológicos discutidos y validados
filtros_topologia = {
    "V": {"method": "iqr", "params": {"factor": 2.5}},
    "A3N3": {"method": "none"},
    "fitness": {"method": "percentile", "params": {"lower": 0.0, "upper": 0.99}}
}

# Calcular estadísticas y exportar
stat.get_stats(outlier_handle=filtros_topologia)
pprint(stat.stats_d)
stat.export_to()

# Generar los gráficos de violín optimizados ópticamente
stat.plot_compare_model(export=True, horizontal=True, outlier_handle=filtros_topologia)







# ==============================================================================
# SELECCIÓN AUTOMATIZADA DEL MEJOR MODELO (CRITERIO DE RIGOR CIENTÍFICO)
# ==============================================================================
print("\n" + "="*60)
print("ALGORITHMIC BENCHMARK SELECTION REPORT")
print("="*60)





# ==============================================================================
# ENTORNO DE EVALUACIÓN MULTI-CRITERIO (MÉTODO DE BORDA SEPARADO)
# ==============================================================================

def calcular_ranking_swampland(stat_analysis_obj, parent_directory, modelos_validos):
    """
    Función aislada para procesar los momentos estadísticos de un directorio específico
    y resolver los 'Best of' parciales y el 'Final Best' conjunto.
    """
    # Verificar que el directorio exista en el diccionario de estadísticas
    if parent_directory not in stat_analysis_obj.stats_d:
        print(f"⚠️ [Advertencia] {parent_directory} no se encuentra en el volcado estadístico.")
        return

    sub_dict = stat_analysis_obj.stats_d[parent_directory]

    # Asegurar la intersección real de modelos que sí tienen datos calculados
    modelos_locales = [m for m in modelos_validos if m in sub_dict]

    if not modelos_locales:
        print(f"⚠️ No se encontraron estadísticas calculadas para los modelos en {parent_directory}")
        return

    print("\n" + "="*65)
    print(f"📊 EVALUACIÓN DE COMPETITIVIDAD EN: {parent_directory}")
    print("="*65)

    criterios_raw = {
        "s1_V_mean": [],
        "s2_V_skew": [],
        "s3_V_kurt_pos": [],
        "s4_V_kurt_neg": [],
        "s5_V_stable_ratio": [],
        "s6_V_dS_stable_ratio": [],
        "s7_fitness_mean": []
    }

    # Extracción limpia utilizando la estructura anidada exacta del pipeline
    # Extracción limpia utilizando la estructura anidada exacta del pipeline
    for m in modelos_locales:
        v_stats = sub_dict[m]["V"]
        v_stats["dS_stable_ratio"] = sub_dict[m]["dS_stable_ratio"]
        v_stats["stable_ratio"] = sub_dict[m]["stable_ratio"]
        fit_stats = sub_dict[m]["fitness"]

        # Corrección del KeyError: Promediar perfiles de curtosis o elegir uno
        criterios_raw["s1_V_mean"             ].append(abs(v_stats["mean"])      )    # s1: Minimizar proximidad a 0
        criterios_raw["s2_V_skew"             ].append(v_stats["skewness"]       )    # s2: Minimizar (sesgo derecho/negativo)
        criterios_raw["s3_V_kurt_pos"         ].append(v_stats["kurtosis_pos"]   )    # s3: Antes v_stats["kurtosis"]
        criterios_raw["s4_V_kurt_neg"         ].append(v_stats["kurtosis_neg"]   )    # s4: Antes v_stats["kurtosis"]
        criterios_raw["s5_V_stable_ratio"     ].append(v_stats["stable_ratio"]   )    # s5: Maximizar radio de soluciones estables
        criterios_raw["s6_V_dS_stable_ratio"  ].append(v_stats["dS_stable_ratio"])    # s6: Maximizar radio de dS estables
        criterios_raw["s7_fitness_mean"       ].append(fit_stats["mean"]         )    # s7: Minimizar fitness, mayor convergencia

    # Construir el DataFrame de Rangos
    df_ranks = pd.DataFrame(index=modelos_locales)
    df_ranks["rank_s1"] = pd.Series(criterios_raw["s1_V_mean"]            ,  index=modelos_locales).rank(ascending=True , method='min')
    df_ranks["rank_s2"] = pd.Series(criterios_raw["s2_V_skew"]            ,  index=modelos_locales).rank(ascending=True , method='min')
    df_ranks["rank_s3"] = pd.Series(criterios_raw["s3_V_kurt_pos"]        ,  index=modelos_locales).rank(ascending=True , method='min')
    df_ranks["rank_s4"] = pd.Series(criterios_raw["s4_V_kurt_neg"]        ,  index=modelos_locales).rank(ascending=True , method='min')
    df_ranks["rank_s5"] = pd.Series(criterios_raw["s5_V_stable_ratio"]    ,  index=modelos_locales).rank(ascending=False, method='max')
    df_ranks["rank_s6"] = pd.Series(criterios_raw["s6_V_dS_stable_ratio"] ,  index=modelos_locales).rank(ascending=True , method='min')
    df_ranks["rank_s7"] = pd.Series(criterios_raw["s7_fitness_mean"]      ,  index=modelos_locales).rank(ascending=True , method='min')

    # --- SECCIÓN 1: LOS "BEST OF" POR CRITERIO ---
    print("\n🥇 GANADORES INDIVIDUALES POR CRITERIO FISICOMATEMÁTICO:")
    print(f" └── [Best of s1]  (Min |V_mean|       ):  {df_ranks['rank_s1'].idxmin()}")
    print(f" └── [Best of s2]  (Min V_Skewness     ):  {df_ranks['rank_s2'].idxmin()}")
    print(f" └── [Best of s3]  (Min V_Kurtosis pos ):  {df_ranks['rank_s3'].idxmin()}")
    print(f" └── [Best of s4]  (Min V_Kurtosis neg ):  {df_ranks['rank_s4'].idxmin()}")
    print(f" └── [Best of s5]  (Max Stable Ratio   ):  {df_ranks['rank_s5'].idxmin()}")
    print(f" └── [Best of s6]  (Max Stable dS Ratio):  {df_ranks['rank_s6'].idxmin()}")
    print(f" └── [Best of s7]  (Min fitness mean   ):  {df_ranks['rank_s7'].idxmin()}")

    # --- SECCIÓN 2: EL "FINAL BEST" CONJUNTO AUTOMATIZADO (s1 a s7) ---
    print("\n🥇 GANADORES PAIR COMBINATORIAL POR CRITERIO FISICOMATEMÁTICO:")

    # Generates all pairs from (1,2) up to (6,7)
    for i, j in combinations(range(1, 8), 2):
        col_name = f"rank_s{i}_s{j}"

        # Calculate sum on the fly if not already saved in the DataFrame
        df_ranks[col_name] = df_ranks[[f"rank_s{i}", f"rank_s{j}"]].sum(axis=1)

        # Print results neatly
        print(f" └── [Best of s{i}, s{j}]:  {df_ranks[col_name].idxmin()}")

    df_ranks["Consensus_Score"] = df_ranks[["rank_s1", "rank_s2", "rank_s3", "rank_s4"]].sum(axis=1)
    df_ranks = df_ranks.sort_values(by="Consensus_Score", ascending=True)

    final_best = df_ranks.index[0]

    #print("\n📋 RANKING DE CONSENSO GENERAL (Suma de Rangos de Borda):")
    #for pos, (modelo, row) in enumerate(df_ranks.iterrows(), 1):
    #    print(f"  {pos:02d}. {modelo:<25} -> Score: {row['Consensus_Score']:>4.1f} "
    #          f"(s1:{int(row['rank_s1'])} | s2:{int(row['rank_s2'])} | s3:{int(row['rank_s3'])} | s4:{int(row['rank_s4'])})")

    print("\n" + "*"*65)
    print(f"🏆 FINAL BEST (Ganador definitivo por Criterio Conjunto): {final_best}")
    print("*"*65 + "\n")


# ==============================================================================
# BUCLE PRINCIPAL DE EXPORTACIÓN Y DISPARO DEL PIPELINE DE RANKING
# ==============================================================================
# Corrección de API: Invocar al método real de dir_handle para obtener el DataFrame
df_global_configs = d.models_to_dataframe()

if df_global_configs is not None and not df_global_configs.empty:
    unique_parent_dirs = df_global_configs["ParentDir"].unique()
    print(f"\n[Estructuración] Detectados {len(unique_parent_dirs)} directorios padres únicos.")

    for current_parent in unique_parent_dirs:
        # 1. Filtrar y limpiar para el reporte CSV/LaTeX
        df_filtered = df_global_configs[df_global_configs["ParentDir"] == current_parent].copy()
        df_filtered = df_filtered.drop(columns=["ParentDir"])

        target_path = os.path.join(current_parent, "configurations_report.csv")
        df_filtered.to_csv(target_path, index=False, encoding='utf-8')
        print(f" └── ✅ Reporte provisional guardado en: {target_path} ({len(df_filtered)} modelos)")

        # 2. Control estricto por argumento
        if dir_args and current_parent == dir_args[0]:
            print("\n" + "="*60)
            print(f"CÓDIGO LATEX LOCAL PARA: {current_parent}")
            print("="*60)
            print(df_filtered.to_latex(index=False,
                                      caption=f"Symmetric hyperparameter specifications for the metaheuristics evaluated in {current_parent}.",
                                      label="tab:hyperparams"))
            print("="*60)

            # 3. LLAMADA AL RANKING: Corrección de 'ModelName' a 'Name'
            if 'Name' in df_filtered.columns:
                modelos_reporte = df_filtered['Name'].unique()
            else:
                modelos_reporte = df_filtered.index.unique()

            # Disparar la función de consenso matemático
            calcular_ranking_swampland(stat, current_parent, modelos_reporte)
else:
    print("\n⚠️ Advertencia: No se encontraron configuraciones globales válidas para procesar rankings.")

