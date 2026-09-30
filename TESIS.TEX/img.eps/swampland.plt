# Configuración del terminal para exportar a PostScript Encapsulado (EPS) con color
#set terminal postscript eps enhanced color solid font 'Helvetica,12' size 3in, 2in
set terminal pdfcairo enhanced color solid font 'Helvetica,12' size 3in, 2in
set output 'swampland.pdf'

# Configuración de la vista (vista superior 2D)
set view map

# Rangos de x e y especificados en TikZ
set xrange [-3.5:3.5]
set yrange [-2.2:2.5]

# Desactivar ejes, marcas (ticks) y bordes para imitar "axis lines=none, ticks=none"
unset key
unset border
unset xtics
unset ytics
unset colorbox

# Definición de la paleta personalizada basada en los puntos RGB del colormap en TikZ
# Mapeo normalizado [0:1]:
# 0.0 -> (0, 25, 55)     [Cyan muy oscuro]
# 0.53 -> (10, 75, 125)  [Cyan oscuro]
# 0.80 -> (80, 215, 245) [Cyan claro]
# 0.93 -> (165, 115, 0)  [Ámbar]
# 1.00 -> (255, 235, 90) [Amarillo claro]
set palette defined ( \
    0.00  0.00 0.10 0.22, \
    0.53  0.04 0.29 0.49, \
    0.80  0.31 0.84 0.96, \
    0.93  0.65 0.45 0.00, \
    1.00  1.00 0.92 0.35  \
)

# Resolución / Número de muestras de la malla
set samples 300
set isosamples 300, 300
# Eliminar los márgenes interno y externo obligando a la gráfica a expandirse
set lmargin at screen 0
set rmargin at screen 1
set bmargin at screen 0
set tmargin at screen 1

# Función 3D convertida desde TikZ (los ángulos se evalúan en radianes directamente en gnuplot)
f(x, y) = sin(2.3*x + 1.7*y + 1.1) * cos(3.1*x - 1.4*y) \
        + 0.5 * sin(1.9*x*y + 2.4) \
        - 0.4 * cos(4.2*x - 0.7*y**2)

# Graficar la superficie utilizando pm3d con sombreado interpolado (shader=interp)
#set pm3d map interpolate 1,1
set pm3d border retrace 
splot f(x, y) with pm3d
