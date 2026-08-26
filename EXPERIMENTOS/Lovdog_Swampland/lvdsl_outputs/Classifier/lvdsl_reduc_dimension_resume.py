import base64
import os
import pandas as pd

def generate_experiment_html(
    base_dir="lvdsl_classify_dim_reduction",
    output_html_path="/tmp/lvdsl_reduc_dim.html"
):
    """
    Genera un reporte HTML monolítico autocontenido en /tmp/lvdsl_reduc_dim.html
    con el árbol de archivos, el reporte de texto, vista previa (head) de los datasets
    y las gráficas 2D/3D embebidas en base64.
    """
    txt_file_path = os.path.join(base_dir, "lvdsl_reduc_dim.txt")

    # 1. Leer contenido de la bitácora .txt
    txt_content = ""
    if os.path.exists(txt_file_path):
        with open(txt_file_path, "r", encoding="utf-8") as f:
            txt_content = f.read()
    else:
        txt_content = "No se encontró el archivo de bitácora lvdsl_reduc_dim.txt"

    # 2. Localizar subdirectorios .img y .ds
    img_dir = None
    ds_dir = None
    for item in os.listdir(base_dir):
        full_path = os.path.join(base_dir, item)
        if os.path.isdir(full_path):
            if item.endswith(".img"):
                img_dir = full_path
            elif item.endswith(".ds"):
                ds_dir = full_path

    # 3. Construir el árbol de archivos visual
    tree_lines = [f"{os.path.basename(os.path.abspath(base_dir))}/"]
    if os.path.exists(txt_file_path):
        tree_lines.append("├── lvdsl_reduc_dim.txt")

    if img_dir:
        tree_lines.append(f"├── {os.path.basename(img_dir)}/")
        imgs = sorted(os.listdir(img_dir))
        for idx, img in enumerate(imgs):
            prefix = "│   └── " if idx == len(imgs) - 1 else "│   ├── "
            tree_lines.append(f"{prefix}{img}")

    if ds_dir:
        tree_lines.append(f"└── {os.path.basename(ds_dir)}/")
        datasets = sorted(os.listdir(ds_dir))
        for idx, ds in enumerate(datasets):
            prefix = "    └── " if idx == len(datasets) - 1 else "    ├── "
            tree_lines.append(f"{prefix}{ds}")

    tree_str = "\n".join(tree_lines)

    # 4. Procesar vista previa (head) de datasets
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

    # 5. Embeber imágenes en base64
    img_gallery_html = ""
    if img_dir and os.path.exists(img_dir):
        for img_file in sorted(os.listdir(img_dir)):
            if img_file.endswith(".png"):
                img_path = os.path.join(img_dir, img_file)
                with open(img_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

                img_gallery_html += f"""
                <div class="img-card">
                    <h4>{img_file}</h4>
                    <img src="data:image/png;base64,{encoded_string}" alt="{img_file}" />
                </div>
                """

    # 6. Estructura HTML final monolítica
    html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LVDSL - Reporte de Reducción Dimensional</title>
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent: #38bdf8;
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
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1, h2, h3, h4 {{
            color: var(--accent);
            margin-top: 0;
        }}
        .card {{
            background-color: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        }}
        pre {{
            background-color: #090d16;
            color: #a7f3d0;
            padding: 1rem;
            border-radius: 6px;
            overflow-x: auto;
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            font-size: 0.9rem;
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
        <h1>LVDSL — Monolito de Reducción Dimensional</h1>

        <div class="card">
            <h2>Estructura de Salida (Árbol)</h2>
            <pre>{tree_str}</pre>
        </div>

        <div class="card">
            <h2>Bitácora Técnica (.txt)</h2>
            <pre>{txt_content}</pre>
        </div>

        <div class="card">
            <h2>Vista Previa de Datasets Generados (.ds)</h2>
            {ds_previews_html if ds_previews_html else "<p>No se encontraron datasets.</p>"}
        </div>

        <h2>Proyecciones Gráficas (.img)</h2>
        <div class="grid-gallery">
            {img_gallery_html if img_gallery_html else "<p>No se encontraron imágenes.</p>"}
        </div>
    </div>
</body>
</html>
"""

    # 7. Escribir el HTML monolítico final
    os.makedirs(os.path.dirname(output_html_path), exist_ok=True)
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_template)

    print(f"[OK] Reporte HTML monolítico generado con éxito en: {output_html_path}")

