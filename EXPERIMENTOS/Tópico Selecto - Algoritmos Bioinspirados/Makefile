DATE=$(shell date +%Y%m%d_%H%M%S)
DATADIR=./data/

pso_ss:
	gcc -c pso.c  -g -Wall &&\
	gcc -c pso-quadsum.c  -g -Wall &&\
	gcc -o exe pso.o pso-quadsum.o -lm -g -Wall ;\
	read -p " :: END OF PROCESS :: " a

pso_r:
	gcc -c pso.c  -g -Wall &&\
	gcc -c pso-rastrigin.c  -g -Wall &&\
	gcc -o exe pso.o pso-rastrigin.o -lm -g -Wall ;\
	read -p " :: END OF PROCESS :: " a

pso_s:
	gcc -c pso.c  -g -Wall &&\
	gcc -c pso-schweffel.c  -g -Wall &&\
	gcc -o exe pso.o pso-schweffel.o -lm -g -Wall ;\
	read -p " :: END OF PROCESS :: " a

pso_fh:
	gcc -c pso.c  -g -Wall &&\
	gcc -c pso-foxhole.c  -g -Wall &&\
	gcc -o exe pso.o pso-foxhole.o -lm -g -Wall ;\
	read -p " :: END OF PROCESS :: " a

pso_run:
	./exe ; \
	read -p " :: END OF PROCESS :: " a

pso_ss_rs:
	gcc -c pso.c  -g -Wall &&\
	gcc -c pso-quadsum.c  -g -Wall &&\
	gcc -o exe pso.o pso-quadsum.o -lm -g -Wall ;\
	echo "Square_Summation" >> $(DATADIR)pso.sqaresummation.$(DATE).output.log ; \
	./exe >> $(DATADIR)pso.sqaresummation.$(DATE).output.log ; \
	 ffplay ~/.SYS_SOUND/Ding_Alert.wav -nodisp -autoexit 2>/dev/null ; \
	read -p " :: END OF PROCESS :: " a

pso_r_rs:
	gcc -c pso.c  -g -Wall &&\
	gcc -c pso-rastrigin.c  -g -Wall &&\
	gcc -o exe pso.o pso-rastrigin.o -lm -g -Wall ;\
	echo "Rastrigin" >> $(DATADIR)pso.rastrigin.$(DATE).output.log ; \
	./exe >> $(DATADIR)pso.rastrigin.$(DATE).output.log ; \
	 ffplay ~/.SYS_SOUND/Ding_Alert.wav -nodisp -autoexit 2>/dev/null ; \
	read -p " :: END OF PROCESS :: " a

pso_s_rs:
	gcc -c pso.c  -g -Wall &&\
	gcc -c pso-schweffel.c  -g -Wall &&\
	gcc -o exe pso.o pso-schweffel.o -lm -g -Wall ;\
	echo "Shweffel" >> $(DATADIR)pso.shweffel.$(DATE).output.log ; \
	./exe >> $(DATADIR)pso.shweffel.$(DATE).output.log ; \
	 ffplay ~/.SYS_SOUND/Ding_Alert.wav -nodisp -autoexit 2>/dev/null ; \
	read -p " :: END OF PROCESS :: " a

pso_fh_rs:
	gcc -c pso.c  -g -Wall &&\
	gcc -c pso-foxhole.c  -g -Wall &&\
	gcc -o exe pso.o pso-foxhole.o -lm -g -Wall ;\
	mkdir -p $(DATADIR) ; \
	echo "Fox_Hole" >> $(DATADIR)pso.foxhole.$(DATE).output.log ; \
	./exe >> $(DATADIR)pso.foxhole.$(DATE).output.log ; \
	 ffplay ~/.SYS_SOUND/Ding_Alert.wav -nodisp -autoexit 2>/dev/null ; \
	read -p " :: END OF PROCESS :: " a

pso_run:
	mkdir -p $(DATADIR) ; \
	./exe\
	read -p " :: END OF PROCESS :: " a

pso_ss_run: pso_ss pso_run

pso_r_run: pso_r pso_run

pso_s_run: pso_s pso_run

pso_fh_run: pso_fh pso_run



ags_ss:
	gcc -c ags.c  -g -Wall &&\
	gcc -c ags-quadsum.c  -g -Wall &&\
	gcc -o exe ags.o ags-quadsum.o -lm -g -Wall ;\
	read -p " :: END OF PROCESS :: " a

ags_r:
	gcc -c ags.c  -g -Wall &&\
	gcc -c ags-rastrigin.c  -g -Wall &&\
	gcc -o exe ags.o ags-rastrigin.o -lm -g -Wall ;\
	read -p " :: END OF PROCESS :: " a

ags_s:
	gcc -c ags.c  -g -Wall &&\
	gcc -c ags-schweffel.c  -g -Wall &&\
	gcc -o exe ags.o ags-schweffel.o -lm -g -Wall ;\
	read -p " :: END OF PROCESS :: " a

ags_fh:
	gcc -c ags.c  -g -Wall &&\
	gcc -c ags-foxhole.c  -g -Wall &&\
	gcc -o exe ags.o ags-foxhole.o -lm -g -Wall ;\
	read -p " :: END OF PROCESS :: " a

ags_run:
	./exe ; \
	read -p " :: END OF PROCESS :: " a

ags_ss_rs:
	gcc -c ags.c  -g -Wall &&\
	gcc -c ags-quadsum.c  -g -Wall &&\
	gcc -o exe ags.o ags-quadsum.o -lm -g -Wall ;\
	echo "Square_Summation" >> $(DATADIR)ags.$(DATE).output.log ; \
	./exe >> $(DATADIR)ags.sqaresummation.$(DATE).output.log ; \
	 ffplay ~/.SYS_SOUND/Ding_Alert.wav -nodisp -autoexit 2>/dev/null ; \
	read -p " :: END OF PROCESS :: " a

ags_r_rs:
	gcc -c ags.c  -g -Wall &&\
	gcc -c ags-rastrigin.c  -g -Wall &&\
	gcc -o exe ags.o ags-rastrigin.o -lm -g -Wall ;\
	echo "Rastrigin" >> $(DATADIR)ags.rastrigin.$(DATE).output.log ; \
	./exe >> $(DATADIR)ags.$(DATE).output.log ; \
	 ffplay ~/.SYS_SOUND/Ding_Alert.wav -nodisp -autoexit 2>/dev/null ; \
	read -p " :: END OF PROCESS :: " a

ags_s_rs:
	gcc -c ags.c  -g -Wall &&\
	gcc -c ags-schweffel.c  -g -Wall &&\
	gcc -o exe ags.o ags-schweffel.o -lm -g -Wall ;\
	echo "Shweffel" >> $(DATADIR)ags.shweffel.$(DATE).output.log ; \
	./exe >> $(DATADIR)ags.$(DATE).output.log ; \
	 ffplay ~/.SYS_SOUND/Ding_Alert.wav -nodisp -autoexit 2>/dev/null ; \
	read -p " :: END OF PROCESS :: " a

ags_fh_rs:
	gcc -c ags.c  -g -Wall &&\
	gcc -c ags-foxhole.c  -g -Wall &&\
	gcc -o exe ags.o ags-foxhole.o -lm -g -Wall ;\
	mkdir -p $(DATADIR) ; \
	echo "Fox_Hole" >> $(DATADIR)ags.foxhole.$(DATE).output.log ; \
	./exe >> $(DATADIR)ags.$(DATE).output.log ; \
	 ffplay ~/.SYS_SOUND/Ding_Alert.wav -nodisp -autoexit 2>/dev/null ;\
	read -p " :: END OF PROCESS :: " a

ags_run:
	mkdir -p $(DATADIR) ; \
	./exe\
	read -p " :: END OF PROCESS :: " a

ags_ss_run: ags_ss ags_run

ags_r_run: ags_r ags_run

ags_s_run: ags_s ags_run

ags_fh_run: ags_fh ags_run

