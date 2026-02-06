#include "pso.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// Definición d'as funciones

ENJAMBRE* CrearEnjambre(
    //ENJAMBRE* __Enjambre__,
    unsigned int __CantidadDeParticulas__,
    unsigned int __CantidadDeParametros__
  ){
  ENJAMBRE *ptr=NULL;
  //Reservar la memoria para la estructura del enjambre
  ptr=(ENJAMBRE *)malloc(sizeof(ENJAMBRE));
  if(!ptr){
    printf("Error al reservar la memoria para la estructura ENJAMBRE.");
    exit(0);
  }
  ptr->CantidadDeParticulas=__CantidadDeParticulas__;
  ptr->CantidadDeParametros=__CantidadDeParametros__;

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
    long double        __ValorDePeso_C1__,
    long double        __ValorDePeso_C2__,
    unsigned int       __MaximoDeIteraciones__,
    const long double *__LimitesInferiores__,
    const long double *__LimitesSuperiores__
){
  if(__Enjambre__){
  long double aux,rango;
  __Enjambre__->X                      = __FactorConstriccion__;
  __Enjambre__->C1                     = __ValorDePeso_C1__;
  __Enjambre__->C2                     = __ValorDePeso_C2__;
  __Enjambre__->MaximoDeIteraciones    = __MaximoDeIteraciones__;
  __Enjambre__->MejorParticulaDelGrupo = 0;
  __Enjambre__->LimitesInferiores      = __LimitesInferiores__;
  __Enjambre__->LimitesSuperiores      = __LimitesSuperiores__;
  //Dar constriccion uwu
  long double fi = __Enjambre__->C1+__Enjambre__->C2;
  __Enjambre__->Constriccion=2/fabs(2-fi-sqrt(pow(fi,2)-(4*fi)));
  lovdog_startlog
  printf("%f\n",fi);
  printf("%f",pow(fi,2)-(4*fi));
  printf("%f",sqrt(pow(fi,2)-(4*fi)));
  printf("%f",fabs(2-fi-sqrt(pow(fi,2)-(4*fi))));
  printf("%f\n\n",__Enjambre__->Constriccion);
  lovdog_endlog
  //Inicializar cada vector de cada particula
  for(unsigned int i=0; i<__Enjambre__->CantidadDeParticulas; ++i) //Para cada particula i
    for(unsigned int j=0; j<__Enjambre__->CantidadDeParametros; ++j) //Para cada parametro j de cada vector de la particula i
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
  for(unsigned int i=0; i<__Enjambre__->CantidadDeParametros; i++)
    printf("%f, ",__Enjambre__->Part[__ID_Particula__].Xi[i]);
  printf("\nP%i,Vi: ",__ID_Particula__);
  for(unsigned int i=0; i<__Enjambre__->CantidadDeParametros; i++)
    printf("%f, ",__Enjambre__->Part[__ID_Particula__].Vi[i]);
  printf("\nP%i,Pi: ",__ID_Particula__);
  for(unsigned int i=0; i<__Enjambre__->CantidadDeParametros; i++)
    printf("%f, ",__Enjambre__->Part[__ID_Particula__].Pi[i]);
  printf("\nP%i,Xfit=%f",__ID_Particula__,__Enjambre__->Part[__ID_Particula__].Xfit);
  printf("\nP%i,Pfit=%f",__ID_Particula__,__Enjambre__->Part[__ID_Particula__].Pfit);
}

void ImprimeParticula(
  const PARTICULA    *__Particula__,
  const unsigned int  __CantidadDeParametros__
){
  printf("\nParticula:");
  for(unsigned int i=0; i<__CantidadDeParametros__; i++)
    printf("%f, ",__Particula__->Xi[i]);
  printf("\nParticula Vi: ");
  for(unsigned int i=0; i<__CantidadDeParametros__; i++)
    printf("%f, ",__Particula__->Vi[i]);
  printf("\nParticula,Pi: ");
  for(unsigned int i=0; i<__CantidadDeParametros__; i++)
    printf("%f, ",__Particula__->Pi[i]);
  printf("\nParticula,Xfit=%f",__Particula__->Xfit);
  printf("\nParticula,Pfit=%f",__Particula__->Pfit);
}

void ImprimeEnjambre(ENJAMBRE *__Enjambre__)
{ for(unsigned int i=0; i<__Enjambre__->CantidadDeParticulas; ++i) //Para cada particula i
    ImprimeParticulaID(__Enjambre__,i);
}


void EvaluarEnjambreMin(ENJAMBRE *__Enjambre__,const long double* __ParametrosDeOperacion__){
  long double BestFit;
  // Calcular el valor de Fitness de cada particula
  BestFit = FuncionObjetivo(
      __Enjambre__->Part[0].Xi,
      __Enjambre__->CantidadDeParametros,
      __ParametrosDeOperacion__
    );
  for(unsigned int i=0; i<__Enjambre__->CantidadDeParticulas; i++){
    __Enjambre__->Part[i].Xfit = FuncionObjetivo(
        __Enjambre__->Part[i].Xi,
        __Enjambre__->CantidadDeParametros,
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
  BestFit = FuncionObjetivo(
      __Enjambre__->Part[0].Xi,
      __Enjambre__->CantidadDeParametros,
      __ParametrosDeOperacion__
    );
  for(unsigned int i=0; i<__Enjambre__->CantidadDeParticulas; i++){
    __Enjambre__->Part[i].Xfit = FuncionObjetivo(
        __Enjambre__->Part[i].Xi,
        __Enjambre__->CantidadDeParametros,
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
  BestFit=FuncionObjetivo(
      __Enjambre__->Part[0].Xi,
      __Enjambre__->CantidadDeParametros,
      __ParametrosDeOperacion__
    );
  for(unsigned int i=0; i<__Enjambre__->CantidadDeParticulas; i++){
    aux=FuncionObjetivo(
        __Enjambre__->Part[i].Xi,
        __Enjambre__->CantidadDeParametros,
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
  BestFit=FuncionObjetivo(
      __Enjambre__->Part[0].Xi,
      __Enjambre__->CantidadDeParametros,
      __ParametrosDeOperacion__
    );
  for(unsigned int i=0; i<__Enjambre__->CantidadDeParticulas; i++){
    aux=FuncionObjetivo(
        __Enjambre__->Part[i].Xi,
        __Enjambre__->CantidadDeParametros,
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
    for(unsigned int j=0; j<__Enjambre__->CantidadDeParametros; j++) //Para cada parametro j de cada vector Vi de la particula i
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
    for(unsigned int j=0; j<__Enjambre__->CantidadDeParametros; j++) //Para cada parametro j de cada vector Vi de la particula i
    {
      Y1=rand()/(long double)RAND_MAX;
      Y2=rand()/(long double)RAND_MAX;
      __Enjambre__->Part[i].Vi[j] =(
          (__Enjambre__->Part[i].Vi[j]*__Enjambre__->X)+
        (__Enjambre__->C1*Y1*(__Enjambre__->Part[i].Pi[j]-__Enjambre__->Part[i].Xi[j]))+
        (__Enjambre__->C2*Y2*(__Enjambre__->Part[__Enjambre__->MejorParticulaDelGrupo].Pi[j]-__Enjambre__->Part[i].Xi[j]))
      );
    }
}
void ActualizarVelocidadConstriction(
    ENJAMBRE *__Enjambre__
){
  long double Y1,Y2;
  //Actualizar cada vector velocidad Vi de cada particula
  for(unsigned int i=0; i<__Enjambre__->CantidadDeParticulas; i++) //Para cada particula i
    for(unsigned int j=0; j<__Enjambre__->CantidadDeParametros; j++) //Para cada parametro j de cada vector Vi de la particula i
    {
      Y1=rand()/(long double)RAND_MAX;
      Y2=rand()/(long double)RAND_MAX;
      //printf("Y1=%f Y2=%f",Y1,Y2);
      __Enjambre__->Part[i].Vi[j] =__Enjambre__->Constriccion*(
        (__Enjambre__->Part[i].Vi[j]+
        (__Enjambre__->C1*Y1*(__Enjambre__->Part[i].Pi[j]-__Enjambre__->Part[i].Xi[j]))+
        (__Enjambre__->C2*Y2*(__Enjambre__->Part[__Enjambre__->MejorParticulaDelGrupo].Pi[j]-__Enjambre__->Part[i].Xi[j]))
      ));
      //printf(" Vt+1= %f",__Enjambre__->Part[i].Vi[j]);
    }
}

void ActualizarPosicion(ENJAMBRE *__Enjambre__){
  // Acutailzsr cada vector Posicion XI de cada particula
  for(unsigned int i=0; i<__Enjambre__->CantidadDeParticulas; i++) //Para cada particula i
    for(unsigned int j=0; j<__Enjambre__->CantidadDeParametros; j++) //Para cada parametro j de cada vector de la particula i
      __Enjambre__->Part[i].Xi[j] += __Enjambre__->Part[i].Vi[j];
}

void ActualizarMejoresPosicionesMin(ENJAMBRE *__Enjambre__){
  for(unsigned int i=0; i<__Enjambre__->CantidadDeParticulas; i++)
    if(__Enjambre__->Part[i].Xfit < __Enjambre__->Part[i].Pfit){
      __Enjambre__->Part[i].Pfit = __Enjambre__->Part[i].Xfit;
      for(unsigned int j=0; j<__Enjambre__->CantidadDeParametros; j++) //Para cada parametro j de cada vector de la particula i
        __Enjambre__->Part[i].Pi[j] = __Enjambre__->Part[i].Xi[j];
    }
}

void ActualizarMejoresPosicionesMax(ENJAMBRE *__Enjambre__){
  for(unsigned int i=0; i<__Enjambre__->CantidadDeParticulas; i++)
    if(__Enjambre__->Part[i].Xfit > __Enjambre__->Part[i].Pfit){
      __Enjambre__->Part[i].Pfit = __Enjambre__->Part[i].Xfit;
      for(unsigned int j=0; j<__Enjambre__->CantidadDeParametros; j++) //Para cada parametro j de cada vector de la particula i
        __Enjambre__->Part[i].Pi[j] = __Enjambre__->Part[i].Xi[j];
    }
}


/*long double FuncionObjetivo(long double *__ValoresDeParametros__, unsigned int __CantidadDeParametros__){
  unsigned int k;
  long double fit, aux = 0;
  // Maximar la siguiente funcion:
  //   f(x,y)=50-(x-5)^2-(y-5)^2; 
  //fit=250-pow(Xi[0]+7,2)-pow(Xi[1]-3,2)-pow(Xi[2]-3,2)-pow(Xi[3]-5,2)-pow(Xi[4]-8,2);

  // Funcion Rastriging (Buscamos el valor 0)
  for (k=0; k<__CantidadDeParametros__; k++)
    aux += pow(__ValoresDeParametros__[k],2)-10*cos(6.283185*__ValoresDeParametros__[k])+10;
  fit = 100 - aux; // El valor d'a precisión se ponderará en una escala del 1 al 100
  return fit;
}*/
