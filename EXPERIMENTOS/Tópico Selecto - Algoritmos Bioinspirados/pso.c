#include "pso.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <string.h>


FitnessFunction FuncionObjetivo;
lovdog_log_var  lovdog_log;

void lovdog_log_level(lovdog_log_var vl) { lovdog_log = vl; }

// Definición d'as funciones

ENJAMBRE* CrearEnjambre(
    //ENJAMBRE* __Enjambre__,
    unsigned int __CantidadDeParticulas__,
    unsigned int __CantidadDeParametros__
  ){
  time_t t;
  srand(time(&t));
  ENJAMBRE *ptr=NULL;
  //Reservar la memoria para la estructura del enjambre
  ptr=(ENJAMBRE *)malloc(sizeof(ENJAMBRE));
  if(!ptr){
    printf("Error al reservar la memoria para la estructura ENJAMBRE.");
    exit(0);
  }
  ptr->CantidadDeParticulas=__CantidadDeParticulas__;
  ptr->CantidadDeDimensiones=__CantidadDeParametros__;

  //Reservar la memoria para N particulas de M parametros
  ptr->Part=NULL;
  ptr->Part=(PARTICULA *)malloc(__CantidadDeParticulas__*sizeof(PARTICULA));
  if(ptr->Part==NULL){
    printf("Error al reservar la memoria para las Particulas.");
    exit(0);
  }
  //Reservar memoria para los 3 vectores de cada Particula
  for(unsigned int i=0; i<__CantidadDeParticulas__; ++i){
    ptr->Part[i].Xi=(long double *)malloc(__CantidadDeParametros__*sizeof(long double));
    ptr->Part[i].Vi=(long double *)malloc(__CantidadDeParametros__*sizeof(long double));
    ptr->Part[i].Pi=(long double *)malloc(__CantidadDeParametros__*sizeof(long double));
  }
  return ptr;
}


void InicializarEnjambre(
    ENJAMBRE          *__Enjambre__,
    long double        __FactorConstriccion__,
    long double        __PesoDeInercia__,
    long double        __ValorDePeso_C1__,
    long double        __ValorDePeso_C2__,
    unsigned int       __MaximoDeIteraciones__,
    const long double *__LimitesInferiores__,
    const long double *__LimitesSuperiores__
){
  if(__Enjambre__){
  long double aux,rango;
  __Enjambre__->K                      = __FactorConstriccion__;
  __Enjambre__->W                      = __PesoDeInercia__;
  __Enjambre__->C1                     = __ValorDePeso_C1__;
  __Enjambre__->C2                     = __ValorDePeso_C2__;
  __Enjambre__->MaximoDeIteraciones    = __MaximoDeIteraciones__;
  __Enjambre__->MejorParticulaDelGrupo = 0;
  __Enjambre__->LimitesInferiores      = __LimitesInferiores__;
  __Enjambre__->LimitesSuperiores      = __LimitesSuperiores__;
  //Dar constriccion uwu
  long double fi = __Enjambre__->C1+__Enjambre__->C2;
  __Enjambre__->Constriccion=2/fabsl(2-fi-sqrtl(powl(fi,2)-(4*fi)));
  lovdog_startverb(0b0010)
  printf("%Lf\n",fi);
  printf("%Lf\n",powl(fi,2)-(4*fi));
  printf("%Lf\n",sqrtl(powl(fi,2)-(4*fi)));
  printf("%Lf\n",fabsl(2-fi-sqrtl(powl(fi,2)-(4*fi))));
  printf("%Lf\n\n",__Enjambre__->Constriccion);
  lovdog_endverb
  lovdog_startverb(0b0100)
  printf("Características del Enjambre:{\n"
         "\tParticulas: %u\n"
         "\tDimensiones: %u\n"
         "\tK: %Lf\n"
         "\tW: %Lf\n"
         "\tC1: %Lf\n"
         "\tC2: %Lf\n"
         "\tConstriccion: %Lf\n"
         "\tMaximoDeIteraciones: %u\n"
         ,__Enjambre__->CantidadDeParticulas
         ,__Enjambre__->CantidadDeDimensiones
         ,__Enjambre__->K
         ,__Enjambre__->W
         ,__Enjambre__->C1
         ,__Enjambre__->C2
         ,__Enjambre__->Constriccion
         ,__Enjambre__->MaximoDeIteraciones);
  printf("\tLimites Inferiores: [");
  for(unsigned int i=0; i<__Enjambre__->CantidadDeDimensiones; ++i)
    printf("%Lf, ",__Enjambre__->LimitesInferiores[i]);
  printf("]\n");
  printf("\tLimites Superiores: [");
  for(unsigned int i=0; i<__Enjambre__->CantidadDeDimensiones; ++i)
    printf("%Lf, ",__Enjambre__->LimitesSuperiores[i]);
  printf("]\n");
  printf("}\n\n");
  lovdog_endlog
  //Inicializar cada vector de cada particula
  for(unsigned int i=0; i<__Enjambre__->CantidadDeParticulas; ++i) //Para cada particula i
    for(unsigned int j=0; j<__Enjambre__->CantidadDeDimensiones; ++j) //Para cada parametro j de cada vector de la particula i
    { rango=__Enjambre__->LimitesSuperiores[j]-__Enjambre__->LimitesInferiores[j];
      aux= ((long double)rand()/(long double)RAND_MAX) * rango + __Enjambre__->LimitesInferiores[j];
      __Enjambre__->Part[i].Xi[j]=aux;
      __Enjambre__->Part[i].Vi[j]=0;
      __Enjambre__->Part[i].Pi[j]=aux;
    }
  }
}


void EliminarEnjambre(ENJAMBRE* __Enjambre__)
{ //Liberar la memoria para de los 3 vectores de cada Particula
  for(unsigned int i=0; i<__Enjambre__->CantidadDeParticulas; ++i)
     { free(__Enjambre__->Part[i].Xi);
       free(__Enjambre__->Part[i].Vi);
       free(__Enjambre__->Part[i].Pi);
     }
  //Liberar la memoria de las estructuras particula
  free(__Enjambre__->Part);
  //Liberar la memoria de la estrcutura del enajmbre
  free(__Enjambre__);
}


void ImprimeParticulaID(ENJAMBRE *__Enjambre__, unsigned int __ID_Particula__){
  printf("\nP%i,Xi: ",__ID_Particula__);
  for(unsigned int i=0; i<__Enjambre__->CantidadDeDimensiones; i++)
    printf("%Lf, ",__Enjambre__->Part[__ID_Particula__].Xi[i]);
  printf("\nP%i,Vi: ",__ID_Particula__);
  for(unsigned int i=0; i<__Enjambre__->CantidadDeDimensiones; i++)
    printf("%Lf, ",__Enjambre__->Part[__ID_Particula__].Vi[i]);
  printf("\nP%i,Pi: ",__ID_Particula__);
  for(unsigned int i=0; i<__Enjambre__->CantidadDeDimensiones; i++)
    printf("%Lf, ",__Enjambre__->Part[__ID_Particula__].Pi[i]);
  printf("\nP%i,Xfit=%Lf",__ID_Particula__,__Enjambre__->Part[__ID_Particula__].Xfit);
  printf("\nP%i,Pfit=%Lf",__ID_Particula__,__Enjambre__->Part[__ID_Particula__].Pfit);
}

void ImprimeParticula(
  const PARTICULA    *__Particula__,
  const unsigned int  __CantidadDeParametros__
){
  printf("\nParticula:");
  for(unsigned int i=0; i<__CantidadDeParametros__; i++)
    printf("%Lf, ",__Particula__->Xi[i]);
  printf("\nParticula Vi: ");
  for(unsigned int i=0; i<__CantidadDeParametros__; i++)
    printf("%Lf, ",__Particula__->Vi[i]);
  printf("\nParticula,Pi: ");
  for(unsigned int i=0; i<__CantidadDeParametros__; i++)
    printf("%Lf, ",__Particula__->Pi[i]);
  printf("\nParticula,Xfit=%Lf",__Particula__->Xfit);
  printf("\nParticula,Pfit=%Lf",__Particula__->Pfit);
}

void CopiaParticula(
    PARTICULA* __Destino__,
    PARTICULA* __Origen__,
    const unsigned int     __CantidadDeParametros__
){
  if(!__Destino__ || !__Origen__) return;
  if(!__Destino__->Xi || !__Destino__->Vi || !__Destino__->Pi) return;
  memcpy(__Destino__->Xi, __Origen__->Xi, __CantidadDeParametros__*sizeof(long double));
  memcpy(__Destino__->Vi, __Origen__->Vi, __CantidadDeParametros__*sizeof(long double));
  memcpy(__Destino__->Pi, __Origen__->Pi, __CantidadDeParametros__*sizeof(long double));
  __Destino__->Xfit =  __Origen__->Xfit;
  __Destino__->Pfit =  __Origen__->Pfit;
}

void ImprimeEnjambre(ENJAMBRE *__Enjambre__) {
  for(unsigned int i=0; i<__Enjambre__->CantidadDeParticulas; ++i) //Para cada particula i
    ImprimeParticulaID(__Enjambre__,i);
}


void EvaluarEnjambreMin(ENJAMBRE *__Enjambre__,const long double* __ParametrosDeOperacion__){
  long double BestFit;
  // Calcular el valor de Fitness de cada particula
  BestFit = (*FuncionObjetivo)(
      __Enjambre__->Part[0].Xi,
      __Enjambre__->CantidadDeDimensiones,
      __ParametrosDeOperacion__
    );
  for(unsigned int i=0; i<__Enjambre__->CantidadDeParticulas; i++){
    __Enjambre__->Part[i].Xfit = (*FuncionObjetivo)(
        __Enjambre__->Part[i].Xi,
        __Enjambre__->CantidadDeDimensiones,
        __ParametrosDeOperacion__
      );
    // Almacena el indice de la mejor particula de todo en enjambre
    if(__Enjambre__->Part[i].Xfit<BestFit){
      BestFit = __Enjambre__->Part[i].Xfit;
      __Enjambre__->MejorParticulaDelGrupo =i;
    }
  }
}

void EvaluarEnjambreMax(ENJAMBRE *__Enjambre__,const long double* __ParametrosDeOperacion__){
  long double BestFit;
  // Calcular el valor de Fitness de cada particula
  BestFit = (*FuncionObjetivo)(
      __Enjambre__->Part[0].Xi,
      __Enjambre__->CantidadDeDimensiones,
      __ParametrosDeOperacion__
    );
  for(unsigned int i=0; i<__Enjambre__->CantidadDeParticulas; i++){
    __Enjambre__->Part[i].Xfit = (*FuncionObjetivo)(
        __Enjambre__->Part[i].Xi,
        __Enjambre__->CantidadDeDimensiones,
        __ParametrosDeOperacion__
      );
    // Almacena el indice de la mejor particula de todo en enjambre
    if(__Enjambre__->Part[i].Xfit>BestFit){
      BestFit = __Enjambre__->Part[i].Xfit;
      __Enjambre__->MejorParticulaDelGrupo =i;
    }
  }
}


void EvaluacionInicialEnjambreMin(ENJAMBRE *__Enjambre__,const long double* __ParametrosDeOperacion__){
  if(__Enjambre__){
  long double aux,BestFit;
  //Calcular el valor de fitness de cada Particula
  BestFit=(*FuncionObjetivo)(
      __Enjambre__->Part[0].Xi,
      __Enjambre__->CantidadDeDimensiones,
      __ParametrosDeOperacion__
    );
  for(unsigned int i=0; i<__Enjambre__->CantidadDeParticulas; i++){
    aux=(*FuncionObjetivo)(
        __Enjambre__->Part[i].Xi,
        __Enjambre__->CantidadDeDimensiones,
        __ParametrosDeOperacion__
      );
    __Enjambre__->Part[i].Xfit=aux;
    __Enjambre__->Part[i].Pfit=aux;
    //Almacena el indice de la mejor particula de todo el enjambre
    if(aux<BestFit){
      BestFit=aux;
      __Enjambre__->MejorParticulaDelGrupo=i;
    }
  }
  }
}

void EvaluacionInicialEnjambreMax(ENJAMBRE *__Enjambre__,const long double* __ParametrosDeOperacion__){
  if(__Enjambre__){
  long double aux,BestFit;
  //Calcular el valor de fitness de cada Particula
  BestFit=(*FuncionObjetivo)(
      __Enjambre__->Part[0].Xi,
      __Enjambre__->CantidadDeDimensiones,
      __ParametrosDeOperacion__
    );
  for(unsigned int i=0; i<__Enjambre__->CantidadDeParticulas; i++){
    aux=(*FuncionObjetivo)(
        __Enjambre__->Part[i].Xi,
        __Enjambre__->CantidadDeDimensiones,
        __ParametrosDeOperacion__
      );
    __Enjambre__->Part[i].Xfit=aux;
    __Enjambre__->Part[i].Pfit=aux;
    //Almacena el indice de la mejor particula de todo el enjambre
    if(aux>BestFit){
      BestFit=aux;
      __Enjambre__->MejorParticulaDelGrupo=i;
    }
  }
  }
}


void ActualizarVelocidad(ENJAMBRE *__Enjambre__){
  long double Y1,Y2;
  //Actualizar cada vector velocidad Vi de cada particula
  for(unsigned int i=0; i<__Enjambre__->CantidadDeParticulas; i++) //Para cada particula i
    for(unsigned int j=0; j<__Enjambre__->CantidadDeDimensiones; j++) //Para cada parametro j de cada vector Vi de la particula i
    {
      Y1=rand()/(long double)RAND_MAX;
      Y2=rand()/(long double)RAND_MAX;
      __Enjambre__->Part[i].Vi[j] =(
        __Enjambre__->Part[i].Vi[j]+
        (__Enjambre__->C1*Y1*(__Enjambre__->Part[i].Pi[j]-__Enjambre__->Part[i].Xi[j]))+
        (__Enjambre__->C2*Y2*(__Enjambre__->Part[__Enjambre__->MejorParticulaDelGrupo].Pi[j]-__Enjambre__->Part[i].Xi[j]))
      );
    }
}

void ActualizarVelocidadInerciaW(ENJAMBRE *__Enjambre__){
  long double Y1,Y2;
  //Actualizar cada vector velocidad Vi de cada particula
  for(unsigned int i=0; i<__Enjambre__->CantidadDeParticulas; i++) //Para cada particula i
    for(unsigned int j=0; j<__Enjambre__->CantidadDeDimensiones; j++) //Para cada parametro j de cada vector Vi de la particula i
    {
      Y1=rand()/(long double)RAND_MAX;
      Y2=rand()/(long double)RAND_MAX;
      __Enjambre__->Part[i].Vi[j] =(
        (__Enjambre__->Part[i].Vi[j]*__Enjambre__->W)+
        (__Enjambre__->C1*Y1*(__Enjambre__->Part[i].Pi[j]-__Enjambre__->Part[i].Xi[j]))+
        (__Enjambre__->C2*Y2*(__Enjambre__->Part[__Enjambre__->MejorParticulaDelGrupo].Pi[j]-__Enjambre__->Part[i].Xi[j]))
      );
    }
}

void ActualizarVelocidadClamping(ENJAMBRE *__Enjambre__){
  long double Y1,Y2;
  long double vMax;
  //Actualizar cada vector velocidad Vi de cada particula
  for(unsigned int i=0; i<__Enjambre__->CantidadDeParticulas; i++) //Para cada particula i
    for(unsigned int j=0; j<__Enjambre__->CantidadDeDimensiones; j++) //Para cada parametro j de cada vector Vi de la particula i
    {
      vMax = __Enjambre__->K*((__Enjambre__->LimitesSuperiores[j] - __Enjambre__->LimitesInferiores[j])/2);
      Y1=(rand()%RAND_MAX)/(long double)RAND_MAX;
      Y2=(rand()%RAND_MAX)/(long double)RAND_MAX;
      lovdog_startverb(0b0010)
      printf("Y1=%Lf\t Y2=%Lf\n"
             "C1=%Lf\t C2=%Lf\n"
             "Vi=%Lf\t Pi=%Lf\t Xi=%Lf\t Pig=%Lf\n"
             ,Y1,Y2
             ,__Enjambre__->C1,__Enjambre__->C2
             ,__Enjambre__->Part[i].Vi[j]
             ,__Enjambre__->Part[i].Pi[j]
             ,__Enjambre__->Part[i].Xi[j]
             ,__Enjambre__->Part[__Enjambre__->MejorParticulaDelGrupo].Pi[j]);
      lovdog_endverb
      __Enjambre__->Part[i].Vi[j] =(
          (__Enjambre__->Part[i].Vi[j]*__Enjambre__->K)+
          (__Enjambre__->C1*Y1*(__Enjambre__->Part[i].Pi[j]-__Enjambre__->Part[i].Xi[j]))+
          (__Enjambre__->C2*Y2*(__Enjambre__->Part[__Enjambre__->MejorParticulaDelGrupo].Pi[j]-__Enjambre__->Part[i].Xi[j]))
      );
      //printf("vMax=%Lf\t Vi=%Lf\n",vMax, __Enjambre__->Part[i].Vi[j]);
      if(__Enjambre__->Part[i].Vi[j] > vMax)
         __Enjambre__->Part[i].Vi[j]  =vMax;
      if(__Enjambre__->Part[i].Vi[j] > vMax)
         __Enjambre__->Part[i].Vi[j] = vMax;
    }
}


void ActualizarVelocidadConstriction(
    ENJAMBRE *__Enjambre__
){
  long double Y1,Y2;
  //Actualizar cada vector velocidad Vi de cada particula
  for(unsigned int i=0; i<__Enjambre__->CantidadDeParticulas; i++) //Para cada particula i
    for(unsigned int j=0; j<__Enjambre__->CantidadDeDimensiones; j++) //Para cada parametro j de cada vector Vi de la particula i
    {
      Y1=rand()/(long double)RAND_MAX;
      Y2=rand()/(long double)RAND_MAX;
      //printf("Y1=%Lf Y2=%Lf",Y1,Y2);
      __Enjambre__->Part[i].Vi[j] =__Enjambre__->Constriccion*(
        (__Enjambre__->Part[i].Vi[j]+
        (__Enjambre__->C1*Y1*(__Enjambre__->Part[i].Pi[j]-__Enjambre__->Part[i].Xi[j]))+
        (__Enjambre__->C2*Y2*(__Enjambre__->Part[__Enjambre__->MejorParticulaDelGrupo].Pi[j]-__Enjambre__->Part[i].Xi[j]))
      ));
      //printf(" Vt+1= %Lf",__Enjambre__->Part[i].Vi[j]);
    }
}

void ActualizarPosicion(ENJAMBRE *__Enjambre__){
  // Acutailzsr cada vector Posicion XI de cada particula
  for(unsigned int i=0; i<__Enjambre__->CantidadDeParticulas; i++) //Para cada particula i
    for(unsigned int j=0; j<__Enjambre__->CantidadDeDimensiones; j++) //Para cada parametro j de cada vector de la particula i
      __Enjambre__->Part[i].Xi[j] += __Enjambre__->Part[i].Vi[j];
}

void ActualizarMejoresPosicionesMin(ENJAMBRE *__Enjambre__){
  for(unsigned int i=0; i<__Enjambre__->CantidadDeParticulas; i++)
    if(__Enjambre__->Part[i].Xfit < __Enjambre__->Part[i].Pfit){
      __Enjambre__->Part[i].Pfit = __Enjambre__->Part[i].Xfit;
      for(unsigned int j=0; j<__Enjambre__->CantidadDeDimensiones; j++) //Para cada parametro j de cada vector de la particula i
        __Enjambre__->Part[i].Pi[j] = __Enjambre__->Part[i].Xi[j];
    }
}

void ActualizarMejoresPosicionesMax(ENJAMBRE *__Enjambre__){
  for(unsigned int i=0; i<__Enjambre__->CantidadDeParticulas; i++)
    if(__Enjambre__->Part[i].Xfit > __Enjambre__->Part[i].Pfit){
      __Enjambre__->Part[i].Pfit = __Enjambre__->Part[i].Xfit;
      for(unsigned int j=0; j<__Enjambre__->CantidadDeDimensiones; j++) //Para cada parametro j de cada vector de la particula i
        __Enjambre__->Part[i].Pi[j] = __Enjambre__->Part[i].Xi[j];
    }
}

void EjecutaBioinspirado(const BIO_PROCESO *__ProcesoBioinspirado__){
  ENJAMBRE *enjambre;
  unsigned int descriptor_index = 2*__ProcesoBioinspirado__->__descriptores__[0]+1;
  unsigned int inflim_index = 1;
  unsigned int suplim_index = 1+__ProcesoBioinspirado__->__descriptores__[0];
  lovdog_log = __ProcesoBioinspirado__->__nivel_de_log__;
  enjambre=CrearEnjambre(
      __ProcesoBioinspirado__->__descriptores__[descriptor_index], // Cantidad de partículas
      __ProcesoBioinspirado__->__descriptores__[0] // Cantidad de dimensiones
  );
  FuncionObjetivo = __ProcesoBioinspirado__->__FuncionDeFitness__;
  InicializarEnjambre(enjambre,
      __ProcesoBioinspirado__->__descriptores__[descriptor_index+4],//Factor Constricción,
      __ProcesoBioinspirado__->__descriptores__[descriptor_index+5],//Factor Inercia,
      __ProcesoBioinspirado__->__descriptores__[descriptor_index+2],//Valor Peso Personal C1,
      __ProcesoBioinspirado__->__descriptores__[descriptor_index+3],//Valor Peso Global C2,
      __ProcesoBioinspirado__->__descriptores__[descriptor_index+1],//Numero Máximo De Iteraciones,
      __ProcesoBioinspirado__->__descriptores__+inflim_index,//Limite Inferior,
      __ProcesoBioinspirado__->__descriptores__+suplim_index//Limite Superior
  );
  EvaluacionInicialEnjambreMin(enjambre, __ProcesoBioinspirado__->__ParametrosDeOperacion__);

  FILE
    *LogFile=NULL,
    *ResultsFile=NULL;

  CrearLog(__ProcesoBioinspirado__->__log__, &LogFile);
  CrearResultados(__ProcesoBioinspirado__->__results__, &ResultsFile);

  lovdog_startlog
  printf("\n ===== Inicialización ======\n");
  ImprimeEnjambre(enjambre);
  lovdog_endlog


  unsigned int n=0; while(n<__ProcesoBioinspirado__->__iteraciones__){
    //ActualizarVelocidad(enjambre);
    //ActualizarVelocidadClamping(enjambre);
    ActualizarVelocidadInerciaW(enjambre);
    ActualizarPosicion(enjambre);
    EvaluarEnjambreMin(enjambre, __ProcesoBioinspirado__->__ParametrosDeOperacion__);
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
}

void CrearLog(
   char *__ArchivoDeLog__,
   FILE ** __log__
){
  if(!__ArchivoDeLog__) return;
  if(__ArchivoDeLog__[0]=='\0') return;
  if(!__log__) return;
  if(*__log__) return;
  *__log__ = fopen(__ArchivoDeLog__,"w");
}

void CrearResults(
   char *__ArchivoDeResultados__,
   FILE ** __results__
){
  if(!__ArchivoDeResultados__) return;
  if(__ArchivoDeResultados__[0]=='\0') return;
  if(!__results__) return;
  if(*__results__) return;
  *__results__ = fopen(__ArchivoDeResultados__,"w");
}

