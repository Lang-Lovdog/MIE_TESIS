#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include "pso.h"

int main (void){
  const long double
    LimSup[2] = { 20, 20 },
    LimInf[2] = {-20,-20 }
  ;
  ProcesoPSO(
     20,   // Cantidad de Particulas
      2,   // Cantidad de Dimensiones
      LimSup,
      LimInf,
     60,   // Cantidad de Iteraciones
      0,
      2.0,
      2,
      NULL);
  return 0;
}

long double FuncionObjetivo(
    long double          *x,
    unsigned int          __CantidadDeParametros__,
    const long double    *__ParametrosDeOperacion__
){
  long double fit = 150 - powl(x[0]-2.0,2) - powl(x[1]-3.0,2);
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
  enjambre=CrearEnjambre(__NumeroDeParticulas__, __Dimension__);
  InicializarEnjambre(enjambre, __Factor_Constriccion_Inercia__, __ValorPesoPersonalC1__, __ValorPesoGlobalC2__, __NumeroMaximoDeIteraciones__, __LimiteInferior__, __LimiteSuperior__);
  EvaluacionInicialEnjambreMax(enjambre, __ParametrosDeOperacion__);
    printf("\n ===== Inicialización ======\n",0);
  ImprimeEnjambre(enjambre);
  unsigned char n=0; while(n<__NumeroMaximoDeIteraciones__){
    //ActualizarVelocidad(enjambre);
    ActualizarVelocidadClamping(enjambre);
    ActualizarPosicion(enjambre);
    EvaluarEnjambreMax(enjambre, __ParametrosDeOperacion__);
    ActualizarMejoresPosicionesMax(enjambre);
    printf("\n ===== Iteración %u ======\n",n);
    ImprimeEnjambre(enjambre);
    printf("\n");
    ++n;
  }
  printf("@ Mejor Partícula : \n{");
  ImprimeParticulaID(enjambre, enjambre->MejorParticulaDelGrupo);
  printf("\n}\n");
  EliminarEnjambre(enjambre);
}
