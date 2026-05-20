#!/bin/bash

# Abre un archivo eps a la vez, del 1 al último de la carpeta.
# Se usará la misma instancia de gv de ser posible

# Esperar por un Ctrl+C para salir
trap "exit" INT

files=$(ls *.eps)
contador=0

for file in $files
do
  timeout 10s gv $file
  #if [ $contador -gt 4 ]; then break; fi
  #contador=$((contador+1))
done
