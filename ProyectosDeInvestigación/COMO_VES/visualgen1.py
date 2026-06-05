import os
import random
from PIL import Image, ImageDraw

# ==================================================
# Parámetros fijos
# ==================================================
POP_SIZE = 7                 # número de individuos (filas)
CHROMOSOME_LEN = 16          # genes por individuo (columnas)
GENE_MIN, GENE_MAX = 0, 9    # rango del gen (0..9)
CELL_W, CELL_H = 60, 60      # tamaño de cada celda en píxeles
CORNER_RADIUS = 12           # redondeo de las esquinas
OUTPUT_DIR = "ftt_genetic_img"
OUTPUT_FILE = "population.png"

# Colores de fondo para cada fila (RGB) – estilo futurista, tonos oscuros y saturados
ROW_BG_COLORS = [
    (25, 35, 55),   # azul profundo
    (45, 30, 55),   # púrpura
    (30, 55, 45),   # verde azulado
    (55, 35, 25),   # terracota
    (35, 55, 30),   # verde musgo
    (55, 30, 45),   # magenta oscuro
    (40, 40, 60),   # gris azulado
]

# Color del borde neón de cada celda
NEON_BORDER = (0, 200, 255)   # cian brillante

# ==================================================
# Generar población aleatoria
# ==================================================
population = [
    [random.randint(GENE_MIN, GENE_MAX) for _ in range(CHROMOSOME_LEN)]
    for _ in range(POP_SIZE)
]

# ==================================================
# Crear lienzo
# ==================================================
img_w = CHROMOSOME_LEN * CELL_W
img_h = POP_SIZE * CELL_H
img = Image.new("RGB", (img_w, img_h), color=(8, 8, 16))  # fondo muy oscuro

# ==================================================
# Dibujar cada fila (individuo)
# ==================================================
for row, genes in enumerate(population):
    row_color = ROW_BG_COLORS[row % len(ROW_BG_COLORS)]
    y0 = row * CELL_H

    for col, value in enumerate(genes):
        x0 = col * CELL_W
        box = (x0, y0, x0 + CELL_W, y0 + CELL_H)

        # 1. Fondo redondeado del color de la fila
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle(box, radius=CORNER_RADIUS, fill=row_color)

        # 2. Borde neón (cian grueso) alrededor de la celda
        draw.rounded_rectangle(box, radius=CORNER_RADIUS, outline=NEON_BORDER, width=2)

        # 3. Rectángulo interior que muestra la intensidad del gen
        # Mapeo: valor 0 → blanco (255), valor 9 → negro (0)
        intensity = 255 - int((value / 9) * 255)
        gene_color = (intensity, intensity, intensity)

        margin = 6   # espacio interior para que se vea el borde
        inner_box = (
            x0 + margin, y0 + margin,
            x0 + CELL_W - margin, y0 + CELL_H - margin
        )
        draw.rounded_rectangle(inner_box, radius=CORNER_RADIUS - 3, fill=gene_color)

        # 4. (Opcional) añade el valor numérico dentro, con fuente pequeña
        # Se puede descomentar si se quiere ver el número
        # from PIL import ImageFont
        # try:
        #     font = ImageFont.truetype("arial.ttf", 14)
        # except:
        #     font = ImageFont.load_default()
        # draw.text((x0+CELL_W//2-6, y0+CELL_H//2-8), str(value), fill=(200,200,200), font=font)

# ==================================================
# Guardar imagen
# ==================================================
os.makedirs(OUTPUT_DIR, exist_ok=True)
output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
img.save(output_path)
print(f"Imagen guardada en: {output_path}")
