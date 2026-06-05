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

# Helix geometry (base units)
RUNG_SPACING = 32
HELIX_WIDTH = 80
BACKBONE_OFFSET = 20
MARKER_W = 25
MARKER_H = 10
MARKER_ROUND = 4

# High‑resolution scaling – NO FINAL DOWNSAMPLE
SCALE_FACTOR = 6   # increase for even smoother results

# Image dimensions (scaled up)
img_w = POP_SIZE * HELIX_WIDTH
img_h = (CHROMOSOME_LEN - 1) * RUNG_SPACING + 60
orig_w, orig_h = img_w, img_h
img_w *= SCALE_FACTOR
img_h *= SCALE_FACTOR

BACKGROUND = (250, 250, 245)      # off‑white

# Colors (unchanged)
INDIVIDUAL_COLORS = [
    (20, 60, 180), (180, 20, 40), (20, 120, 40),
    (180, 100, 20), (100, 20, 140), (0, 120, 120), (140, 60, 20)
]

# ==================================================
# Generate random population
# ==================================================
population = [
    [random.randint(GENE_MIN, GENE_MAX) for _ in range(CHROMOSOME_LEN)]
    for _ in range(POP_SIZE)
]

# ==================================================
# Color helpers
# ==================================================
def gene_color_from_base(value, base_color, light_factor=1.5, dark_factor=0.5):
    t = value / GENE_MAX
    light = tuple(min(255, int(c * light_factor)) for c in base_color)
    dark = tuple(int(c * dark_factor) for c in base_color)
    r = int(light[0] * (1 - t) + dark[0] * t)
    g = int(light[1] * (1 - t) + dark[1] * t)
    b = int(light[2] * (1 - t) + dark[2] * t)
    return (r, g, b)

# ==================================================
# Create high‑resolution canvas
# ==================================================
img = Image.new("RGB", (img_w, img_h), BACKGROUND)
draw = ImageDraw.Draw(img)

# Scale all geometry
def scale(x):
    return x * SCALE_FACTOR

# ==================================================
# Draw each DNA helix (all coordinates scaled)
# ==================================================
for idx, genes in enumerate(population):
    x_center = scale(idx * HELIX_WIDTH + HELIX_WIDTH // 2)
    color = INDIVIDUAL_COLORS[idx % len(INDIVIDUAL_COLORS)]

    left_x = x_center - scale(BACKBONE_OFFSET)
    right_x = x_center + scale(BACKBONE_OFFSET)
    y_start = scale(30)
    y_end = y_start + scale((CHROMOSOME_LEN - 1) * RUNG_SPACING)

    # Waved backbones – smoother with more steps and scaled amplitude
    steps = 200
    amplitude = scale(6)
    for step in range(steps):
        t = step / steps
        y1 = y_start + t * (y_end - y_start)
        y2 = y_start + (step+1)/steps * (y_end - y_start)
        dx1 = amplitude * math.sin(t * math.pi * 2 * (CHROMOSOME_LEN/4))
        dx2 = amplitude * math.sin((step+1)/steps * math.pi * 2 * (CHROMOSOME_LEN/4))
        draw.line((left_x + dx1, y1, left_x + dx2, y2), fill=color, width=scale(3))
        draw.line((right_x - dx1, y1, right_x - dx2, y2), fill=color, width=scale(3))

    # Draw rungs and 5:2 markers
    for pos, value in enumerate(genes):
        y = y_start + scale(pos * RUNG_SPACING)
        draw.line((left_x, y, right_x, y), fill=color, width=scale(2))

        # Gene color
        if USE_COLOR_FOR_VALUE:
            gene_color = gene_color_from_base(value, color)
        else:
            gray = 50 + int((value / GENE_MAX) * 180)
            gene_color = (gray, gray, gray)

        # Scaled 5:2 rectangle
        cx, cy = x_center, y
        half_w = scale(MARKER_W // 2)
        half_h = scale(MARKER_H // 2)
        box = (cx - half_w, cy - half_h, cx + half_w, cy + half_h)
        outer_box = (cx - half_w - scale(2), cy - half_h - scale(2),
                     cx + half_w + scale(2), cy + half_h + scale(2))
        draw.rounded_rectangle(outer_box, radius=scale(MARKER_ROUND), outline=color, width=scale(2))
        draw.rounded_rectangle(box, radius=scale(MARKER_ROUND), fill=gene_color)

# ==================================================
# Save image – NO DOWNSAMPLING, keep high resolution
# ==================================================
os.makedirs("ftt_genetic_img", exist_ok=True)
output_path = "ftt_genetic_img/dna_squares_hires.png"
img.save(output_path)
print(f"High‑resolution DNA helix saved to: {output_path}")
print(f"Size: {img.width}×{img.height} pixels (no scaling artifacts)")
