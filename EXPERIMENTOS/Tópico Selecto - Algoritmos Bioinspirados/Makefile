DATE=`date +%Y%m%d_%H%M%S`

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

pso_ss_run: pso_ss pso_run

pso_r_run: pso_r pso_run

pso_s_run: pso_s pso_run

pso_fh_run: pso_fh pso_run

pso_run_save:
	./exe > pso.$(DATE).output.log ; \
	read -p " :: END OF PROCESS :: " a

pso_ss_run_save: pso_ss pso_run_save

pso_r_run_save: pso_r pso_run_save

pso_s_run_save: pso_s pso_run_save

pso_fh_run_save: pso_fh pso_run_save

