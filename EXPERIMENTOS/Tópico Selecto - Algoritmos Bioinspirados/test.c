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

/*void initialize_options(TuningVars *tuning_vars){
  tuning_vars->constriccion=0.005;
  tuning_vars->c1=2.0;
  tuning_vars->c2=2.0;
  tuning_vars->max_iter=300;
  tuning_vars->cant_part=60;
  tuning_vars->cant_dim=10;
  tuning_vars->execution_times=1;
} 
// Goods for SquareSummation*/

/*
void initialize_options(TuningVars *tuning_vars){
  tuning_vars->constriccion=0.01;
  tuning_vars->c1=2.0;
  tuning_vars->c2=2.0;
  tuning_vars->max_iter=300;
  tuning_vars->cant_part=60;
  tuning_vars->cant_dim=2;
  tuning_vars->execution_times=1;
}*/


void initialize_options(TuningVars *tuning_vars){
  tuning_vars->constriccion=0.9;
  tuning_vars->c1=2.0;
  tuning_vars->c2=2.0;
  tuning_vars->max_iter=300;
  tuning_vars->cant_part=60;
  tuning_vars->cant_dim=2;
  tuning_vars->execution_times=12;
}

void help(void){
  printf("pso [-c constriccion] [-c1 c1] [-c2 c2] [-i max_iter] [-p cant_part] [-d cant_dim]");
}

int main (int argc, char *argv[]) {

  lovdog_log = 0b0110;

  help();
  printf("\n");
  TuningVars tv;
  initialize_options(&tv);
  parse_opts(argc,argv,&tv);
  const long double
//    LimSup[10] = { 20, 20, 20, 20, 20, 20, 20, 20 },
//    LimInf[10] = {-20,-20,-20,-20,-20,-20,-20,-20 }
    LimSup[2] = { 500, 500 },
    LimInf[2] = {-500,-500 }
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

static long double SquareSummation(
    long double          *x,
    unsigned int          __CantidadDeParametros__,
    const long double    *__ParametrosDeOperacion__
){
  //long double fit = 150 - powl(x[0]-2.0,2) - powl(x[1]-3.0,2);
  //long double fit = 1000 - powl(x[0]-2.0,2) - powl(x[1]-3.0,2);
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

static long double Schwefel(
    long double          *x,
    unsigned int          __CantidadDeParametros__,
    const long double    *__ParametrosDeOperacion__
){
  long double fitness_val=0;
  uint n=0; while(n<__CantidadDeParametros__){
    if(x[n]>=-500 && x[n]<=500) fitness_val+=0.02*x[n]*x[n];
    else fitness_val += -x[n]*sinl(sqrtl(fabsl(x[n])));
    ++n;
  }
  fitness_val += (__CantidadDeParametros__)*418.9829;
  return fitness_val;
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
  InicializarEnjambre(enjambre, __Factor_Constriccion_Inercia__, __Factor_Constriccion_Inercia__, __ValorPesoPersonalC1__, __ValorPesoGlobalC2__, __NumeroMaximoDeIteraciones__, __LimiteInferior__, __LimiteSuperior__);
  EvaluacionInicialEnjambreMin(enjambre, __ParametrosDeOperacion__);
  lovdog_startlog
  printf("\n ===== Inicialización ======\n");
  ImprimeEnjambre(enjambre);
  lovdog_endlog
  unsigned int n=0; while(n<__NumeroMaximoDeIteraciones__){
    //ActualizarVelocidad(enjambre);
    //ActualizarVelocidadClamping(enjambre);
    ActualizarVelocidadInerciaW(enjambre);
    ActualizarPosicion(enjambre);
    EvaluarEnjambreMin(enjambre, __ParametrosDeOperacion__);
    ActualizarMejoresPosicionesMin(enjambre);
    lovdog_startlog
    printf("\n ===== Iteración %u ======\n",n);
    ImprimeEnjambre(enjambre);
    printf("\n");
    lovdog_endlog
    ++n;
  }
  printf("@ Mejor Partícula : \n{");
  ImprimeParticulaID(enjambre, enjambre->MejorParticulaDelGrupo);
  printf("\n}\n");
  EliminarEnjambre(enjambre);
  PARTICULA p_best;
  return p_best;
}
