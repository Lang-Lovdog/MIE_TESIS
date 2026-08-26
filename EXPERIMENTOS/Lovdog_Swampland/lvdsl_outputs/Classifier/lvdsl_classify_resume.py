import base64
import os
import pandas as pd


def _build_file_tree(dir_path):
    """Construye una representación en texto en forma de árbol del directorio."""
    if not os.path.exists(dir_path):
        return f"{os.path.basename(dir_path)}/ [NO ENCONTRADO]\n"

    tree_lines = [f"{os.path.basename(os.path.abspath(dir_path))}/"]

    def recurse_dir(current_dir, depth_prefix=""):
        items = sorted(os.listdir(current_dir))
        for idx, item in enumerate(items):
            item_path = os.path.join(current_dir, item)
            is_last = idx == len(items) - 1
            connector = "└── " if is_last else "├── "
            tree_lines.append(f"{depth_prefix}{connector}{item}")

            if os.path.isdir(item_path):
                new_prefix = depth_prefix + ("    " if is_last else "│   ")
                recurse_dir(item_path, new_prefix)

    recurse_dir(dir_path)
    return "\n".join(tree_lines)


def _encode_images_from_dir(img_dir):
    """Convierte todas las imágenes PNG de un directorio a tarjetas HTML con base64."""
    html_cards = ""
    if img_dir and os.path.exists(img_dir):
        for img_file in sorted(os.listdir(img_dir)):
            if img_file.endswith(".png"):
                img_path = os.path.join(img_dir, img_file)
                with open(img_path, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode("utf-8")

                html_cards += f"""
                <div class="img-card">
                    <h4>{img_file}</h4>
                    <img src="data:image/png;base64,{encoded}" alt="{img_file}" />
                </div>
                """
    return html_cards


def generate_classification_html(
    reduc_dir="lvdsl_classify_dim_reduction",
    classify_dir="lvdsl_classify_grid",
    output_html_path="/tmp/lvdsl_reduc_dim.html",
):
    """Genera un reporte HTML monolítico autocontenido combinando los resultados

    de la Reducción Dimensional y de la Rejilla de Clasificación.
    """
    # -------------------------------------------------------------------------
    # 1. LECTURA DE BITÁCORAS
    # -------------------------------------------------------------------------
    reduc_txt_path = os.path.join(reduc_dir, "lvdsl_reduc_dim.txt")
    reduc_txt_content = (
        open(reduc_txt_path, "r", encoding="utf-8").read()
        if os.path.exists(reduc_txt_path)
        else "Sin bitácora de reducción."
    )

    classify_txt_path = os.path.join(classify_dir, "lvdsl_classify_summary.txt")
    classify_txt_content = (
        open(classify_txt_path, "r", encoding="utf-8").read()
        if os.path.exists(classify_txt_path)
        else "Sin bitácora de clasificación."
    )

    # -------------------------------------------------------------------------
    # 2. LOCALIZACIÓN DE SUBDIRECTORIOS (.img, .ds, .plot, .model)
    # -------------------------------------------------------------------------
    reduc_img_dir = None
    ds_dir = None
    if os.path.exists(reduc_dir):
        for item in os.listdir(reduc_dir):
            full_path = os.path.join(reduc_dir, item)
            if os.path.isdir(full_path):
                if item.endswith(".img"):
                    reduc_img_dir = full_path
                elif item.endswith(".ds"):
                    ds_dir = full_path

    classify_plot_dir = None
    if os.path.exists(classify_dir):
        for item in os.listdir(classify_dir):
            full_path = os.path.join(classify_dir, item)
            if os.path.isdir(full_path) and item.endswith(".plot"):
                classify_plot_dir = full_path

    # -------------------------------------------------------------------------
    # 3. ÁRBOLES DE DIRECTORIOS
    # -------------------------------------------------------------------------
    tree_reduc_str = _build_file_tree(reduc_dir)
    tree_classify_str = _build_file_tree(classify_dir)

    # -------------------------------------------------------------------------
    # 4. VISTA PREVIA DE DATASETS (.ds)
    # -------------------------------------------------------------------------
    ds_previews_html = ""
    if ds_dir and os.path.exists(ds_dir):
        for ds_file in sorted(os.listdir(ds_dir)):
            ds_path = os.path.join(ds_dir, ds_file)
            if ds_file.endswith(".csv"):
                df_preview = pd.read_csv(ds_path, nrows=5)
            elif ds_file.endswith(".parquet"):
                df_preview = pd.read_parquet(ds_path).head(5)
            else:
                continue

            table_html = df_preview.to_html(classes="ds-table", index=False)
            ds_previews_html += f"""
            <div class="card">
                <h3>{ds_file} <span class="badge">head(5)</span></h3>
                <div class="table-container">
                    {table_html}
                </div>
            </div>
            """

    # -------------------------------------------------------------------------
    # 5. EMBEDDING DE IMÁGENES (Reducción y Clasificación)
    # -------------------------------------------------------------------------
    reduc_gallery_html = _encode_images_from_dir(reduc_img_dir)
    classify_gallery_html = _encode_images_from_dir(classify_plot_dir)

    # -------------------------------------------------------------------------
    # 6. PLANTILLA HTML MONOLÍTICA
    # -------------------------------------------------------------------------
    html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LVDSL — Reporte Integrado: Reducción Dimensional & Clasificación</title>
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent: #38bdf8;
            --accent-green: #34d399;
            --border: #334155;
        }}
        body {{
            font-family: system-ui, -apple-system, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 2rem;
            line-height: 1.5;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        h1, h2, h3, h4 {{
            color: var(--accent);
            margin-top: 0;
        }}
        .section-title {{
            color: var(--accent-green);
            border-bottom: 2px solid var(--border);
            padding-bottom: 0.5rem;
            margin-top: 2.5rem;
            margin-bottom: 1.5rem;
        }}
        .card {{
            background-color: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        }}
        .grid-2col {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 1.5rem;
        }}
        pre {{
            background-color: #090d16;
            color: #a7f3d0;
            padding: 1rem;
            border-radius: 6px;
            overflow-x: auto;
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            font-size: 0.85rem;
            max-height: 500px;
        }}
        .table-container {{
            overflow-x: auto;
        }}
        .ds-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
            text-align: left;
        }}
        .ds-table th, .ds-table td {{
            padding: 8px 12px;
            border: 1px solid var(--border);
        }}
        .ds-table th {{
            background-color: #0f172a;
            color: var(--accent);
        }}
        .ds-table tr:nth-child(even) {{
            background-color: rgba(255, 255, 255, 0.02);
        }}
        .grid-gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 1.5rem;
        }}
        .img-card {{
            background-color: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1rem;
            text-align: center;
        }}
        .img-card img {{
            max-width: 100%;
            height: auto;
            border-radius: 4px;
        }}
        .badge {{
            font-size: 0.75rem;
            background-color: var(--border);
            color: var(--accent);
            padding: 2px 8px;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>LVDSL — Pipeline Experimental Integrado</h1>

        <!-- SECCIÓN 1: ESTRUCTURA DE ARCHIVOS -->
        <h2 class="section-title">1. Estructura de Salida y Artefactos (Árbol)</h2>
        <div class="grid-2col">
            <div class="card">
                <h3>Reducción Dimensional ({os.path.basename(reduc_dir)})</h3>
                <pre>{tree_reduc_str}</pre>
            </div>
            <div class="card">
                <h3>Rejilla de Clasificación ({os.path.basename(classify_dir)})</h3>
                <pre>{tree_classify_str}</pre>
            </div>
        </div>

        <!-- SECCIÓN 2: BITÁCORAS TÉCNICAS -->
        <h2 class="section-title">2. Bitácoras Técnicas de Ejecución</h2>
        <div class="grid-2col">
            <div class="card">
                <h3>lvdsl_reduc_dim.txt</h3>
                <pre>{reduc_txt_content}</pre>
            </div>
            <div class="card">
                <h3>lvdsl_classify_summary.txt</h3>
                <pre>{classify_txt_content}</pre>
            </div>
        </div>

        <!-- SECCIÓN 3: VISTA PREVIA DE DATASETS -->
        <h2 class="section-title">3. Vista Previa de Datasets Proyectados (.ds)</h2>
        {ds_previews_html if ds_previews_html else "<div class='card'><p>No se encontraron datasets generados en .ds</p></div>"}

        <!-- SECCIÓN 4: REJILLA DE CLASIFICACIÓN (PLOTS Y MATRICES) -->
        <h2 class="section-title">4. Resultados de Clasificación (Plots & Matrices)</h2>
        <div class="grid-gallery">
            {classify_gallery_html if classify_gallery_html else "<p>No se encontraron gráficos de clasificación.</p>"}
        </div>

        <!-- SECCIÓN 5: PROYECCIONES DE REDUCCIÓN DIMENSIONAL -->
        <h2 class="section-title">5. Proyecciones Espaciales de Reducción Dimensional (.img)</h2>
        <div class="grid-gallery">
            {reduc_gallery_html if reduc_gallery_html else "<p>No se encontraron imágenes de reducción dimensional.</p>"}
        </div>

    </div>
</body>
</html>
"""

    # -------------------------------------------------------------------------
    # 7. ESCRITURA EN DISCO
    # -------------------------------------------------------------------------
    os.makedirs(os.path.dirname(output_html_path), exist_ok=True)
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_template)

    print(f"[OK] Reporte HTML integrado generado en: {output_html_path}")

