# Configuración de la ventana y el renderizado
set terminal qt size 800,600
set title "Función de Schwefel (Implementación Personalizada)"
set xlabel "x"
set ylabel "y"
set zlabel "Fitness"

# Rangos de búsqueda de Schwefel
set xrange [-500:500]
set yrange [-500:500]

# Estilo visual
set palette rgbformulae 33,13,10  # Colores atractivos (arcoíris)
set pm3d                              # Habilita el mapeo de color en 3D
set contour base                      # Dibuja líneas de contorno en la base
set hidden3d                          # Oculta las líneas de malla traseras
set samples 100                       # Resolución de la malla
set isosamples 100

# --- Definición de la función basada en tu código C ---
# Nota: gnuplot usa 'sin', 'sqrt' y 'abs'. 
# Tu condición (x > -500 && x < 500) se traduce con el operador ternario (?:)

f_schwefel(x) = (x >= -500 && x <= 500) ? (0.02 * x**2) : (-x * sin(sqrt(abs(x))))

# Fitness total para 2 parámetros (x e y) más la constante de ajuste
# fitness_val += (__CantidadDeParametros__)*418.9829
C = 2 * 418.9829
Z(x, y) = f_schwefel(x) + f_schwefel(y) + C

# Comando para graficar
splot Z(x, y) with pm3d title "Superficie de Fitness"

