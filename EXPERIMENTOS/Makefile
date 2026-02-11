# Simple makefile to run python experiments

ProjectDir=Lovdog_Swampland
MathicsDir=Mathematica_Stuff

.PHONY: all

all: help

genetico:
	. venv/bin/activate && \
		cd $(ProjectDir)  && \
		python3 BusquedaGeneticos.py

vacua:
	. venv/bin/activate && \
		cd $(ProjectDir)  && \
	  python3 MetastableVacua.py

test_fitness:
	. venv/bin/activate && \
		cd $(ProjectDir)  && \
	  python3 test_fitness_function.py

configure:
	bash setup.sh

mathics:
	. venv/bin/activate && \
		cd $(MathicsDir)  && \
	  mathicsscript --no-prompt < MetastableVacua-Mathematica-rewritten-script-run.wl

update_pip:
	. venv/bin/activate && \
		python3 -m pip install --upgrade pip && \
		python3 -m pip install -r requirements.txt

py:
	. venv/bin/activate && python

bio_enjambre:
	cd "./Tópico Selecto - Algoritmos Bioinspirados" &&\
	gcc -o exe pso.c test.c -lm &&\
	./exe

bio_enjambre_it_build:
	cd "./Tópico Selecto - Algoritmos Bioinspirados" &&\
	gcc -o exe pso.c test.c -lm &&\
	./test_multi.sh

bio_enjambre_it:
	cd "./Tópico Selecto - Algoritmos Bioinspirados" &&\
	./test_multi.sh

help:
	@echo "make configure ............... # Configura el entorno (bash y python venv)"
	@echo "make genetico ................ # Realiza la optimización"
	@echo "make vacua ................... # Muestra la inicialización de la función potencial"
	@echo "make test_fitness ............ # Realiza pruebas de verificación de la función de fitness sobre la función potencial a través de su definición simbólica"
	@echo "make help .................... # Muestra esta ayuda"
	@echo "make mathics ................. # Ejecuta el script de Mathematica"
	@echo "make update_pip .............. # Actualiza las dependencias del proyecto de Python"
	@echo "make py ...................... # Ejecuta Python en el entorno virtual"
	@echo "make bio_enjambre ............ # Ejecuta el algoritmo de enjambre (curso bioinspirados)"
	@echo "make bio_enjambre_it ......... # Ejecuta el script iterativo"
	@echo "make bio_enjambre_it_build ... # Compila el algoritmo de enjambre y Ejecuta el script iterativo"
