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
SQUARE_SIZE = 20             # size of the square marker on the rung
SQUARE_ROUNDNESS = 4         # corner radius for the square (0 = sharp)

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
    
    # Backbones with a slight wave (sine) for realism
    # We'll draw a series of short lines for a smooth wave effect
    steps = 100
    amplitude = 6
    for step in range(steps):
        t = step / steps
        y1 = y_start + t * (y_end - y_start)
        y2 = y_start + (step+1)/steps * (y_end - y_start)
        # Sine wave displacement
        dx1 = amplitude * math.sin(t * math.pi * 2 * (CHROMOSOME_LEN/4))
        dx2 = amplitude * math.sin((step+1)/steps * math.pi * 2 * (CHROMOSOME_LEN/4))
        draw.line((left_x + dx1, y1, left_x + dx2, y2), fill=color, width=3)
        draw.line((right_x - dx1, y1, right_x - dx2, y2), fill=color, width=3)
    
    # Draw each rung (gene)
    for pos, value in enumerate(genes):
        y = y_start + pos * RUNG_SPACING
        # Draw horizontal rung line (straight for simplicity, but could also wave)
        draw.line((left_x, y, right_x, y), fill=color, width=2)
        
        # Draw a square marker on the rung representing gene intensity
        intensity = gene_to_intensity(value)
        square_color = (intensity, intensity, intensity)
        # Square centered at the midpoint of the rung
        cx = x_center
        cy = y
        half = SQUARE_SIZE // 2
        box = (cx - half, cy - half, cx + half, cy + half)
        # Outer neon square (individual color) slightly larger
        outer_box = (cx - half - 2, cy - half - 2, cx + half + 2, cy + half + 2)
        draw.rounded_rectangle(outer_box, radius=SQUARE_ROUNDNESS, outline=color, width=2)
        # Inner square filled with intensity
        draw.rounded_rectangle(box, radius=SQUARE_ROUNDNESS, fill=square_color)
        
        # Optional: tiny text showing the value
        # draw.text((cx-4, cy-6), str(value), fill=(200,200,200))

# ==================================================
# Save image
# ==================================================
os.makedirs("ftt_genetic_img", exist_ok=True)
output_path = "ftt_genetic_img/dna_squares_population.png"
img.save(output_path)
print(f"DNA helix with squares saved to: {output_path}")
