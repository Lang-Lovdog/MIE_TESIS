import os
import random
from PIL import Image, ImageDraw

# ==================================================
# Fixed parameters
# ==================================================
POP_SIZE = 7                # rows (individuals)
CHROMOSOME_LEN = 16         # genes per individual (columns)
GENE_MIN, GENE_MAX = 0, 9   # gene value range
CELL_W, CELL_H = 100, 40    # 2:5 aspect ratio (40/100 = 2/5)
CORNER_RADIUS = 12          # rounding radius (can be adjusted)
BORDER_WIDTH = 4            # neon border thickness
INNER_MARGIN = 3            # space between border and inner rectangle
OUTPUT_DIR = "ftt_genetic_img"
OUTPUT_FILE = "population.png"

# Row background colors (RGB) – deep, futuristic tones
ROW_BG_COLORS = [
    (25, 35, 55),   # deep blue
    (45, 30, 55),   # purple
    (30, 55, 45),   # teal
    (55, 35, 25),   # terracotta
    (35, 55, 30),   # moss green
    (55, 30, 45),   # dark magenta
    (40, 40, 60),   # blue‑grey
]

# Neon border color per row (customizable) – bright neon tones
NEON_COLORS = [
    (0, 255, 255),   # cyan
    (255, 0, 255),   # magenta
    (255, 255, 0),   # yellow
    (0, 255, 128),   # spring green
    (255, 128, 0),   # orange
    (128, 0, 255),   # violet
    (255, 64, 64),   # coral
]

# ==================================================
# Generate random population
# ==================================================
population = [
    [random.randint(GENE_MIN, GENE_MAX) for _ in range(CHROMOSOME_LEN)]
    for _ in range(POP_SIZE)
]

# ==================================================
# Create canvas
# ==================================================
img_w = CHROMOSOME_LEN * CELL_W
img_h = POP_SIZE * CELL_H
img = Image.new("RGB", (img_w, img_h), color=(8, 8, 16))  # very dark background

# ==================================================
# Draw each row (individual)
# ==================================================
for row, genes in enumerate(population):
    row_bg = ROW_BG_COLORS[row % len(ROW_BG_COLORS)]
    neon = NEON_COLORS[row % len(NEON_COLORS)]
    y0 = row * CELL_H

    for col, value in enumerate(genes):
        x0 = col * CELL_W
        box = (x0, y0, x0 + CELL_W, y0 + CELL_H)

        # 1. Rounded background for the whole cell (row color)
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle(box, radius=CORNER_RADIUS, fill=row_bg)

        # 2. Neon border (custom color for this row)
        draw.rounded_rectangle(box, radius=CORNER_RADIUS, outline=neon, width=BORDER_WIDTH)

        # 3. Inner rectangle showing gene intensity (0→white, 9→black)
        intensity = 255 - int((value / GENE_MAX) * 255)
        intensity = intensity/255 - 0.2 if intensity > 0.2 else intensity/255
        gene_color = (int(intensity*NEON_COLORS[row][0]), int(intensity*NEON_COLORS[row][1]), int(intensity*NEON_COLORS[row][2]))

        inner_box = (
            x0 + INNER_MARGIN, y0 + INNER_MARGIN,
            x0 + CELL_W - INNER_MARGIN, y0 + CELL_H - INNER_MARGIN
        )
        # Keep the same rounding but slightly smaller radius
        inner_radius = max(CORNER_RADIUS - 4, 0)
        draw.rounded_rectangle(inner_box, radius=inner_radius, fill=gene_color)

# ==================================================
# Save image
# ==================================================
os.makedirs(OUTPUT_DIR, exist_ok=True)
output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
img.save(output_path)
print(f"Image saved to: {output_path}")
