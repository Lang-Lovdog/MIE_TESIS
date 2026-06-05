import os
import random
import math
from PIL import Image, ImageDraw

# ==================================================
# Fixed parameters
# ==================================================
POP_SIZE = 7
CHROMOSOME_LEN = 16
GENE_MIN, GENE_MAX = 0, 9
USE_COLOR_FOR_VALUE = True   # False for grayscale

# Helix geometry
RUNG_SPACING = 62
HELIX_WIDTH = 80
BACKBONE_OFFSET = 20
RUNG_LENGTH = 40
SQUARE_SIZE = 20
SQUARE_ROUNDNESS = 4
SCALE_FACTOR = 2   # draw at double size then shrink for anti‑aliasing
MARKER_W = 25        # width  (5 parts)
MARKER_H = 10        # height (2 parts)
MARKER_ROUND = 4     # corner radius

# Image dimensions
img_w = POP_SIZE * HELIX_WIDTH
img_h = (CHROMOSOME_LEN - 1) * RUNG_SPACING + 60
orig_w, orig_h = img_w, img_h
BACKGROUND = (250, 250, 245)      # off‑white, paper‑friendly

# Colors for backbones and borders – darker, muted, print‑friendly
#INDIVIDUAL_COLORS = [
#    (30, 80, 120),   # muted blue
#    (100, 40, 120),  # plum
#    (40, 100, 60),   # forest green
#    (120, 80, 30),   # ochre
#    (80, 50, 100),   # mauve
#    (50, 90, 110),   # slate
#    (110, 70, 50),   # rust
#]

## Hight contrast-jewel
#INDIVIDUAL_COLORS = [
#    (0, 100, 200),      # strong blue
#    (200, 0, 100),      # raspberry
#    (0, 150, 80),       # emerald
#    (220, 120, 0),      # orange
#    (120, 0, 180),      # purple
#    (0, 180, 180),      # teal
#    (180, 80, 0),       # burnt orange
#]

## Vivid Rainbow
#INDIVIDUAL_COLORS = [
#    (230, 0, 0),        # red
#    (0, 180, 0),        # green
#    (0, 0, 230),        # blue
#    (230, 150, 0),      # gold
#    (150, 0, 180),      # violet
#    (0, 180, 150),      # sea green
#    (200, 0, 150),      # magenta
#]

## Saturated Dark
INDIVIDUAL_COLORS = [
    (20, 60, 180),      # royal blue
    (180, 20, 40),      # cardinal red
    (20, 120, 40),      # forest
    (180, 100, 20),     # ochre
    (100, 20, 140),     # plum
    (0, 120, 120),      # deep teal
    (140, 60, 20),      # rust
]

# ==================================================
# Generate random population
# ==================================================
population = [
    [random.randint(GENE_MIN, GENE_MAX) for _ in range(CHROMOSOME_LEN)]
    for _ in range(POP_SIZE)
]

# ==================================================
# Helper: map gene value to gray intensity
# 0 -> dark gray (visible), 9 -> light gray
# ==================================================
def gene_to_gray(value):
    # 0 -> 50, 9 -> 230 (avoid pure black/white for print)
    return 50 + int((value / GENE_MAX) * 180)

def gene_to_color(value):
    # 0 -> (0, 100, 200) deep blue, 9 -> (220, 50, 50) red
    r = int((value / GENE_MAX) * 220)
    g = int((value / GENE_MAX) * 50)
    b = 200 - int((value / GENE_MAX) * 200)
    return (r, g, b)

def gene_color_from_base(value, base_color, light_factor=1.5, dark_factor=0.5):
    """
    value: 0..9
    base_color: tuple (R,G,B)
    light_factor: multiplicador para aclarar (>1)
    dark_factor: multiplicador para oscurecer (<1)
    returns RGB tuple
    """
    # Normalizar value a 0..1
    t = value / GENE_MAX   # 0 -> light, 1 -> dark

    # Calcular color claro y oscuro
    light = tuple(min(255, int(c * light_factor)) for c in base_color)
    dark  = tuple(int(c * dark_factor) for c in base_color)

    # Interpolación lineal
    r = int(light[0] * (1 - t) + dark[0] * t)
    g = int(light[1] * (1 - t) + dark[1] * t)
    b = int(light[2] * (1 - t) + dark[2] * t)
    return (r, g, b)

# ==================================================
# Create canvas
# ==================================================
orig_w, orig_h = img_w, img_h
img = Image.new("RGB", (orig_w * SCALE_FACTOR, orig_h * SCALE_FACTOR), BACKGROUND)
draw = ImageDraw.Draw(img)

# ==================================================
# Draw each individual's DNA helix
# ==================================================
for idx, genes in enumerate(population):
    x_center = idx * HELIX_WIDTH + HELIX_WIDTH // 2
    color = INDIVIDUAL_COLORS[idx % len(INDIVIDUAL_COLORS)]

    left_x = x_center - BACKBONE_OFFSET
    right_x = x_center + BACKBONE_OFFSET
    y_start = 30
    y_end = y_start + (CHROMOSOME_LEN - 1) * RUNG_SPACING

    # Draw waved backbones (subtle sine, same amplitude as before)
    steps = 100
    amplitude = 6
    for step in range(steps):
        t = step / steps
        y1 = y_start + t * (y_end - y_start)
        y2 = y_start + (step+1)/steps * (y_end - y_start)
        dx1 = amplitude * math.sin(t * math.pi * 2 * (CHROMOSOME_LEN/4))
        dx2 = amplitude * math.sin((step+1)/steps * math.pi * 2 * (CHROMOSOME_LEN/4))
        draw.line((left_x + dx1, y1, left_x + dx2, y2), fill=color, width=3)
        draw.line((right_x - dx1, y1, right_x - dx2, y2), fill=color, width=3)

    # Draw rungs and squares
    # Inside the main loop over idx, genes
    for pos, value in enumerate(genes):
        y = y_start + pos * RUNG_SPACING
        draw.line((left_x, y, right_x, y), fill=color, width=2)

        # Determine gene color
        if USE_COLOR_FOR_VALUE:
            t = value / GENE_MAX
            gene_color = gene_color_from_base(value, color)
        else:
            gray = 50 + int((value / GENE_MAX) * 180)
            gene_color = (gray, gray, gray)

        # 5:2 rectangle
        cx, cy = x_center, y
        half_w = MARKER_W // 2
        half_h = MARKER_H // 2
        box = (cx - half_w, cy - half_h, cx + half_w, cy + half_h)
        outer_box = (cx - half_w - 2, cy - half_h - 2, cx + half_w + 2, cy + half_h + 2)
        draw.rounded_rectangle(outer_box, radius=MARKER_ROUND, outline=color, width=2)
        draw.rounded_rectangle(box, radius=MARKER_ROUND, fill=gene_color)

# ==================================================
# Save image
# ==================================================
os.makedirs("ftt_genetic_img", exist_ok=True)
output_path = "ftt_genetic_img/dna_squares_light.png"
img = img.resize((orig_w, orig_h), Image.LANCZOS)
img.save(output_path)
print(f"Print‑friendly DNA helix saved to: {output_path}")
