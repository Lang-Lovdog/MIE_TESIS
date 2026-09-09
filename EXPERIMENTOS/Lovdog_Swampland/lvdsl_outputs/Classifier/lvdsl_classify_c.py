"""
LVDSL - Grid de Clasificación, Curvas de Aprendizaje y Reporte HTML
Módulo extendido para evaluar clasificadores personalizados, generar curvas de aprendizaje
y exportar reportes ejecutivos en HTML.
"""

import os
import sys
import joblib
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from lvdsl_utils import print_log

# Modelos de Clasificación
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier

# Métricas y Evaluación
from sklearn.model_selection import StratifiedKFold, cross_validate, learning_curve
from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay,
    accuracy_score,
    precision_recall_fscore_support
)
from sklearn.base import clone
from sklearn.model_selection import ParameterGrid

# Configuración global de gráficos
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'font.sans-serif': 'DejaVu Sans',
    'axes.edgecolor': '#cccccc',
    'axes.linewidth': 0.8
})

def setup_output_directories(base_dir="lvdsl_classify_grid"):
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    dir_plots = os.path.join(base_dir, f"lvdsl_classify_{date_str}.plot")
    dir_models = os.path.join(base_dir, f"lvdsl_classify_{date_str}.model")

    os.makedirs(dir_plots, exist_ok=True)
    os.makedirs(dir_models, exist_ok=True)

    return dir_plots, dir_models, date_str

def get_default_classification_models(random_state=42):
    """Retorna un diccionario base de modelos."""
    return {
        "DecisionTree_depth5": DecisionTreeClassifier(max_depth=5, random_state=random_state),
        "DecisionTree_depth10": DecisionTreeClassifier(max_depth=10, random_state=random_state),
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=random_state),
        "RandomForest_100": RandomForestClassifier(n_estimators=100, max_depth=6, random_state=random_state),
        "RandomForest_200": RandomForestClassifier(n_estimators=200, max_depth=10, random_state=random_state),
        "KNN_k3": KNeighborsClassifier(n_neighbors=3),
        "KNN_k5": KNeighborsClassifier(n_neighbors=5),
        "XGBoost_lr01": XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.1, eval_metric="logloss", random_state=random_state)
    }

def build_model_grid(param_grid, random_state=42):
    """
    Genera un diccionario de instancias de modelos a partir de una especificación en rejilla.

    Parameters:
        param_grid (dict): Diccionario con la estructura:
            {
                "NombreModelo": {
                    "base_estimator": InstanciaBase(),
                    "params": {
                        "param1": [val1, val2],
                        "param2": [val3, val4]
                    }
                }
            }
        random_state (int): Semilla para los modelos que soporten random_state.

    Returns:
        dict: Diccionario { "NombreModelo_param1_val1_param2_val3": InstanciaReconfigurada }
    """
    expanded_models = {}

    for model_key, spec in param_grid.items():
        base_estimator = spec["base_estimator"]
        grid_params = spec.get("params", {})

        # Si no hay parámetros para iterar, mantenemos la instancia base
        if not grid_params:
            expanded_models[model_key] = clone(base_estimator)
            continue

        # Generar todas las combinaciones posibles
        for param_combination in ParameterGrid(grid_params):
            # Clonar estimador para evitar compartir estado entre variaciones
            model_instance = clone(base_estimator)

            # Asignar random_state si el estimador lo soporta
            if hasattr(model_instance, "random_state"):
                param_combination["random_state"] = random_state

            # Configurar los hiperparámetros
            model_instance.set_params(**param_combination)

            # Crear una etiqueta clara para el identificador único
            param_str = "_".join(f"{k}{v}" for k, v in param_combination.items() if k != "random_state")
            tag_name = f"{model_key}_{param_str}" if param_str else model_key

            expanded_models[tag_name] = model_instance

    return expanded_models


def plot_learning_curve(model, X, y, model_name, dataset_name, dir_plots):
    """Genera y guarda la gráfica de la curva de aprendizaje."""
    train_sizes, train_scores, test_scores = learning_curve(
        model, X, y, cv=5, scoring='accuracy', n_jobs=1,
        train_sizes=np.linspace(0.1, 1.0, 5), random_state=42
    )

    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)

    fig, ax = plt.subplots(figsize=(6, 4.5), dpi=300)
    ax.plot(train_sizes, train_mean, 'o-', color='#2b5c8f', label='Training Score')
    ax.plot(train_sizes, test_mean, 'o-', color='#d95f02', label='Cross-Validation Score')

    ax.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.15, color='#2b5c8f')
    ax.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, alpha=0.15, color='#d95f02')

    ax.set_title(f"Learning Curve: {model_name}\nDataset: {dataset_name}", fontsize=10, fontweight="bold")
    ax.set_xlabel("Training Examples", fontsize=9, fontweight="bold")
    ax.set_ylabel("Accuracy", fontsize=9, fontweight="bold")
    ax.set_ylim(0, 1.05)
    ax.legend(loc="lower right", fontsize=8)
    plt.tight_layout()

    lc_filename = f"LearningCurve_{model_name}_{dataset_name}.png"
    lc_path = os.path.join(dir_plots, lc_filename)
    plt.savefig(lc_path, format="png")
    plt.close(fig)
    return lc_path

def eval_model_on_dataset(model_name, model, X, y, dataset_name, dir_plots, dir_models):
    """Entrena, evalúa, genera matrices de confusión y curva de aprendizaje."""
    unique_classes = np.unique(y)
    if len(unique_classes) < 2:
        return {
            "model_name": model_name,
            "dataset_name": dataset_name,
            "params": str(model.get_params()),
            "acc_mean": np.nan, "acc_std": np.nan, "f1_mean": np.nan,
            "cm_matrix": [], "model_path": "N/A", "cm_plot_path": "N/A", "lc_plot_path": "N/A"
        }

    try:
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        scoring = ['accuracy', 'precision_macro', 'recall_macro', 'f1_macro']

        cv_results = cross_validate(model, X, y, cv=skf, scoring=scoring, n_jobs=1, error_score=np.nan)

        acc_mean = float(np.nanmean(cv_results['test_accuracy']))
        acc_std = float(np.nanstd(cv_results['test_accuracy']))
        f1_mean = float(np.nanmean(cv_results['test_f1_macro']))

        # Curva de aprendizaje
        lc_plot_path = plot_learning_curve(model, X, y, model_name, dataset_name, dir_plots)

        # Fit final
        model.fit(X, y)
        y_pred = model.predict(X)

        # Guardado de modelo
        model_filename = f"model_{model_name}_{dataset_name}.model"
        model_path = os.path.join(dir_models, model_filename)
        joblib.dump(model, model_path)

        # Matriz de confusión
        cm = confusion_matrix(y, y_pred, labels=np.unique(y))
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=np.unique(y))

        fig, ax = plt.subplots(figsize=(5, 4), dpi=300)
        disp.plot(cmap="Blues", ax=ax, colorbar=False)
        ax.set_title(f"Confusion Matrix: {model_name}\nDataset: {dataset_name}", fontsize=10, fontweight="bold")
        plt.tight_layout()

        cm_filename = f"ConfusionMatrix_{model_name}_{dataset_name}.png"
        cm_path = os.path.join(dir_plots, cm_filename)
        plt.savefig(cm_path, format="png")
        plt.close(fig)

        return {
            "model_name": model_name,
            "dataset_name": dataset_name,
            "params": str(model.get_params()),
            "acc_mean": acc_mean,
            "acc_std": acc_std,
            "f1_mean": f1_mean,
            "cm_matrix": cm.tolist(),
            "model_path": model_path,
            "cm_plot_path": cm_path,
            "lc_plot_path": lc_plot_path
        }

    except Exception as e:
        print_log(f"    [ERROR] Fallo al evaluar {model_name} sobre {dataset_name}: {str(e)}")
        return {
            "model_name": model_name,
            "dataset_name": dataset_name,
            "params": str(model.get_params()),
            "acc_mean": np.nan, "acc_std": np.nan, "f1_mean": np.nan,
            "cm_matrix": [], "model_path": f"ERROR: {str(e)}", "cm_plot_path": "N/A", "lc_plot_path": "N/A"
        }

def plot_accuracy_comparison(results_list, dir_plots):
    df_res = pd.DataFrame(results_list)
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    sns.barplot(data=df_res, x="dataset_name", y="acc_mean", hue="model_name", ax=ax, palette="viridis")

    ax.set_title("Comparativa de Accuracy por Clasificador y Reducción Dimensional", fontsize=12, fontweight="bold")
    ax.set_xlabel("Dataset / Reducción", fontsize=10, fontweight="bold")
    ax.set_ylabel("Accuracy Promedio (5-Fold CV)", fontsize=10, fontweight="bold")
    ax.set_ylim(0, 1.05)
    ax.tick_params(axis='x', rotation=35)
    plt.setp(ax.get_xticklabels(), ha='right')
    ax.legend(title="Modelo", bbox_to_anchor=(1.02, 1), loc="upper left")

    plt.tight_layout()
    output_path = os.path.join(dir_plots, "Accuracy_Comparison_All_Models.png")
    plt.savefig(output_path, format="png", bbox_inches="tight")
    plt.close(fig)
    return output_path

def write_html_summary(base_dir, results_list, datasets_dict, target_col, comparison_plot_path, html_suffix=None):
    """Genera un reporte interactivo en HTML con estilos CSS embebidos."""
    if html_suffix is not None:
        html_path = os.path.join(base_dir, f"lvdsl_classify_report_{html_suffix}.html")
    else:
        html_path = os.path.join(base_dir, "lvdsl_classify_report.html")
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>LVDSL - Reporte de Clasificación</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 30px; background-color: #f8f9fa; color: #333; }}
        h1, h2, h3 {{ color: #1a365d; }}
        .card {{ background: white; padding: 20px; margin-bottom: 25px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.9em; }}
        th, td {{ padding: 10px 12px; border: 1px solid #e2e8f0; text-align: left; }}
        th {{ background-color: #2b6cb0; color: white; }}
        tr:nth-child(even) {{ background-color: #f7fafc; }}
        .img-container {{ display: flex; gap: 10px; flex-wrap: wrap; margin-top: 10px; }}
        .img-card {{ background: #edf2f7; padding: 10px; border-radius: 6px; text-align: center; }}
        img {{ max-width: 320px; height: auto; border-radius: 4px; border: 1px solid #cbd5e0; }}
        .badge {{ background-color: #319795; color: white; padding: 3px 8px; border-radius: 4px; font-size: 0.8em; }}
    </style>
</head>
<body>
    <h1>LVDSL - Reporte Ejecutivo de Clasificación</h1>
    <p><strong>Fecha de Generación:</strong> {now_str}</p>

    <div class="card">
        <h2>1. Información de Datasets Evaluados</h2>
        <table>
            <tr>
                <th>Dataset</th>
                <th>Muestras (Filas)</th>
                <th>Características</th>
                <th>Distribución de Clases</th>
            </tr>"""

    for ds_name, df in datasets_dict.items():
        n_rows, n_cols = df.shape
        feat_cnt = n_cols - 1 if target_col in df.columns else n_cols
        dist_str = str(df[target_col].value_counts().to_dict()) if target_col in df.columns else "N/A"
        html_content += f"""
            <tr>
                <td><strong>{ds_name}</strong></td>
                <td>{n_rows}</td>
                <td>{feat_cnt}</td>
                <td><code>{dist_str}</code></td>
            </tr>"""

    html_content += f"""
        </table>
    </div>

    <div class="card">
        <h2>2. Comparativa General de Rendimiento</h2>
        <img src="{os.path.relpath(comparison_plot_path, base_dir)}" style="max-width: 100%; height: auto;">
    </div>

    <div class="card">
        <h2>3. Detalle por Modelo y Artefactos</h2>
        <table>
            <tr>
                <th>Modelo</th>
                <th>Dataset</th>
                <th>Accuracy (CV)</th>
                <th>F1-Score (CV)</th>
                <th>Artefactos Visuales</th>
            </tr>"""

    for res in results_list:
        acc_str = f"{res['acc_mean']:.4f} (±{res['acc_std']:.4f})" if not np.isnan(res['acc_mean']) else "N/A"
        f1_str = f"{res['f1_mean']:.4f}" if not np.isnan(res['f1_mean']) else "N/A"

        cm_rel = os.path.relpath(res['cm_plot_path'], base_dir) if res['cm_plot_path'] != "N/A" else ""
        lc_rel = os.path.relpath(res['lc_plot_path'], base_dir) if res['lc_plot_path'] != "N/A" else ""

        html_content += f"""
            <tr>
                <td><strong>{res['model_name']}</strong></td>
                <td><span class="badge">{res['dataset_name']}</span></td>
                <td>{acc_str}</td>
                <td>{f1_str}</td>
                <td>
                    <div class="img-container">"""
        if cm_rel:
            html_content += f'<div class="img-card"><p>Matriz de Confusión</p><img src="{cm_rel}"></div>'
        if lc_rel:
            html_content += f'<div class="img-card"><p>Curva de Aprendizaje</p><img src="{lc_rel}"></div>'

        html_content += """
                    </div>
                </td>
            </tr>"""

    html_content += """
        </table>
    </div>
</body>
</html>"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print_log(f"[+] Reporte HTML generado exitosamente en: {html_path}")

def run_classification_grid(datasets_dict, custom_models=None, target_col="target", base_dir="lvdsl_classify_grid", generate_html=True, html_suffix=None):
    """
    Orquestador principal.
    Permite pasar una rejilla/diccionario personalizado de modelos vía 'custom_models'.
    """
    dir_plots, dir_models, date_str = setup_output_directories(base_dir)

    # Si se pasa un diccionario personalizado, se usa ese; si no, el default
    models = custom_models if custom_models is not None else get_default_classification_models()

    results = []
    print_log(f"[*] Iniciando Grid de Clasificación LVDSL ({date_str})...")

    for ds_name, df in datasets_dict.items():
        if target_col not in df.columns:
            print_log(f"[!] Advertencia: La columna '{target_col}' no existe en '{ds_name}'. Omitiendo...")
            continue

        X = df.drop(columns=[target_col])
        y = df[target_col]

        for model_name, model in models.items():
            print_log(f"  -> Evaluando {model_name} sobre {ds_name}...")
            res = eval_model_on_dataset(model_name, model, X, y, ds_name, dir_plots, dir_models)
            results.append(res)
            #print(res)

    comp_plot_path = plot_accuracy_comparison(results, dir_plots)

    if generate_html:
        write_html_summary(base_dir, results, datasets_dict, target_col, comp_plot_path,html_suffix)

    print_log("[+] Proceso de clasificación completado.")
