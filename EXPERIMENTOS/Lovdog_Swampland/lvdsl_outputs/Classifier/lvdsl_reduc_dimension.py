import numpy as np
import pandas as pd
import os
from typing import List, Union, Optional
import sys
import psutil
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA, SparsePCA, TruncatedSVD
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.manifold import Isomap, LocallyLinearEmbedding as LLE
from sklearn.neighbors import NeighborhoodComponentsAnalysis as NCA
from sklearn.model_selection import train_test_split
import time
import matplotlib.pyplot as plt
from datetime import datetime
from lvdsl_reduc_dimension_resume import generate_experiment_html


def load_and_audit_datasets(
    file_list_path: str, verbose: bool = True
) -> pd.DataFrame:
    """Lee las rutas del txt, detecta/reporta archivos con NaN/INF y devuelve

    el DataFrame consolidado y limpio de nulos.
    """
    if not os.path.exists(file_list_path):
        raise FileNotFoundError(f"Archivo no encontrado: {file_list_path}")

    with open(file_list_path, "r", encoding="utf-8") as f:
        filepaths = [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#")
        ]

    df_list = []
    files_with_errors = {}

    for path in filepaths:
        if not os.path.exists(path):
            continue

        # Primer columna y filas son indices y cabeceras
        df_temp = pd.read_csv(path, index_col=0, header=0)

        # Convertir inf/ -inf a NaN para conteo unificado
        df_clean_check = df_temp.replace([np.inf, -np.inf], np.nan)
        bad_rows = df_clean_check.isna().any(axis=1).sum()

        if bad_rows > 0:
            files_with_errors[path] = bad_rows
            # Descartar filas con NaN/INF en el DataFrame temporal
            df_temp = df_clean_check.dropna()

        df_list.append(df_temp)

    # Reportar archivos 'delatados'
    if files_with_errors and verbose:
        print(
            f"\n[ALERTA] Se encontraron {len(files_with_errors)} archivos con datos corruptos (NaN/INF):"
        )
        for file, count in files_with_errors.items():
            print(f"  └─ {file}: {count} filas descartadas")

    df_raw = pd.concat(df_list, ignore_index=True)

    if verbose:
        print(f"\n[INFO] Dataset cargado y saneado. Forma final: {df_raw.shape}")

    return df_raw

def load_datasets(
    file_list_path: str,
    verbose: bool = True
) -> pd.DataFrame:
    """
    Lee las rutas indicadas en el archivo txt de salidas, carga los CSVs
    y los concatena en un solo DataFrame unificado.
    """
    if not os.path.exists(file_list_path):
        raise FileNotFoundError(f"El archivo de lista no existe: {file_list_path}")

    # 1. Extraer rutas válidas (ignorando líneas vacías y comentarios)
    with open(file_list_path, 'r', encoding='utf-8') as f:
        filepaths = [
            line.strip() for line in f
            if line.strip() and not line.startswith('#')
        ]

    if not filepaths:
        raise ValueError("El archivo de entradas no contiene rutas válidas.")

    if verbose:
        print(f"[INFO] Cargando {len(filepaths)} archivos desde {file_list_path}...")

    # 2. Cargar y concatenar DataFrames
    df_list: List[pd.DataFrame] = []
    contador_datasets = 0
    for path in filepaths:
        if os.path.exists(path):
            # First column is index
            # First row is column names
            df_temp = pd.read_csv(path, index_col=0, header=0)
            if psutil.virtual_memory().percent >= 96.0:
                raise MemoryError("Límite de RAM (96%) alcanzado. Carga interrumpida.")
            df_list.append(df_temp)
            contador_datasets += 1
        else:
            if verbose:
                print(f"[WARNING] Omitiendo archivo no encontrado: {path}")

    if not df_list:
        raise RuntimeError("No se pudo cargar ningún dataset válido de la lista.")

    df_raw = pd.concat(df_list, ignore_index=True)

    if verbose:
        print(f"[INFO] Dataset unificado cargado con éxito. Forma total: {df_raw.shape}")
        print(f"[INFO] Contador de datasets cargados: {contador_datasets}")
        print(f"[INFO] Cabecera del dataset:\n{df_raw.head()}")

    return df_raw

def create_physics_target(df: pd.DataFrame) -> pd.DataFrame:
    """Crea la columna 'target' con las 4 clases físicas a partir de 'type' y 'taquiónico'."""
    # Asegurar tipo booleano explícito en taquiónico
    taquionico = df["taquiónico"].astype(bool)
    is_ds = df["type"] == 1

    # Definir condiciones
    conditions = [
        (~is_ds) & (~taquionico),  # AdS Stable (0)
        (~is_ds) & (taquionico),  # AdS Unstable (1)
        (is_ds) & (~taquionico),  # dS Stable (2)
        (is_ds) & (taquionico),  # dS Unstable (3)
    ]

    choices = [0, 1, 2, 3]

    df["target"] = np.select(conditions, choices, default=-1)
    print(df.head())
    return df

def balance_df_by_min(
    df: pd.DataFrame, label_col: str = "target", random_state: int = 42
) -> pd.DataFrame:
    """Aplica trimming al número mínimo de muestras por clase."""
    class_counts = df[label_col].value_counts()
    min_samples = class_counts.min()

    print("--- Distribución original ---")
    print(class_counts)
    print(f"\n[INFO] Recortando a {min_samples} muestras por clase...")

    # Submuestreo directo preservando todas las columnas:
    balanced_df = (
        df.groupby(label_col, group_keys=True)
        .sample(n=min_samples, random_state=random_state)
        .reset_index(drop=True)
    )

    print("\n--- Distribución balanceada ---")
    print(balanced_df[label_col].value_counts())

    return balanced_df

def run_dimensionality_reduction_grid(
    X_scaled, y, n_samples_subset: int = 8000, random_state: int = 42
):
    """
    Ejecuta una rejilla de reducción de dimensionalidad (supervisada y no supervisada)
    para 2D y 3D, aplicando un submuestreo estratificado para los métodos de alta
    complejidad computacional.
    """
    # Muestreo estratificado para métodos O(N^2) / O(N^3)
    if len(X_scaled) > n_samples_subset:
        X_sub, _, y_sub, _ = train_test_split(
            X_scaled,
            y,
            train_size=n_samples_subset,
            stratify=y,
            random_state=random_state,
        )
    else:
        X_sub, y_sub = X_scaled, y

    reduced_results = {}

    for n_comp in [2, 3]:
        print(f"\n==========================================")
        print(f"[REJILLA] Evaluando reducciones a {n_comp}D...")
        print(f"==========================================")

        methods = {
            # Superficie Supervisada (usan X y y)
            "LDA": (LDA(n_components=n_comp), X_scaled, y, True),
            "NCA": (
                NCA(n_components=n_comp, random_state=random_state),
                X_sub,
                y_sub,
                True,
            ),
            # Superficie No Supervisada (usan solo X)
            "PCA": (PCA(n_components=n_comp), X_scaled, None, False),
            "SparsePCA": (
                SparsePCA(
                    n_components=n_comp, random_state=random_state, n_jobs=-1
                ),
                X_sub,
                None,
                False,
            ),
            "TruncatedSVD": (
                TruncatedSVD(n_components=n_comp, random_state=random_state),
                X_scaled,
                None,
                False,
            ),
            "Isomap": (
                Isomap(n_components=n_comp, n_neighbors=15, n_jobs=-1),
                X_sub,
                None,
                False,
            ),
            "LLE_standard": (
                LLE(
                    n_components=n_comp,
                    n_neighbors=15,
                    method="standard",
                    n_jobs=-1,
                ),
                X_sub,
                None,
                False,
            ),
        }

        for name, (model, X_target, y_target, is_supervised) in methods.items():
            key = f"{name}_{n_comp}D"
            print(
                f"  └─ Ejecutando {key} sobre {len(X_target)} muestras...",
                end=" ",
            )

            t_start = time.time()

            if is_supervised:
                X_red = model.fit_transform(X_target, y_target)
            else:
                X_red = model.fit_transform(X_target)

            t_elapsed = time.time() - t_start
            print(f"[OK] ({t_elapsed:.2f}s)")

            reduced_results[key] = {
                "X_red": X_red,
                "y": y_target,
                "model": model,
                "n_components": n_comp,
                "is_supervised": is_supervised,
            }

    return reduced_results


import os
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def export_reduction_experiment(
    reduced_results,
    feature_names=None,
    base_dir="lvdsl_classify_dim_reduction",
    file_format="csv" # 'csv' o 'parquet'
):
    """
    Exporta la bitácora técnica, los gráficos individuales y guarda las matrices
    transformadas (datasets finales) en un directorio dedicado con sufijo .ds.
    """
    today_str = datetime.now().strftime("%Y_%m_%d")

    # Nomenclatura uniforme para ambos directorios
    folder_base_name = f"lvdsl_reduc_dim_{today_str}"
    img_dir_path = os.path.join(base_dir, f"{folder_base_name}.img")
    ds_dir_path = os.path.join(base_dir, f"{folder_base_name}.ds")

    os.makedirs(img_dir_path, exist_ok=True)
    os.makedirs(ds_dir_path, exist_ok=True)

    txt_file_path = os.path.join(base_dir, "lvdsl_reduc_dim.txt")

    # 1. Exportación de Datasets finales (.ds)
    dataset_files_created = []

    for key, data in reduced_results.items():
        X_red = data["X_red"]
        y_target = data["y"]
        n_comp = data["n_components"]

        # Crear nombres de columnas para el espacio reducido
        col_names = [f"comp_{i+1}" for i in range(n_comp)]
        df_export = pd.DataFrame(X_red, columns=col_names)

        # Incluir la variable objetivo si existe
        if y_target is not None:
            df_export["target"] = np.array(y_target).ravel()

        # Nombre del archivo individual por modelo
        file_name = f"dataset_{key}.{file_format}"
        file_path = os.path.join(ds_dir_path, file_name)

        if file_format == "parquet":
            df_export.to_parquet(file_path, index=False)
        else:
            df_export.to_csv(file_path, index=False)

        dataset_files_created.append((key, file_name, df_export.shape))

    # 2. Generación del reporte técnico (.txt)
    with open(txt_file_path, "w", encoding="utf-8") as f:
        f.write("=========================================================\n")
        f.write("   LVDSL - BITÁCORA DE SELECCIÓN Y DATASETS PROCESADOS   \n")
        f.write(f"   FECHA DE EJECUCIÓN: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=========================================================\n\n")

        f.write(">>> DIRECTORIOS DE SALIDA GENERADOS <<<\n")
        f.write(f"  • Imágenes (.png):  {img_dir_path}\n")
        f.write(f"  • Datasets (.ds):   {ds_dir_path}\n\n")

        f.write(">>> RESUMEN DE DATASETS FINALES ALMACENADOS <<<\n")
        for key, f_name, shape in dataset_files_created:
            f.write(f"  • [{key}] -> {f_name} | Dimensiones: {shape}\n")

        f.write("\n" + "=" * 57 + "\n\n")

        f.write(">>> APORTE DE CARACTERÍSTICAS ORIGINALES Y PESOS <<<\n\n")
        for key, data in reduced_results.items():
            model = data["model"]
            X_red = data["X_red"]
            n_comp = data["n_components"]

            f.write(f"--- MODELO: {key} ---\n")
            f.write(f"Matriz de salida: {X_red.shape}\n")

            if hasattr(model, "explained_variance_ratio_"):
                var_exp = model.explained_variance_ratio_
                f.write(f"Varianza explicada acumulada: {sum(var_exp):.4f} {var_exp.round(4).tolist()}\n")

            components = None
            if hasattr(model, "components_"):
                components = model.components_
            elif hasattr(model, "scalings_"):
                components = model.scalings_.T

            if components is not None and feature_names is not None:
                f.write("Top 3 Características con mayor peso absoluto por Componente:\n")
                for i in range(min(n_comp, components.shape[0])):
                    comp_weights = components[i]
                    top_indices = np.argsort(np.abs(comp_weights))[::-1][:3]

                    top_features_str = ", ".join(
                        [f"{feature_names[idx]} (|w|={abs(comp_weights[idx]):.3f})" for idx in top_indices]
                    )
                    f.write(f"   • Comp {i+1}: {top_features_str}\n")
            elif components is None:
                f.write("Pesos por Feature: Transformación no lineal (Sin componentes explícitos).\n")

            f.write("\n" + "-" * 40 + "\n\n")

    print(f"[OK] Bitácora técnica actualizada en: {txt_file_path}")
    print(f"[OK] {len(dataset_files_created)} datasets guardados en: {ds_dir_path}")

    # 3. Generación de gráficos (.png) en directorio .img
    for key, data in reduced_results.items():
        X_red = data["X_red"]
        y_target = data["y"]
        n_comp = data["n_components"]

        fig = plt.figure(figsize=(8, 6), dpi=300)

        if y_target is not None:
            c_vals = y_target
            n_classes = len(np.unique(y_target))
        else:
            c_vals = "tab:blue"
            n_classes = 1

        cmap = plt.colormaps.get_cmap("tab10").resampled(max(n_classes, 1))

        if n_comp == 2:
            ax = fig.add_subplot(111)
            scatter = ax.scatter(
                X_red[:, 0],
                X_red[:, 1],
                c=c_vals,
                cmap=cmap if y_target is not None else None,
                alpha=0.6,
                s=12,
                edgecolors="none",
            )
            ax.set_xlabel("Componente 1")
            ax.set_ylabel("Componente 2")

        elif n_comp == 3:
            ax = fig.add_subplot(111, projection="3d")
            scatter = ax.scatter(
                X_red[:, 0],
                X_red[:, 1],
                X_red[:, 2],
                c=c_vals,
                cmap=cmap if y_target is not None else None,
                alpha=0.6,
                s=10,
                edgecolors="none",
            )
            ax.set_xlabel("Comp 1")
            ax.set_ylabel("Comp 2")
            ax.set_zlabel("Comp 3")

        ax.set_title(f"Proyección {key} (N={len(X_red)})", fontsize=12)

        if y_target is not None:
            cbar = plt.colorbar(scatter, ax=ax, pad=0.1)
            cbar.set_label("Clase de Vacío")

        plt.tight_layout()

        plot_path = os.path.join(img_dir_path, f"plot_{key}.png")
        plt.savefig(plot_path)
        plt.close(fig)

    print(f"[OK] {len(reduced_results)} gráficos guardados en: {img_dir_path}")








# --- Ejemplo de uso e integración ---
if __name__ == "__main__":
    df_raw = load_datasets("lvdsl_dataset_unifier_outputs.txt")
    print(f"[AUDITORÍA] Filas con NaN o INF: {df_raw.replace([np.inf, -np.inf], np.nan).isna().any(axis=1).sum()} de {len(df_raw)}")
    print(df_raw.replace([np.inf, -np.inf], np.nan).isna().sum())
    # Filtrar las filas que contienen NaN o Inf
    mask_nan_inf = df_raw.replace([np.inf, -np.inf], np.nan).isna().any(axis=1)
    # Imprimir las columnas críticas de esas filas
    cols_interes = ["s", "tau", "A3N3", "AD5", "lambda1", "lambda2", "taquiónico"]
    print(df_raw.loc[mask_nan_inf, cols_interes].head(10))
    # Retirar todos los elementos inválidos
    df_raw = df_raw[~mask_nan_inf]
    print(f"[AUDITORÍA] Filas con NaN o INF: {df_raw.replace([np.inf, -np.inf], np.nan).isna().any(axis=1).sum()} de {len(df_raw)}")
    print(df_raw.replace([np.inf, -np.inf], np.nan).isna().sum())


   # df_raw = load_and_audit_datasets("lvdsl_dataset_unifier_outputs.txt")
    df_tagged = create_physics_target(df_raw)
    df_balanced = balance_df_by_min(df_tagged, label_col="target")

    non_feature_cols = ["target", "type", "taquiónico", "V", "lambda1", "lambda2", "fitness"]
    print("Extrayendo datos...")
    X = df_balanced.drop(columns=[c for c in non_feature_cols if c in df_balanced.columns]).values
    y = df_balanced['target'].values.astype('int')
    print(X.shape)
    print(y.shape)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    print(f"[OK] Matriz X escalada: {X_scaled.shape}")
    print(f"[INFO] Medias aproximadas: {np.mean(X_scaled, axis=0).round(2)}")
    print(f"[INFO] Desviaciones estándar: {np.std(X_scaled, axis=0).round(2)}")


    results = run_dimensionality_reduction_grid(X_scaled, y)

    feature_names = [c for c in df_balanced.columns if c not in non_feature_cols]
    export_reduction_experiment(results, feature_names=feature_names)

    ##generate_experiment_html(
    ##    base_dir="lvdsl_classify_dim_reduction",
    ##    output_html_path="/tmp/lvdsl_reduc_dim.html"
    ##)

    # --- [NUEVO: Construcción de Datasets para Clasificación] ---
    feature_cols = [c for c in df_balanced.columns if c not in non_feature_cols]

    # 1. Dataset Original (Escalado)
    df_orig_scaled = pd.DataFrame(X_scaled, columns=feature_cols)
    df_orig_scaled['target'] = y

    datasets_to_classify = {
        "Original_Scaled": df_orig_scaled
    }

    # 2. Reconstruir DataFrames de las componentes reducidas desde 'results'
    df_orig_raw = pd.DataFrame(X, columns=feature_cols)
    df_orig_raw['target'] = y

    df_orig_scaled = pd.DataFrame(X_scaled, columns=feature_cols)
    df_orig_scaled['target'] = y

    datasets_to_classify = {
        "Original_Raw": df_orig_raw,
        "Original_Scaled": df_orig_scaled
    }
    # 2. Reconstrucción de DataFrames reducidos
    for model_name, res in results.items():
        X_red = res["X_red"]
        y_model = res.get("y", None)

        # Si y_model no viene en el diccionario del resultado, fallback seguro
        if y_model is None:
            y_model = y[: len(X_red)]

        n_components = X_red.shape[1]
        comp_cols = [f"comp_{i+1}" for i in range(n_components)]

        df_red = pd.DataFrame(X_red, columns=comp_cols)
        df_red["target"] = np.array(y_model, dtype=int)
        datasets_to_classify[model_name] = df_red
    #for model_name, res in results.items():
    #    X_red = res["X_red"]
    #    y_model = res["y"]

    #    # Si el modelo devolvió None en 'y', usar el vector 'y' global (ajustado según número de filas de X_red)
    #    if y_model is None:
    #        y_model = y[: len(X_red)]

    #    n_components = X_red.shape[1]
    #    comp_cols = [f"comp_{i+1}" for i in range(n_components)]

    #    df_red = pd.DataFrame(X_red, columns=comp_cols)
    #    df_red["target"] = np.array(y_model, dtype=int)
    #    datasets_to_classify[model_name] = df_red


    # --- [NUEVO: Ejecución del Grid de Clasificación] ---
    from lvdsl_classify import run_classification_grid
    run_classification_grid(
        datasets_dict=datasets_to_classify,
        target_col="target",
        base_dir="lvdsl_classify_grid"
    )

    from lvdsl_classify_resume import generate_classification_html
    # En tu bloque __main__:
    generate_classification_html(
        reduc_dir="lvdsl_classify_dim_reduction",
        classify_dir="lvdsl_classify_grid",
        output_html_path="/tmp/lvdsl_reduc_dim.html",
    )



