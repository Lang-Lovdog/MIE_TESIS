#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<math.h>
#include"ags.h"

/*Configuraciones del Algoritmo Geneticos*/
#define NumDeGenes_ 10
const unsigned int PoblacionSize = 300;
const unsigned int NumeroDeGenes = NumDeGenes_;
const unsigned int NumDeBitPorGen[NumDeGenes_]={16,16,16,16,16,16,16,16,16,16};
const long double LimitesSuperior[NumDeGenes_]={ 20, 20, 20, 20, 20, 20, 20, 20, 20, 20};
const long double LimitesInferior[NumDeGenes_]={-20,-20,-20,-20,-20,-20,-20,-20,-20,-20};
const long double PCruza=0.85; 
const long double PMuta=0.005;
const unsigned int MAXdeGenearciones=600;


int main()
{ AGS ga;
  unsigned int generacion=1;
  time_t tx;
  srand((unsigned) time(&tx));
  ga=InicializarAGS( PoblacionSize,  
                     NumeroDeGenes,
                     NumDeBitPorGen,
                     LimitesSuperior,
                     LimitesInferior,
                     PCruza,
                     PMuta,
                     MAXdeGenearciones);
  DecodeReal(&ga);
  EvaluarPoblacion(&ga);
  Obj2Fit(&ga,MAX);
  ShowPoblacion(&ga);
  printf("\nTotal de Fitness: %Lf",ga.TotalFitness);
  printf("\nPromedio Fitness: %Lf",ga.PromFit);
  printf("\nEl mejor es el %i",ga.IdBest);
  printf("\nEl peor es el %i",ga.IdWorst);
  
  while(generacion<=ga.NumMaxGenerations) {
    SeleccionRuleta(&ga);
    Cruza1P(&ga);
    MutacionDeBit(&ga);
    Elitismo(&ga);
    NextGeneration(&ga);
    DecodeReal(&ga);
    EvaluarPoblacion(&ga);
    Obj2Fit(&ga,MAX);
    //printf("\nGeneracion %i:",generacion);
    //ShowPoblacion(&ga);
    //printf("\nTotal de Fitness: %Lf",ga.TotalFitness);
    //printf("\nPromedio Fitness: %Lf",ga.PromFit);
    //printf("\nEl mejor es el %i, Obj=%Lf",ga.IdBest,ga.Pob[ga.IdBest].VObj);
    //printf("\nEl peor es el %i",ga.IdWorst);
    generacion++;
  }
  ShowIndividuo(&ga,ga.IdBest);
  printf("\nTotal de Fitness: %Lf",ga.TotalFitness);
  printf("\nPromedio Fitness: %Lf",ga.PromFit);
  printf("\nEl mejor es el %i, Obj=%Lf",ga.IdBest,ga.Pob[ga.IdBest].VObj);
  printf("\nEl peor es el %i",ga.IdWorst);
  return 0;	
}


long double FuncionObjetivo(long double *x) { 
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
