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

// Proyecto 01

void initialize_options(TuningVars *tuning_vars){
  tuning_vars->constriccion=0.9;
  tuning_vars->c1=2.0;
  tuning_vars->c2=2.0;
  tuning_vars->max_iter=300;
  tuning_vars->cant_part=60;
  tuning_vars->cant_dim=2;
  tuning_vars->execution_times=100;
}

// Proyecto 02
/*
void initialize_options(TuningVars *tuning_vars){
  tuning_vars->constriccion=0.6;
  tuning_vars->c1=0.02;
  tuning_vars->c2=0.02;
  tuning_vars->max_iter=300;
  tuning_vars->cant_part=60;
  tuning_vars->cant_dim=10;
  tuning_vars->execution_times=100;
}*/

// Proyecto 03
/*
void initialize_options(TuningVars *tuning_vars){
  tuning_vars->constriccion=0.005;
  tuning_vars->c1=0.02;
  tuning_vars->c2=0.02;
  tuning_vars->max_iter=300;
  tuning_vars->cant_part=60;
  tuning_vars->cant_dim=10;
  tuning_vars->execution_times=100;
}*/

void help(void){
  printf("pso [-c constriccion] [-c1 c1] [-c2 c2] [-i max_iter] [-p cant_part] [-d cant_dim]");
}

int main (int argc, char *argv[]) {

  lovdog_log = 0b0110;
  lovdog_log =       0b100000;

  //help();
  //printf("\n");
  TuningVars tv;
  initialize_options(&tv);
  parse_opts(argc,argv,&tv);
  const long double
    LimSup[2] = { 65.536, 65.536 },
    LimInf[2] = {-65.536,-65.536 }
  ;
  unsigned int i=0;
  while(i<tv.execution_times){
  ProcesoPSO(
     tv.cant_part,    // Cantidad de Particulas
     tv.cant_dim,     // Cantidad de Dimensiones
     LimSup,
     LimInf,
     tv.max_iter,     // Cantidad de Iteraciones
     tv.constriccion, // Factor de constriccion
     tv.c1,           // Peso C1
     tv.c2,           // Peso C2
      NULL);
    descansa();
  ++i;
  }
  return 0;
}

long double FoxHole(
    long double          *Xi,
    unsigned int          Dimension,
    const long double    *__ParametrosDeOperacion__

){
  long double fit,aux1,aux2;
  int a[2][25]=
  {{-32,-16,  0, 16, 32,-32,-16,  0, 16, 32,-32,-16,  0, 16, 32,-32,-16,  0, 16, 32,-32,-16,  0, 16, 32},
   {-32,-32,-32,-32,-32,-16,-16,-16,-16,-16,  0,  0,  0,  0,  0, 16, 16, 16, 16, 16, 32, 32, 32, 32, 32}};
   int i,j;
   aux1=0;
   for(j=0; j<25; j++){
     for(i=0,aux2=0; i<2; i++) aux2+=powl(Xi[i]-a[i][j],6);
     aux1+=(1.0/((j+1)+aux2));
  }
   fit=1/((0.002)+aux1);
   return (-1.0*fit);
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
  FuncionObjetivo=&FoxHole;
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
  EvaluacionInicialEnjambreMax(enjambre, __ParametrosDeOperacion__);
  lovdog_startlog
  printf("\n ===== Inicialización ======\n");
  ImprimeEnjambre(enjambre);
  lovdog_endlog
  uint n=0; while(n<__NumeroMaximoDeIteraciones__){
    ActualizarVelocidadClamping(enjambre);
    //ActualizarVelocidadInerciaW(enjambre);
    ActualizarPosicion(enjambre);
    EvaluarEnjambreMax(enjambre, __ParametrosDeOperacion__);
    ActualizarMejoresPosicionesMax(enjambre);
    lovdog_startlog
      printf("\n ===== Iteración %u ======\n",n);
      ImprimeEnjambre(enjambre);
      printf("\n");
    lovdog_endlog
    lovdog_startverb(0b10000)
      printf("\n ===== Iteración %u ======\n",n);
      printf("@ Mejor Partícula : %4d\n", enjambre->MejorParticulaDelGrupo);
    lovdog_endverb
    ++n;
  }
  lovdog_startverb(0b1000000)
    printf("@ Mejor Partícula : \n{");
    ImprimeParticulaID(enjambre, enjambre->MejorParticulaDelGrupo);
    printf("\n}\n");
  lovdog_endverb
  lovdog_startverb(0b100000)
    printf("%Lf\n",enjambre->Part[enjambre->MejorParticulaDelGrupo].Xfit);
  lovdog_endverb
  EliminarEnjambre(enjambre);
  PARTICULA p_best;
  return p_best;
}

