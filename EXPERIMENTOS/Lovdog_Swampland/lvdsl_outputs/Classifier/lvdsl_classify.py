"""
LVDSL - Grid de Clasificación y Evaluación
Módulo de clasificación multimodelo para espacios de datos originales y reducidos.
"""

import os
import sys
import joblib
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Modelos de Clasificación
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier

# Métricas y Evaluación
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay,
    accuracy_score,
    precision_recall_fscore_support,
    roc_auc_score
)

# Configuración global de gráficos
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'font.sans-serif': 'DejaVu Sans',
    'axes.edgecolor': '#cccccc',
    'axes.linewidth': 0.8
})

def setup_output_directories(base_dir="lvdsl_classify_grid"):
    """
    Crea la estructura de carpetas necesaria basada en la fecha actual.

    Parameters:
        base_dir (str): Directorio raíz para la salida de clasificación.

    Returns:
        tuple: Rutas absolutas/relativas para la carpeta de plots,
               la carpeta de modelos y el prefijo de fecha.
    """
    date_str = datetime.datetime.now().strftime("%Y%m%d")

    dir_plots = os.path.join(base_dir, f"lvdsl_classify_{date_str}.plot")
    dir_models = os.path.join(base_dir, f"lvdsl_classify_{date_str}.model")

    os.makedirs(dir_plots, exist_ok=True)
    os.makedirs(dir_models, exist_ok=True)

    return dir_plots, dir_models, date_str

def get_classification_models(random_state=42):
    """
    Retorna el conjunto de clasificadores a evaluar.

    Returns:
        dict: Diccionario {nombre_modelo: instancia_clasificador}
    """
    models = {
        # Con poder explicativo
        "DecisionTree": DecisionTreeClassifier(
            max_depth=5,
            random_state=random_state
        ),
        "LogisticRegression": LogisticRegression(
            max_iter=1000,
            random_state=random_state
        ),

        # Caja negra / Geométricos
        "RandomForest": RandomForestClassifier(
            n_estimators=100,
            max_depth=6,
            random_state=random_state
        ),
        "KNN": KNeighborsClassifier(
            n_neighbors=5
        ),
        "XGBoost": XGBClassifier(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.1,
            eval_metric="logloss",
            random_state=random_state
        )
    }
    return models

def eval_model_on_dataset(model_name, model, X, y, dataset_name, dir_plots, dir_models):
    """
    Entrena y evalúa un clasificador sobre un dataset específico usando Stratified K-Fold.
    Captura excepciones para evitar el colapso del pipeline completo si un dataset/modelo falla.
    """
    # Verificación preventiva de clases únicas antes de CV
    unique_classes = np.unique(y)
    if len(unique_classes) < 2:
        print(f"    [!] Omitiendo {model_name} en {dataset_name}: Solo contiene la clase {unique_classes[0]}")
        return {
            "model_name": model_name,
            "dataset_name": dataset_name,
            "acc_mean": np.nan,
            "acc_std": np.nan,
            "f1_mean": np.nan,
            "cm_matrix": [],
            "model_path": "N/A (Error: Clase única)",
            "cm_plot_path": "N/A"
        }

    try:
        # 1. Validación Cruzada Estratificada (5 Folds) con fallback suave (error_score=np.nan)
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        scoring = ['accuracy', 'precision_macro', 'recall_macro', 'f1_macro']

        cv_results = cross_validate(
            model, X, y, cv=skf, scoring=scoring, n_jobs=-1, error_score=np.nan
        )

        acc_mean = float(np.nanmean(cv_results['test_accuracy']))
        acc_std = float(np.nanstd(cv_results['test_accuracy']))
        f1_mean = float(np.nanmean(cv_results['test_f1_macro']))

        # 2. Re-entrenamiento con el dataset completo
        model.fit(X, y)
        y_pred = model.predict(X)

        # 3. Guardar el modelo entrenado (.model)
        model_filename = f"model_{model_name}_{dataset_name}.model"
        model_path = os.path.join(dir_models, model_filename)
        joblib.dump(model, model_path)

        # 4. Generar y guardar la Matriz de Confusión (.png)
        cm = confusion_matrix(y, y_pred, labels=np.unique(y))
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=np.unique(y))

        fig, ax = plt.subplots(figsize=(6, 5), dpi=300)
        disp.plot(cmap="Blues", ax=ax, colorbar=False)
        ax.set_title(f"Confusion Matrix: {model_name}\nDataset: {dataset_name}", fontsize=11, fontweight="bold")
        plt.tight_layout()

        cm_filename = f"ConfusionMatrix_{model_name}_{dataset_name}.png"
        cm_path = os.path.join(dir_plots, cm_filename)
        plt.savefig(cm_path, format="png")
        plt.close(fig)

        return {
            "model_name": model_name,
            "dataset_name": dataset_name,
            "acc_mean": acc_mean,
            "acc_std": acc_std,
            "f1_mean": f1_mean,
            "cm_matrix": cm.tolist(),
            "model_path": model_path,
            "cm_plot_path": cm_path
        }

    except Exception as e:
        print(f"    [ERROR] Fallo al evaluar {model_name} sobre {dataset_name}: {str(e)}")
        return {
            "model_name": model_name,
            "dataset_name": dataset_name,
            "acc_mean": np.nan,
            "acc_std": np.nan,
            "f1_mean": np.nan,
            "cm_matrix": [],
            "model_path": f"ERROR: {str(e)}",
            "cm_plot_path": "N/A"
        }

def _eval_model_on_dataset(model_name, model, X, y, dataset_name, dir_plots, dir_models):
    """
    Entrena y evalúa un clasificador sobre un dataset específico usando Stratified K-Fold.
    Guarda la matriz de confusión (.png) y el modelo entrenado (.model).

    Parameters:
        model_name (str): Nombre identificador del modelo.
        model: Instancia del clasificador de scikit-learn/XGBoost.
        X (pd.DataFrame o np.ndarray): Matriz de características.
        y (pd.Series o np.ndarray): Vector de etiquetas.
        dataset_name (str): Nombre del dataset/reducción evaluada.
        dir_plots (str): Ruta a la carpeta de gráficos.
        dir_models (str): Ruta a la carpeta de modelos.

    Returns:
        dict: Resumen de métricas de desempeño y rutas de artefactos.
    """
    # 1. Validación Cruzada Estratificada (5 Folds)
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scoring = ['accuracy', 'precision_macro', 'recall_macro', 'f1_macro']

    cv_results = cross_validate(model, X, y, cv=skf, scoring=scoring, n_jobs=-1)

    acc_mean = float(np.mean(cv_results['test_accuracy']))
    acc_std = float(np.std(cv_results['test_accuracy']))
    f1_mean = float(np.mean(cv_results['test_f1_macro']))

    # 2. Re-entrenamiento con el dataset completo para persistencia y artefactos
    model.fit(X, y)
    y_pred = model.predict(X)

    # 3. Guardar el modelo entrenado (.model)
    model_filename = f"model_{model_name}_{dataset_name}.model"
    model_path = os.path.join(dir_models, model_filename)
    joblib.dump(model, model_path)

    # 4. Generar y guardar la Matriz de Confusión (.png)
    cm = confusion_matrix(y, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)

    fig, ax = plt.subplots(figsize=(6, 5), dpi=300)
    disp.plot(cmap="Blues", ax=ax, colorbar=False)
    ax.set_title(f"Confusion Matrix: {model_name}\nDataset: {dataset_name}", fontsize=11, fontweight="bold")
    plt.tight_layout()

    cm_filename = f"ConfusionMatrix_{model_name}_{dataset_name}.png"
    cm_path = os.path.join(dir_plots, cm_filename)
    plt.savefig(cm_path, format="png")
    plt.close(fig)

    return {
        "model_name": model_name,
        "dataset_name": dataset_name,
        "acc_mean": acc_mean,
        "acc_std": acc_std,
        "f1_mean": f1_mean,
        "cm_matrix": cm.tolist(),
        "model_path": model_path,
        "cm_plot_path": cm_path
    }


def plot_accuracy_comparison(results_list, dir_plots):
    """
    Genera y guarda una gráfica de barras comparando el Accuracy de cada modelo por dataset.

    Parameters:
        results_list (list): Lista de diccionarios retornados por eval_model_on_dataset.
        dir_plots (str): Ruta donde se guardará la imagen final.
    """
    df_res = pd.DataFrame(results_list)

    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    sns.barplot(
        data=df_res,
        x="dataset_name",
        y="acc_mean",
        hue="model_name",
        ax=ax,
        palette="viridis"
    )

    ax.set_title("Comparativa de Accuracy por Clasificador y Reducción Dimensional", fontsize=12, fontweight="bold")
    ax.set_xlabel("Dataset / Reducción", fontsize=10, fontweight="bold")
    ax.set_ylabel("Accuracy Promedio (5-Fold CV)", fontsize=10, fontweight="bold")
    ax.set_ylim(0, 1.05)
    ax.tick_params(axis='x', rotation=35)
    plt.setp(ax.get_xticklabels(), ha='right')
    ax.legend(title="Modelo", bbox_to_anchor=(1.02, 1), loc="upper left")

    # Anotar valores en las barras
    for p in ax.patches:
        height = p.get_height()
        if not np.isnan(height) and height > 0:
            ax.annotate(
                f"{height:.2f}",
                (p.get_x() + p.get_width() / 2., height),
                ha='center', va='bottom',
                fontsize=7, color='black',
                xytext=(0, 2), textcoords='offset points'
            )

    plt.tight_layout()
    output_path = os.path.join(dir_plots, "Accuracy_Comparison_All_Models.png")
    plt.savefig(output_path, format="png", bbox_inches="tight")
    plt.close(fig)


def write_classification_summary(base_dir, results_list, datasets_dict, target_col):
    """
    Escribe el informe detallado de ejecución y resultados en base_dir/lvdsl_classify_summary.txt.

    Parameters:
        base_dir (str): Directorio raíz del proceso lvdsl_classify_grid.
        results_list (list): Resultados recolectados durante la ejecución.
        datasets_dict (dict): Diccionario {nombre_dataset: dataframe}.
        target_col (str): Nombre de la columna objetivo / clase.
    """
    summary_path = os.path.join(base_dir, "lvdsl_classify_summary.txt")
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("======================================================================\n")
        f.write("        LVDSL - BITÁCORA DE RESUMEN DE CLASIFICACIÓN Y GRID         \n")
        f.write("======================================================================\n")
        f.write(f"Fecha de Ejecución: {now_str}\n\n")

        # 1. Información de los Datasets
        f.write("1. INFORMACIÓN DE LOS DATASETS EVALUADOS\n")
        f.write("----------------------------------------------------------------------\n")
        for ds_name, df in datasets_dict.items():
            n_rows, n_cols = df.shape
            features_count = n_cols - 1 if target_col in df.columns else n_cols
            f.write(f" Dataset: {ds_name}\n")
            f.write(f"   - Filas (Muestras): {n_rows}\n")
            f.write(f"   - Columnas Totales: {n_cols} (Características: {features_count})\n")
            if target_col in df.columns:
                class_dist = df[target_col].value_counts().to_dict()
                f.write(f"   - Distribución de Clases ({target_col}): {class_dist}\n")
            f.write("\n")

        # 2. Resultados por Combinación Modelo - Dataset
        f.write("2. RESULTADOS DE EVALUACIÓN Y ARTEFACTOS\n")
        f.write("----------------------------------------------------------------------\n")
        for res in results_list:
            f.write(f" [Modelo: {res['model_name']}]  <--->  [Dataset: {res['dataset_name']}]\n")
            f.write(f"   - Accuracy Mean (CV): {res['acc_mean']:.4f} (+/- {res['acc_std']:.4f})\n")
            f.write(f"   - F1-Score Mean (CV): {res['f1_mean']:.4f}\n")
            f.write(f"   - Matriz de Confusión: {res['cm_matrix']}\n")
            f.write(f"   - Modelo Guardado: {res['model_path']}\n")
            f.write(f"   - Gráfico Matriz: {res['cm_plot_path']}\n")
            f.write("-" * 70 + "\n")

    print(f"[+] Bitácora exportada exitosamente en: {summary_path}")


def run_classification_grid(datasets_dict, target_col="target", base_dir="lvdsl_classify_grid"):
    """
    Función orquestadora principal. Ejecuta la rejilla de modelos sobre todos los datasets.

    Parameters:
        datasets_dict (dict): Diccionario {"Nombre_Dataset": DataFrame}
        target_col (str): Nombre de la variable objetivo en los DataFrames.
        base_dir (str): Directorio raíz para los resultados.
    """
    dir_plots, dir_models, date_str = setup_output_directories(base_dir)
    models = get_classification_models()

    results = []

    print(f"[*] Iniciando Grid de Clasificación LVDSL ({date_str})...")

    for ds_name, df in datasets_dict.items():
        if target_col not in df.columns:
            print(f"[!] Advertencia: La columna '{target_col}' no existe en '{ds_name}'. Omitiendo...")
            continue

        X = df.drop(columns=[target_col])
        y = df[target_col]

        for model_name, model in models.items():
            print(f"  -> Evaluando {model_name} sobre {ds_name}...")
            res = eval_model_on_dataset(
                model_name, model, X, y, ds_name, dir_plots, dir_models
            )
            results.append(res)

    # Generar gráficos comparativos y bitácora final
    plot_accuracy_comparison(results, dir_plots)
    write_classification_summary(base_dir, results, datasets_dict, target_col)

    print("[+] Proceso de clasificación finalizado exitosamente.")






