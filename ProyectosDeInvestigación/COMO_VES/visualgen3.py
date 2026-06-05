import os
import random
import math
from PIL import Image, ImageDraw

# ==================================================
# Fixed parameters
# ==================================================
POP_SIZE = 7                 # number of individuals (helices)
CHROMOSOME_LEN = 16          # number of genes (rungs)
GENE_MIN, GENE_MAX = 0, 9    # gene value range

# Helix geometry
RUNG_SPACING = 32            # vertical distance between rungs (px)
HELIX_WIDTH = 80             # total width of one helix (px)
BACKBONE_OFFSET = 20         # horizontal distance from center to each backbone
RUNG_LENGTH = 40             # length of each rung (px)
CIRCLE_RADIUS = 12           # radius of the circle on the rung

# Image dimensions
img_w = POP_SIZE * HELIX_WIDTH
img_h = (CHROMOSOME_LEN - 1) * RUNG_SPACING + 60  # + margin top/bottom
BACKGROUND = (10, 10, 20)    # very dark blue/black

# Colors for each individual (row) – used for backbone lines and accents
INDIVIDUAL_COLORS = [
    (0, 255, 255),   # cyan
    (255, 0, 255),   # magenta
    (255, 255, 0),   # yellow
    (0, 255, 128),   # spring green
    (255, 128, 0),   # orange
    (128, 0, 255),   # violet
    (255, 64, 64),   # coral
]

# ==================================================
# Generate random population (list of individuals)
# ==================================================
population = [
    [random.randint(GENE_MIN, GENE_MAX) for _ in range(CHROMOSOME_LEN)]
    for _ in range(POP_SIZE)
]

# ==================================================
# Helper: map gene value to intensity (0..255)
# ==================================================
def gene_to_intensity(value):
    # 0 -> 255 (white), 9 -> 0 (black)
    return 255 - int((value / GENE_MAX) * 255)

# ==================================================
# Create canvas
# ==================================================
img = Image.new("RGB", (img_w, img_h), BACKGROUND)
draw = ImageDraw.Draw(img)

# ==================================================
# Draw each individual's DNA helix
# ==================================================
for idx, genes in enumerate(population):
    # Horizontal start of this helix
    x_center = idx * HELIX_WIDTH + HELIX_WIDTH // 2
    color = INDIVIDUAL_COLORS[idx % len(INDIVIDUAL_COLORS)]
    
    # Draw the two backbones (vertical lines)
    left_x = x_center - BACKBONE_OFFSET
    right_x = x_center + BACKBONE_OFFSET
    y_start = 30   # top margin
    y_end = y_start + (CHROMOSOME_LEN - 1) * RUNG_SPACING
    
    # Backbones with a slight wave to mimic a helix (optional: sine wave)
    # For simplicity, straight lines with neon style:
    draw.line((left_x, y_start, left_x, y_end), fill=color, width=3)
    draw.line((right_x, y_start, right_x, y_end), fill=color, width=3)
    
    # Draw each rung (gene)
    for pos, value in enumerate(genes):
        y = y_start + pos * RUNG_SPACING
        # Draw horizontal rung line
        draw.line((left_x, y, right_x, y), fill=color, width=2)
        
        # Draw a circle on the rung that represents the gene intensity
        intensity = gene_to_intensity(value)
        circle_color = (intensity, intensity, intensity)
        # Circle center is at the midpoint of the rung
        cx = x_center
        cy = y
        # Draw a glowing outer circle (neon-like) then inner circle
        # Outer ring in individual color
        draw.ellipse((cx - CIRCLE_RADIUS - 2, cy - CIRCLE_RADIUS - 2,
                      cx + CIRCLE_RADIUS + 2, cy + CIRCLE_RADIUS + 2),
                     outline=color, width=2)
        # Inner circle filled with intensity (white to black)
        draw.ellipse((cx - CIRCLE_RADIUS, cy - CIRCLE_RADIUS,
                      cx + CIRCLE_RADIUS, cy + CIRCLE_RADIUS),
                     fill=circle_color)
        # Optional: small text showing the gene value
        # (uncomment if needed)
        # draw.text((cx-4, cy-6), str(value), fill=(200,200,200))

# ==================================================
# Save image
# ==================================================
os.makedirs("ftt_genetic_img", exist_ok=True)
output_path = "ftt_genetic_img/dna_population.png"
img.save(output_path)
print(f"DNA helix population saved to: {output_path}")
