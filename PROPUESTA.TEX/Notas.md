---
title: Descriptor y meta-journal del proyecto de tesis
description: Aquí se describen detalles e ideas posiblemente relevantes a la tesis o al proyecto
author: Brandon Marquez Salazar (Lang Lovdog Inu Oókami)
categories: meta.journal
created: 2026-02-06T14:41:43-0600
updated: 2026-03-07T01:37:01-0600
version: 1.1.1
---

[Index](#indexnorgmd)

Este archivo servirá como complemento a mi diario de tesis
para poder tener comentarios que en la generalidad serían
poco relevantes al trabajo y más relevantes a mi pensamiento.

Como punto de partida, estos comentarios no se centrarán en
ser la documentación del código, sino un mero escape de
pensamientos que pueden o no, en un futuro, tomar relevancia.


# Definición del problema


Este es el primer punto a desarrollar, ¿qué estoy haciendo?
Bien, la respuesta parece clara en un inicio,
estoy mapeando el landscape, desde la interpretación de la
teoría K. Bueno, más bien, estoy mapeando el swampland.
Para poder continuar con este proyecto debo tener el contexto
de que es un paso a comprender el comportamiento del modelo.

Ahora, tengo un código en Mathematica a la que se le está
realizando ingeniería inversa para replicar el experimento,
este experimento originalmente usa Templado Simulado, luego
hace un refinamiento con gradiente conjugado.

Mi aproximación será con diversos métodos metaheurísticos.
Para lograr esto, cada aspecto del experimento original fue
considerado de modo que pueda tomar decisiones más adelante
en el proyecto.

Para la validación de mi implementación se necesita realizar
una corrida del método completo, para luego juzgar
gráficamente los resultados.

Admito que aquí es donde radica el detalle: para ver si mi
trabajo es implementable, debe ser probada en implementación.

Aquí otro detalle, para cerrar el capítulo. Durante este
cuatrimestre (Enero-Abril 2023) tomé un curso de algoritmos
bioinspirados. Trabajaremos en C, por lo que debo pasar a C
tanto la función como los descriptores de la función. Esto
siendo emocionante y pesado. Espero poder realizar bien el
proyecto y sacar algo relevante.


# Estructura del proyecto


Al momento, 06/02/2026 a las 15:00, estoy procurando que el
proyecto tenga una estructura clara en el árbol de
directorios que podrá ser tomado desde mi github una vez se
haya formalizado todo (está público, no sé si sea bueno).

Para lograr que mi trabajo sea correcto, si bien no puedo
hacer un sistema de ficheros de múltiple enlace, al menos
puedo dar a entender la estructura plana del árbol.

```liotree 

  | TESIS/                                          > El directorio relativo al proyecto de tesis.                          ||
  |- EXPERIMENTOS/                                  > El directorio donde realizo los códigos y cosas por el estilo.        ||
  |=-
  |-- CESAR-BRITO_ORIGINAL-DATA/                    > Información del experimento original                                  ||
  |-- Lovdog_Swampland/                             > El código donde estoy replicando el experimento del Dr. Cesar.        ||
  |=-
  |--- MetastableVacua.py                           > Módulo que contiene la función potencial y sus descriptores
  |                                                 correspondientes.                                                       ||
  |--- BusquedaGeneticos.py                         > Este script es la primera versión que implementa los
  |                                                 metaheurísticos en Python. Originalmente PSO y Genéticos.               ||
  |--- test_fitness_function.py                     > Aquí únicamente se evalúan los elementos según los resultados
  |                                                 esperados.                                                              ||
  |==
  |-- Mathematica_Stuff/                            > Código de Mathematica donde analizo sobre el experimento,
  |                                                 sintaxis, etc.                                                          ||
  |-- 'Tópico Selecto - Algoritmos Bioinspirados/'  > Directorio correspondiente a la UDA de algoritmos bioinspirados,
  |                                                 curso en el cual se estudian algoritmos de optimización
  |                                                 metaheurísticos, la razón de contener este directorio aquí es que
  |                                                 el enfoque del curso está dirigido al proyecto, dándole un carácter
  |                                                 de documentación/experimentación necesaria.                             ||
  |=-
  |--- pso.c
  |--- pso.h
  |--- vacua.c
  |--- vacua.h
  |--- test.c
  |--- test_multi.sh
  |--- resultados.txt
  |==
  |==
  |- venv/                                          > Producto del "setup.sh", es el entorno virtual donde se encuentran
  |                                                 los paquetes correspondientes al proyecto,  sin éste, no es posible
  |                                                 (ni recomendable) realizar ejecuciones del proyecto.                    ||
  |- Makefile                                       > Este es un archivo maestro que permite ejecutar cualquier código
  |                                                 simulación, prueba o tarea dentro del proyecto.                         ||
  |- Notas.norg                                     > Este meta-journal                                                     ||
  |- requirements.txt                               > Lista de paquetes y módulos necesarios para el proyecto. Si acaso
  |                                                 algún error de dependencias, verifíque las versiones a la fecha
  |                                                 última de instalación estable: 11/02/2026.                              ||
  |- setup.sh                                       > Script de configuración del entorno virtual de Pyrhon.                ||
  |- PresentaciónXX                                 > En caso de realizar alguna presentación, ésta llevará el nombre
  |                                                 respetando el patrón (plantilla de nombre).                             ||
  |- hyp                                            > Hipótesis y propuestas relevantes, algunas cosas que haya desarrollado
  |                                                 lo suficiente para una correcta presentación.                           ||

```


## Lista de presentaciones

- Presentación 01: Presentación sobre la teoría de cuerdas,
  el doctor Ascencio realizó observaciones sobre algunos
  conceptos teóricos que se registraron en el diario de
  tesis. La información aún no ha sido actualizada, es poco
  probable que se llegue a realizar dicha actualización.


# Makefile


Estoy consciente de que no debería ser una documentación
del proyecto, pero valdrá la pena considerar que el makefile
fungirá de forma importante en todo el proyecto, siendo el
archivo maestro para compilar y correr código; pero estoy
pensando en la forma correcta de implementarlo. Una de las
ideas es usar un sistema simple de sufijos y prefijos que
ofrezcan contexto suficiente, permitiendo el polimorfismo
necesario en los nombres. Pues, por ejemplo, si quiero una
ejecución del optimizador, para hacerlo sería 'make optimiza'
con la implicación de que podría ser la versión de python
base, la versión final formal, la versión en c, o la de
wolfram. Por lo tanto habré de sostener contexto en la
llamada a make.


## Opciones de desarrollo en make


A continuación las opciones del Makefile. Es preciso
corresponder que estas opciones son una lista incremental
debido a la naturaleza del proyecto.

- configure ............... # Configura el entorno (bash y python venv)
- genetico ................ # Realiza la optimización
- vacua ................... # Muestra la inicialización de la función potencial
- test_fitness ............ # Realiza pruebas de verificación de la función de fitness sobre la función potencial a
  # través de su definición simbólica
- help .................... # Muestra esta ayuda
- mathics ................. # Ejecuta el script de Mathematica
- update_pip .............. # Actualiza las dependencias del proyecto de Python
- py ...................... # Ejecuta Python en el entorno virtual
- bio_enjambre ............ # Ejecuta el algoritmo de enjambre (curso bioinspirados)
- bio_enjambre_it ......... # Ejecuta el script iterativo
- bio_enjambre_it_build ... # Compila el algoritmo de enjambre y Ejecuta el script iterativo


# Sobre'l programa de Lovdog Swampland


A día de hoy: 13/02/2023. Me he dado cuenta de que'n mi
implementación uso dS y AdS como suffijos de las funciones
co'l siguiente significado:

- foo__dS es una función que no utiliza lifting
- foo_AdS es una función que sí utiliza lifting

Esto es destacable pues es un error grave de concepto que se
heredará próximamente y debe ser resuelto para futuras
referencias sobre el código.

Lo correcto es el uso de dS para aquellos que tengan un
levantamiento teórico con los efectos de las D5-Branas y por
ello, que pasen de ser dS a AdS en un caso de éxito en la
búsqueda.

Por tanto en un sistema donde dicho lifing no existe,
entonces se conserva como un vacío AdS. Esto siendo, la 
primera versión de la función potencial.

En pocas palabras, aún si el sufijo es AdS, en realidad
se hace referencia a una función que implementa los efectos
de las D5-Branas, permitiendo realmente, en teoría la
predicción de un vacío dS. Por lo tanto, las otras funciones
son las que nos permites construir los vacíos AdS en
contraste con lo que su sufijo nos indica..

.....

Bien, para hoy 19/02/2023, el experimento que corría duró ya
al menos dos días desde su ejecución (y sigue en ejecución).
La cuenta se va al rededor de 15000 iteraciones totales
divididas en 100 iteraciones del optimizador por cada
elemento de la base de datos original, con 75 elementos cada
base de datos. Una en búsqueda de Veff y otra con Veff_lift.
Cada optimización buscará al mejor en 50 épocas, lo que le
da cierta lentitud al proceso.

Debo comentar que si bien se encontraron soluciones
interesantes, hay un problema grave. Los límites de
optimización del metaheurístico están mal establecidos, pues

- A3N3=[-100,100]
- s=(0,100]
- tau=(0,100]

Esto es un problema grave, si es posible que los elementos
encontrados tengan sentido, estaré contento, si no... Esto
fue tiempo perdido.

dS vs AdS
: El concepto de dS discutido en esta sección será meramente
  en pos de la clasificación dellos vacíos.
  En el esquema a continuación se puede observar la
  clasificación utilizada, permitiendo ilustrar el concepto de
  forma simplificada.
  
 
/handmade-images/vacua_classification.png

[Abrir imagen](#handmade-imagesvacuaclassificationpngmd)


# Diario

A partir de aquí comienzo a redactar miscelaneos necesarios
para entender lo que voy haciendo. Es posible que haya cosas
redundantes entre este meta diario y el diario físico. Eso
corroborará cualquier decisión como importante o, al menos
como llevada a cabo.


## Dom 01 de Marzo del 2026


He decidido, por cuestiones de la volatilidad de mi puesto de
trabajo, robustecer mi implementación.

Esta decisión tomó forma tras reflexionar sobre el tiempo
perdido en cada apagón del sistema que me ha hecho perder
horas de experimentación.

El próximo paso es la reesttructuración del Lovdog_Swampland

```liotree

  | Lovdog_Swampland/           > Carpeta del proyecto                                                                    ||
  |- lvdsl                      > Módulo del Lovdog Swapland                                                              ||
  |-- k_theory/                 > La teoría en revisión actual                                                            ||
  |=-
  |--- vars.py                  > Variables de la función potencial, definición simbólica de la función potencial, Hess y
  |                             autovalores. Además de algunas funciones auxiliares para fijar coeficientes/módulos y
  |                             precisión decimal de operación para sympy.                                                ||
  |==
  |-- potentials.py             > Definición de las funciones de evaluación, tanto de la versión lifting como de la
  |                             original. (Sujeto a cambio de nombre)                                                     ||
  |-- plots.py                  > Graficación de las funciones, las principales serán inspiradas en el experimento
  |                             original. Algunos extras en caso de ser necesario.                                        ||

```

CORREO_URGENTE
Hoy llegó el correo del Coordinador, la propuesta de tesis
debe entregarse a más tardar el 18 del presente mes.


## Mar 05 de Marzo del 2023

Hoy hubo un apagón mientras realizaba mis diagramas, los
cambios serán subidos.


___


[Index](#indexnorgmd)
