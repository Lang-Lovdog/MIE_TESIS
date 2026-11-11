
#set terminal pdfcairo enhanced font "Linux Libertine,11" size 4.5,3.5
#set output "vacios_apilados_vertical.pdf"


#set terminal pdfcairo enhanced font "VictorMono Nerd Font,10" size 3,2.5

set terminal postscript color eps size 4,2.5
set output "vacios_apilados_horizontal.eps"

# Estilo de histograma apilado vertical
set style data histograms
set style histogram rowstacked
set style fill solid 0.90 border -1
set tics font "VictorMono Nerd Font,20"

# Grosor de barras y separación
set boxwidth 0.55

# Estética de ejes y cuadrícula (border 2 mantiene solo el eje vertical izquierdo)
set border 2 linetype -1 linewidth 0.8
set tics nomirror
set grid y linetype 1 linewidth 0.4 linecolor rgb "#e0e0e0"

# Rotulado de ejes (quitamos el xlabel para evitar redundancia en categorías)
set ylabel "Número de vacíos" font "VictorMono Nerd Font,20"
set xlabel ""

# Paleta Magma
color_estable   = "#8e208d"   # Coral/Naranja cálido
color_inestable = "#3b0f70"   # Púrpura oscuro profundo

# Leyenda superior fuera del área de trazado
set key outside top center horizontal samplen 1.5 spacing 1.25 box linetype -1 linewidth 0.4 font "VictorMono Nerd Font,20"

# Bloque de datos: Categoría, Estables, Inestables
$datos << EOD
dS     987   2309
AdS   1345   7338
EOD

# Gráfica principal con xtic(1) para mapear 'dS' y 'AdS' al eje X
plot $datos using 2:xtic(1) title "Estables" linecolor rgb color_estable, \
     ''     using 3        title "Inestables" linecolor rgb color_inestable, \
     ''     using 0:($2/2):($2 == 0 ? "" : sprintf("%d", $2)) \
            with labels textcolor rgb "white" font "VictorMono Nerd Font,20" notitle, \
     ''     using 0:($2 + $3/2):($3 == 0 ? "" : sprintf("%d", $3)) \
            with labels textcolor rgb "white" font "VictorMono Nerd Font,20" notitle

#### Gráfica principal de barras + capas automáticas de etiquetas centradas en cada segmento
###plot $datos using 2:key(1) title "Estables" linecolor rgb color_estable, \
###     ''     using 3        title "Inestables" linecolor rgb color_inestable, \
###     ''     using 0:($2/2):($2 == 0 ? "" : sprintf("%d", $2)) \
###            with labels textcolor rgb "white" font "Linux Libertine,9" notitle, \
###     ''     using 0:($2 + $3/2):($3 == 0 ? "" : sprintf("%d", $3)) \
###            with labels textcolor rgb "white" font "Linux Libertine,9" notitle
