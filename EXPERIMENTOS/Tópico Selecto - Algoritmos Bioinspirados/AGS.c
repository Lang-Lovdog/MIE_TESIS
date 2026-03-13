/* Algoritmo Genetico Simple
   Código Fuente: ags.c
   Dr. Carlos García
*/

#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<time.h>

/*Configuraciones del Algoritmo Geneticos*/
#define NumDeGenes_ 2
const unsigned int PoblacionSize = 30;
const unsigned int NumeroDeGenes = NumDeGenes_;
const unsigned int NumDeBitPorGen[NumDeGenes_]={16,16};
const float LimitesSuperior[NumDeGenes_]={ 6.28, 6.28};
const float LimitesInferior[NumDeGenes_]={-6.28,-6.28};
const float PCruza=0.8; 
const float PMuta=0.01;
const unsigned int MAXdeGenearciones=300;

/*Estructuras Fundamentales del Algoritmo Genetico*/
typedef unsigned char BYTE;
typedef enum{MAX,MIN} TIPO_OPT;
typedef struct{ BYTE  *Cromosoma;
	              int   *Vale;
	              float *Valr;
                float  VObj;
                float  Fit;
                }INDIVIDUO;
typedef struct{ INDIVIDUO          *Pob;
                INDIVIDUO          *NewPob;
                unsigned int        PobSize;
                unsigned int        NdGens;
                const unsigned int *NdBxGen;
                unsigned int        CromSize;
                const float        *LimSup;
                const float        *LimInf;
                unsigned int       IdWorst;
                unsigned int       IdBest;
                unsigned int       *Seleccion;
                float              TotalFitness;
                float              PromFit;
                float              ProbabilidadCruza;
                float              ProbabilidadMuta;
                unsigned int       NumMaxGenerations;
               }AGS;

AGS InicializarAGS(unsigned int PobSize, 
                   unsigned int NumDeGen,
                   const unsigned int *NumBitxGen,
                   const float *LimSuperior,
                   const float *LimInferior,
                   float ProbCruza,
                   float ProbMuta,
                   unsigned int N_Max_Generaciones);
void DecodeReal(AGS* p);
void ShowReal(INDIVIDUO* p,unsigned int NdGens_);
void DecodeEntero(AGS* p);
void ShowEntero(INDIVIDUO* p,unsigned int NdGens_);
void ShowIndividuo(AGS *pAG, unsigned int Id);
void ShowPoblacion(AGS *pAG);
void EvaluarPoblacion(AGS *pAG); 
float FuncionObjetivo(float *Vr);
void Obj2Fit(AGS *pAG,TIPO_OPT tipo);
void SeleccionRuleta(AGS *pAG);
void Cruza1P(AGS *pAG);
void MutacionDeBit(AGS *pAG);
void NextGeneration(AGS *pAG);
void Elitismo(AGS *pAG);

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
  printf("\nTotal de Fitness: %f",ga.TotalFitness);
  printf("\nPromedio Fitness: %f",ga.PromFit);
  printf("\nEl mejor es el %i",ga.IdBest);
  printf("\nEl peor es el %i",ga.IdWorst);
  
  while(generacion<=ga.NumMaxGenerations)
  { SeleccionRuleta(&ga);
    Cruza1P(&ga);
    MutacionDeBit(&ga);
    Elitismo(&ga);
    NextGeneration(&ga);
    DecodeReal(&ga);
    EvaluarPoblacion(&ga);
    Obj2Fit(&ga,MAX);
    printf("\nGeneracion %i:",generacion);
    ShowPoblacion(&ga);
    printf("\nTotal de Fitness: %f",ga.TotalFitness);
    printf("\nPromedio Fitness: %f",ga.PromFit);
    printf("\nEl mejor es el %i, Obj=%f",ga.IdBest,ga.Pob[ga.IdBest].VObj);
    printf("\nEl peor es el %i",ga.IdWorst);
    generacion++;
  }
  return 0;	
}

void Elitismo(AGS *pAG)
{ int k;
  for(k=0; k<pAG->CromSize; k++)
      pAG->NewPob[0].Cromosoma[k]=pAG->Pob[pAG->IdBest].Cromosoma[k];
}

void NextGeneration(AGS *pAG)
{ INDIVIDUO *aux;
  aux=pAG->Pob;
  pAG->Pob=pAG->NewPob;
  pAG->NewPob=aux;
}

void MutacionDeBit(AGS *pAG)
{ int i,k,q,aux;
  float x;
  for(i=0; i<pAG->PobSize; i++)
  for(k=0; k<pAG->CromSize; k++)
     { x=(float)rand()/RAND_MAX;
       if(x<pAG->ProbabilidadMuta)
          { //printf("\nSe muto bit:%i, de Poblador%i",k,i);
            if(pAG->NewPob[i].Cromosoma[k])
               pAG->NewPob[i].Cromosoma[k]=0;
            else
               pAG->NewPob[i].Cromosoma[k]=1;
           /*printf("\nHijo(%i):",i);  
           for(q=0; q<pAG->CromSize; q++)
              { aux=pAG->NewPob[i].Cromosoma[q];
                printf("%i",aux); } */
          }
      }
}

void Cruza1P(AGS *pAG)
{ int i,k,PuntoDeCruza,aux;
  float x;
  for(i=0; i<pAG->PobSize; i+=2)
     { x=(float)rand()/RAND_MAX;
       if(x<=pAG->ProbabilidadCruza)
         { PuntoDeCruza=(rand()%pAG->CromSize);
           for(k=0; k<PuntoDeCruza; k++)
              { pAG->NewPob[i].Cromosoma[k]=pAG->Pob[pAG->Seleccion[i+1]].Cromosoma[k];
                pAG->NewPob[i+1].Cromosoma[k]=pAG->Pob[pAG->Seleccion[i]].Cromosoma[k];
              }   
           for(k=PuntoDeCruza; k<pAG->CromSize; k++)
              { pAG->NewPob[i].Cromosoma[k]=pAG->Pob[pAG->Seleccion[i]].Cromosoma[k];
                pAG->NewPob[i+1].Cromosoma[k]=pAG->Pob[pAG->Seleccion[i+1]].Cromosoma[k];
              }
          }
        else
          { //printf("\n(x=%f)No se cruzo %i",x,i);  
            for(k=0; k<pAG->CromSize; k++)
              { pAG->NewPob[i].Cromosoma[k]=pAG->Pob[pAG->Seleccion[i]].Cromosoma[k];
                pAG->NewPob[i+1].Cromosoma[k]=pAG->Pob[pAG->Seleccion[i+1]].Cromosoma[k];
              }
        }
       /*
       printf("\nPunto de cruza: %i",PuntoDeCruza);  
       printf("\nPadre(i=%i,%i):",i,pAG->Seleccion[i]);  
       for(k=0; k<pAG->CromSize; k++)
          { aux=pAG->Pob[pAG->Seleccion[i]].Cromosoma[k];
            printf("%i",aux); } 
       printf("\nPadre(i=%i,%i):",i+1,pAG->Seleccion[i+1]);  
       for(k=0; k<pAG->CromSize; k++)
          { aux=pAG->Pob[pAG->Seleccion[i+1]].Cromosoma[k];
            printf("%i",aux); }         
       printf("\nHijo(%i):",i);  
       for(k=0; k<pAG->CromSize; k++)
          { aux=pAG->NewPob[i].Cromosoma[k];
            printf("%i",aux); } 
       printf("\nHijo(%i):",i+1);  
       for(k=0; k<pAG->CromSize; k++)
          { aux=pAG->NewPob[i+1].Cromosoma[k];
            printf("%i",aux); }
       */     
     }      
}

void SeleccionRuleta(AGS *pAG)
{ float Ruleta[pAG->PobSize];
  float pelota,suma;
  int i,k;
  //Constuir la ruleta con partes proporcionales
  // al Fitness de cada individuo 
  for(k=0; k<pAG->PobSize; k++)
     { Ruleta[k]=pAG->Pob[k].Fit/pAG->TotalFitness;
       //printf("\nRuleta[%i],%2.2f%%",k,100*Ruleta[k]);
      }

  for(i=0; i<pAG->PobSize; i++)
     {pelota=(float)rand()/RAND_MAX;
      //printf("\nPelota: %f%%",100*pelota);
      suma=0;
      for(k=0; k<pAG->PobSize; k++)
         {suma+=Ruleta[k];
          if(suma>pelota)
            {pAG->Seleccion[i]=k;
             break; }
          }
      //printf("\nIndividuo seleccionado: %i",pAG->Seleccion[i]);
     }
}

float FuncionObjetivo(float *Vr)
{ float Obj;
  //Evaluar al individuo de acuerdo con el problema a resolver
  //Obj=50 -pow(Vr[0]-5,2) -pow(Vr[1]-5,2); 
  Obj= 10*exp((-1*(pow(Vr[0]+1,2)+pow(Vr[1]-3.14,2)))/25)+cos(2*Vr[0])+sin(2*Vr[1]); 
  return Obj;
}
void Obj2Fit(AGS *pAG,TIPO_OPT tipo)
{ unsigned int k;
  float aux,min,max,dif;
  pAG->TotalFitness=0;

  dif=fabsf(pAG->Pob[pAG->IdBest].VObj-pAG->Pob[pAG->IdWorst].VObj);
  if(dif<0.000001)
    { for(k=0; k<pAG->PobSize; k++)
             { pAG->Pob[k].Fit=100;
               pAG->TotalFitness+=pAG->Pob[k].Fit; }
      pAG->PromFit=pAG->TotalFitness/pAG->PobSize;
    }
  else{  
      if(tipo==MAX)
        { min=pAG->Pob[pAG->IdWorst].VObj;
          max=pAG->Pob[pAG->IdBest].VObj-min;
          //Recorre toda la poblacion
          for(k=0; k<pAG->PobSize; k++)
             { pAG->Pob[k].Fit=100*((pAG->Pob[k].VObj-min)/max);
               pAG->TotalFitness+=pAG->Pob[k].Fit; }
               pAG->PromFit=pAG->TotalFitness/pAG->PobSize;
               }
      else
        { max=pAG->Pob[pAG->IdBest].VObj;
          min=max-pAG->Pob[pAG->IdWorst].VObj;
          for(k=0; k<pAG->PobSize; k++)
             { pAG->Pob[k].Fit=100*((max-pAG->Pob[k].VObj)/min);
               pAG->TotalFitness+=pAG->Pob[k].Fit;}
          pAG->PromFit=pAG->TotalFitness/pAG->PobSize;
          aux=pAG->IdWorst;
          pAG->IdWorst=pAG->IdBest;
          pAG->IdBest=aux;  
        }
      }  
}
void EvaluarPoblacion(AGS *pAG)
{ unsigned int k;
   //Recorre toda la poblacion
  pAG->IdBest=0;
  pAG->IdWorst=0;
  pAG->Pob[0].VObj=FuncionObjetivo(&pAG->Pob[0].Valr[0]);
  for(k=1; k<pAG->PobSize; k++)
     { pAG->Pob[k].VObj=FuncionObjetivo(&pAG->Pob[k].Valr[0]);
       if(pAG->Pob[k].VObj>pAG->Pob[pAG->IdBest].VObj)
          pAG->IdBest=k;
       if(pAG->Pob[k].VObj<pAG->Pob[pAG->IdWorst].VObj)
          pAG->IdWorst=k; 
       }
}

void DecodeEntero(AGS* p)
{ int j,i,k,Inicio;
  //i es el indice para recorrer todos los genes de un individuo
  //K es el indice para recorrer todos los bits de un gen
  for(j=0; j<p->PobSize; j++)
     { Inicio=0; 
       for(i=0; i<p->NdGens; i++)
          { p->Pob[j].Vale[i]=0;
            for(k=Inicio; k<(p->NdBxGen[i]+Inicio); k++)
               p->Pob[j].Vale[i]+=pow(2,k-Inicio)*p->Pob[j].Cromosoma[k];
            Inicio+=p->NdBxGen[i];
          }
     }
}

void DecodeReal(AGS* p)
{ float rango;
  int i,j,k,Inicio;
  for(j=0; j<p->PobSize; j++)
     {Inicio=0; 
      //i es el indice para recorrer todos los genes de un individuo
      //K es el indice para recorrer todos los bits de un gen
      for(i=0; i<p->NdGens; i++)
         { p->Pob[j].Vale[i]=0;
           for(k=Inicio; k<(p->NdBxGen[i]+Inicio); k++)
               p->Pob[j].Vale[i]+=pow(2,k-Inicio)*p->Pob[j].Cromosoma[k];
           Inicio+=p->NdBxGen[i];
          }
      for(i=0; i<p->NdGens; i++)
         { rango=p->LimSup[i]-p->LimInf[i];
           p->Pob[j].Valr[i]=(p->Pob[j].Vale[i]/(pow(2,p->NdBxGen[i])-1))*rango + p->LimInf[i];
          }
      }  
}

void ShowReal(INDIVIDUO* p,unsigned int NdGens_)
{ int k;
  printf(" - ");
  for(k=NdGens_-1; k>=0; k--)
      printf("%f,",p->Valr[k]);
}

void ShowEntero(INDIVIDUO* p,unsigned int NdGens_)
{ int k;
  printf(" - ");
  for(k=NdGens_-1; k>=0; k--)
      printf("%i,",p->Vale[k]);
}

void ShowPoblacion(AGS *pAG)
{ unsigned int k;
  for(k=0; k<pAG->PobSize; k++)
     ShowIndividuo(pAG,k);
}
void ShowIndividuo(AGS *pAG, unsigned int Id)
{ int k,j,acumulador;
  acumulador= pAG->CromSize - pAG->NdBxGen[pAG->NdGens-1];
  j=pAG->NdGens-1;
  printf("\n:");
  for(k=pAG->CromSize-1; k>=0; k--)
     { if(k==acumulador-1)
          { printf(":");
            j--;
            acumulador-=pAG->NdBxGen[j];
           }
	     printf("%i",pAG->Pob[Id].Cromosoma[k]);
      }
  ShowEntero(&pAG->Pob[Id],pAG->NdGens);
  ShowReal(&pAG->Pob[Id],pAG->NdGens);
  printf(" VObj: %f",pAG->Pob[Id].VObj);
  printf(" Fit: %f",pAG->Pob[Id].Fit);
}

AGS InicializarAGS(unsigned int PobSize, 
                   unsigned int NumDeGen, 
                   const unsigned int *NumBitxGen,
                   const float *LimSuperior,
                   const float *LimInferior,
                   float ProbCruza,
                   float ProbMuta,
                   unsigned int N_Max_Generaciones)
{ AGS ag;
  unsigned int k,j,aux=0;
  ag.PobSize=PobSize;
  ag.ProbabilidadCruza=ProbCruza;
  ag.ProbabilidadMuta=ProbMuta;
  ag.NumMaxGenerations=N_Max_Generaciones;
  //Reservar memoria para la Poblacion de Individuos
  ag.Pob=(INDIVIDUO *)malloc(ag.PobSize*sizeof(INDIVIDUO));
  if(ag.Pob==NULL)
    { printf("Error, no se pudo reservar memoria para los individuos");
      exit(0);
    }
  ag.NewPob=(INDIVIDUO *)malloc(ag.PobSize*sizeof(INDIVIDUO));  
  if(ag.NewPob==NULL)
    { printf("Error, no se pudo reservar memoria para los nuevos individuos");
      exit(0);
    }
  ag.NdGens=NumDeGen;
  ag.NdBxGen=NumBitxGen;
  ag.LimSup=LimitesSuperior;
  ag.LimInf=LimitesInferior;
  //Reservar memoria para la decodificaion a Entero de la poblacion
  for(k=0; k<ag.PobSize; k++)
     { ag.Pob[k].Vale=(int *)malloc(ag.NdGens*sizeof(int));
       if(ag.Pob[k].Vale==NULL)
         { printf("Error, no se pudo reservar memoria para la decodificacion entero.");
           exit(0);
           }  
     }
  for(k=0; k<ag.PobSize; k++)
     { ag.NewPob[k].Vale=(int *)malloc(ag.NdGens*sizeof(int));
       if(ag.NewPob[k].Vale==NULL)
         { printf("Error, no se pudo reservar memoria para la decodificacion entero.");
           exit(0);
           }  
     }   
  //Reservar memoria para la decodificaion a Real de la poblacion
  for(k=0; k<ag.PobSize; k++)
     { ag.Pob[k].Valr=(float *)malloc(ag.NdGens*sizeof(float));
       if(ag.Pob[k].Valr==NULL)
         { printf("Error, no se pudo reservar memoria para la descodificacion real.");
           exit(0);
          }  
     }
  for(k=0; k<ag.PobSize; k++)
     { ag.NewPob[k].Valr=(float *)malloc(ag.NdGens*sizeof(float));
       if(ag.NewPob[k].Valr==NULL)
         { printf("Error, no se pudo reservar memoria para la descodificacion real.");
           exit(0);
          }  
     }   
   //Calcular el tamaño en bits del cromosoma
  for(k=0; k<ag.NdGens; k++)
      aux+=ag.NdBxGen[k];
  ag.CromSize=aux;
  //Reservar la memoria para el cromosoma de cada individuo
  for(k=0; k<ag.PobSize; k++)
     { ag.Pob[k].Cromosoma=(BYTE *)malloc(ag.CromSize*sizeof(BYTE));
       if(ag.Pob[k].Cromosoma==NULL)
         { printf("Error, no se pudo reservar memoria para el cromosoma.");
           exit(0);
           }
     }
  //Reservar la memoria para el cromosoma de cada individuo
  for(k=0; k<ag.PobSize; k++)
     { ag.NewPob[k].Cromosoma=(BYTE *)malloc(ag.CromSize*sizeof(BYTE));
       if(ag.NewPob[k].Cromosoma==NULL)
         { printf("Error, no se pudo reservar memoria para el cromosoma.");
           exit(0);
           }
     }   
  //Inicializar el cromosoma de cada individuo
  for(k=0; k<ag.PobSize; k++)
  for(j=0; j<ag.CromSize; j++)
      ag.Pob[k].Cromosoma[j]=rand()%2;
  //Reservar Memoria para el listado de Individuos Seleccionados
  ag.Seleccion=(unsigned int *)malloc(ag.PobSize*sizeof(unsigned int));  
  return ag;
}


