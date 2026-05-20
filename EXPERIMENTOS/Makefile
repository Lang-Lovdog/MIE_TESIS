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

solutions_counter:
	. venv/bin/activate && \
		cd $(ProjectDir)  && \
		python3 SolutionsCounter.py ; \
		read -p " :: END OF PROCESS :: " a

solutions_counter_o:
	. venv/bin/activate && \
		cd $(ProjectDir)  && \
		python3 SolutionsCounter_O.py ; \
		read -p " :: END OF PROCESS :: " a

solutions_plot_o:
	. venv/bin/activate && \
		cd $(ProjectDir)  && \
		python3 PlotOriginal.py ; \
		read -p " :: END OF PROCESS :: " a

solutions_plot:
	. venv/bin/activate && \
		cd $(ProjectDir)  && \
		python3 PlotVacuaFound.py ; \
		read -p " :: END OF PROCESS :: " a

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

bio_enjambre_build:
	cd "./Tópico Selecto - Algoritmos Bioinspirados" &&\
	gcc -c pso.c  -g -Wall &&\
	gcc -c test.c -g -Wall &&\
	gcc -o exe pso.o test.o -lm -g -Wall ;\
	read -p " :: END OF PROCESS :: " a

bio_enjambre_run:
	cd "./Tópico Selecto - Algoritmos Bioinspirados" &&\
	./exe ; \
	read -p " :: END OF PROCESS :: " a



bio_genetico_build:
	cd "./Tópico Selecto - Algoritmos Bioinspirados" &&\
	gcc -c ags.c  -g -Wall &&\
	gcc -c ags_main.c -g -Wall &&\
	gcc -o ags_exe ags.o ags_main.o -lm -g -Wall ; \
	read -p " :: END OF PROCESS :: " a

bio_genetico_run:
	cd "./Tópico Selecto - Algoritmos Bioinspirados" &&\
	./ags_exe ; \
	read -p " :: END OF PROCESS :: " a


help:
	@echo "make configure ............... # Configura el entorno (bash y python venv)"
	@echo "make genetico ................ # Realiza la optimización"
	@echo "make vacua ................... # Muestra la inicialización de la función potencial"
	@echo "make test_fitness ............ # Realiza pruebas de verificación de la función de fitness sobre la función potencial a través de su definición simbólica"
	@echo "make help .................... # Muestra esta ayuda"
	@echo "make mathics ................. # Ejecuta el script de Mathematica"
	@echo "make update_pip .............. # Actualiza las dependencias del proyecto de Python"
	@echo "make py ...................... # Ejecuta Python en el entorno virtual"
	@echo "make bio_enjambre_run ........ # Ejecuta el algoritmo de enjambre (curso bioinspirados)"
	@echo "make bio_enjambre_build ...... # Compila el algoritmo de enjambre"
	@echo "make bio_genetico_run ........ # Ejecuta el algoritmo genético (curso bioinspirados)"
	@echo "make bio_genetico_build ...... # Compila el algoritmo genético"
