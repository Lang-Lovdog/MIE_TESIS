#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "pso.h"
#include "test.h"

lovdog_log_setup;

extern FitnessFunction FuncionObjetivo;

void parse_opts(int argc, char *argv[], TuningVars *tuning_vars){
  unsigned char i=0;
  while(i<argc){
    if(!strcmp(argv[i],"-k")) tuning_vars->constriccion=atof(argv[++i]);
    if(!strcmp(argv[i],"-c1")) tuning_vars->c1=atof(argv[++i]);
    if(!strcmp(argv[i],"-c2")) tuning_vars->c2=atof(argv[++i]);
    if(!strcmp(argv[i],"-i")) tuning_vars->max_iter=atoi(argv[++i]);
    if(!strcmp(argv[i],"-p")) tuning_vars->cant_part=atoi(argv[++i]);
    if(!strcmp(argv[i],"-d")) tuning_vars->cant_dim=atoi(argv[++i]);
    if(!strcmp(argv[i],"-e")) tuning_vars->execution_times=atoi(argv[++i]);
    ++i;
  }
}

void initialize_options(TuningVars *tuning_vars){
  tuning_vars->constriccion=0.005;
  tuning_vars->c1=0.01;
  tuning_vars->c2=0.02;
  tuning_vars->max_iter=300;
  tuning_vars->cant_part=60;
  tuning_vars->cant_dim=10;
  tuning_vars->execution_times=100;
}

void help(void){
  printf("pso [-c constriccion] [-c1 c1] [-c2 c2] [-i max_iter] [-p cant_part] [-d cant_dim]");
}

long double promedio=0;
FILE* Data;

int main (int argc, char *argv[]) {

  lovdog_log = 0b0110;
  const char* datafile = "pso_square_summation.dat";
  const char* title = "Square Summation";
  const char* xlabel = ".";
  const char* ylabel = "Fitness";
  const char* outfile = "pso_square_summation.png";

  //help();
  //printf("\n");
  TuningVars tv;
  initialize_options(&tv);
  parse_opts(argc,argv,&tv);
  const long double
    LimSup[10] = { 20, 20, 20, 20, 20, 20, 20, 20, 20, 20 },
    LimInf[10] = {-20,-20,-20,-20,-20,-20,-20,-20,-20,-20 }
  ;
  float step=100.00/tv.execution_times;
  long double c1c2[10]={0.02, 0.021, 0.022, 0.023, 0.024, 0.025, 0.026, 0.027, 0.028, 0.029};
  for(int k=0; k<10; ++k) for(int l=0; l<10; ++l){
    unsigned int i=0;
    Data=fopen(datafile, "wt");
    while(i<tv.execution_times){
      ProcesoPSO(
          tv.cant_part,    // Cantidad de Particulas
          tv.cant_dim,     // Cantidad de Dimensiones
          LimSup,
          LimInf,
          tv.max_iter,     // Cantidad de Iteraciones
          tv.constriccion, // Factor de constriccion
          tv.c1=c1c2[k],           // Peso C1
          tv.c2=c1c2[l],           // Peso C2
          NULL
          );
      descansa();
      printf(":: %04.4f%%\r", step*i);
      fflush(stdout);
      ++i;
    }
    fclose(Data);
    printf("Promedio con c1 = %Lf, c2 = %Lf: %Lf\n", c1c2[k], c1c2[l], promedio/tv.execution_times);
    char command[256];
    printf("%s\n\n", command);
    snprintf(command, sizeof(command), "./boxplot.sh %s '%s' '%s' '%s' '%03d-%s'", datafile, title, xlabel, ylabel, k+l*10, outfile);
    system(command);
    promedio=0;
  }
  return 0;
}

static long double SquareSummation(
    long double          *x,
    unsigned int          __CantidadDeParametros__,
    const long double    *__ParametrosDeOperacion__
){
  long double fit =
    1000
    - powl(x[0]+7.0,2)
    - powl(x[1]+3.0,2)
    - powl(x[2]-3.0,2)
    - powl(x[3]-5.0,2)
    - powl(x[4]+2.5,2)
    - powl(x[5]-10 ,2)
    - powl(x[6]-15 ,2)
    - powl(x[7]+10,2)
    - powl(x[8]+15,2)
    - powl(x[9]-0.5,2);
  return fit;
}

PARTICULA ProcesoPSO(
    const long double        __NumeroDeParticulas__,
    const long double        __Dimension__,
    const long double       *__LimiteSuperior__,
    const long double       *__LimiteInferior__,
    const unsigned int       __NumeroMaximoDeIteraciones__,
    const long double        __Factor_Constriccion_Inercia__,
    const long double        __ValorPesoPersonalC1__,
    const long double        __ValorPesoGlobalC2__,
    const long double       *__ParametrosDeOperacion__
){
  ENJAMBRE *enjambre;
  FuncionObjetivo=&SquareSummation;
  enjambre=CrearEnjambre(__NumeroDeParticulas__, __Dimension__);
  InicializarEnjambre(
      enjambre,
      __Factor_Constriccion_Inercia__,
      __Factor_Constriccion_Inercia__,
      __ValorPesoPersonalC1__,
      __ValorPesoGlobalC2__,
      __NumeroMaximoDeIteraciones__,
      __LimiteInferior__,
      __LimiteSuperior__
  );
  uint *HistogramBestId = (uint*)malloc(sizeof(uint) * __NumeroDeParticulas__);
  uint prev_bestid=__NumeroDeParticulas__;
  uint n=0; while(n<__NumeroDeParticulas__) HistogramBestId[n++]=0;
  lovdog_log =       0b00000;
  EvaluacionInicialEnjambreMax(enjambre, __ParametrosDeOperacion__);
  lovdog_startlog
  printf("\n ===== Inicialización ======\n");
  ImprimeEnjambre(enjambre);
  lovdog_endlog
  n=0; while(n<__NumeroMaximoDeIteraciones__){
    ActualizarVelocidadClamping(enjambre);
    ActualizarPosicion(enjambre);
    EvaluarEnjambreMax(enjambre, __ParametrosDeOperacion__);
    ActualizarMejoresPosicionesMax(enjambre);
    //if(prev_bestid!=enjambre->MejorParticulaDelGrupo){
    //  prev_bestid=enjambre->MejorParticulaDelGrupo;
    //  printf("@ %4u: ", prev_bestid);
    //  ImprimeParticulaID(enjambre,enjambre->MejorParticulaDelGrupo);
    //  printf("\n");
    //}
    lovdog_startlog
      printf("\n ===== Iteración %u ======\n",n);
      ImprimeEnjambre(enjambre);
      printf("\n");
    lovdog_endlog
    lovdog_startverb(0b00001)
      //printf("\n ===== Iteración %u ======\n",n);
      //printf("@ Mejor Partícula : %4d\n", enjambre->MejorParticulaDelGrupo);
      HistogramBestId[enjambre->MejorParticulaDelGrupo]++;
    lovdog_endverb
    ++n;
  }
  lovdog_startverb(0b00001)
    // Print histogram
    n=0; while(n<__NumeroDeParticulas__){
      if(HistogramBestId[n])
        printf("%4u: %4u %c\n", n,HistogramBestId[n], n==enjambre->MejorParticulaDelGrupo ? '*' : ' ');
      ++n;
    }
  lovdog_endverb
  free(HistogramBestId);
  //printf("@ Mejor Partícula : \n{");
  //ImprimeParticulaID(enjambre, enjambre->MejorParticulaDelGrupo);
  //printf("\n}\n");
  promedio+=enjambre->Part[enjambre->MejorParticulaDelGrupo].Xfit;
  fprintf(Data,"%04Lf\n",enjambre->Part[enjambre->MejorParticulaDelGrupo].Xfit);
  PARTICULA p_best;
  EliminarEnjambre(enjambre);
  return p_best;
}


