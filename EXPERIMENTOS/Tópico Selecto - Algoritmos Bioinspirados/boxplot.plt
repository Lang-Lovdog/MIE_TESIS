function boxplot_it(Data_File, Title, x_label, y_label, Out_File){
# Establecer el título y las etiquetas del gráfico
set title "Gráfica de Caja (Bigote)"
set ylabel "Datos"
set xlabel ""
# Habilitar la creación de gráficas de caja
set style data candlesticks

# Definir el nombre del archivo de datos
datafile = "tu_archivo.dat"

# Crear la gráfica de caja usando los datos del archivo
plot datafile u 1 w candlesticks title 'Gráfica de Caja', \
     '' u 1:2:3:4 with points pointtype 7 title 'Datos'
}
