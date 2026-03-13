/* Algoritmo Genetico Simple
   Código Fuente: ags.c
   Dr. Carlos García

   Modificación por Lang Lovdog Inu Oókami
*/

#ifndef __lovdog__capulin_ags__
#define __lovdog__capulin_ags__

/*Estructuras Fundamentales del Algoritmo Genetico*/
typedef unsigned char BYTE;
typedef enum{MAX,MIN} TIPO_OPT;
typedef struct{ BYTE  *Cromosoma;
                int   *Vale;
                long double *Valr;
                long double  VObj;
                long double  Fit;
                }INDIVIDUO;
typedef struct{ INDIVIDUO          *Pob;
                INDIVIDUO          *NewPob;
                unsigned int        PobSize;
                unsigned int        NdGens;
                const unsigned int *NdBxGen;
                unsigned int        CromSize;
                const long double        *LimSup;
                const long double        *LimInf;
                unsigned int       IdWorst;
                unsigned int       IdBest;
                unsigned int       *Seleccion;
                long double              TotalFitness;
                long double              PromFit;
                long double              ProbabilidadCruza;
                long double              ProbabilidadMuta;
                unsigned int       NumMaxGenerations;
               }AGS;

AGS InicializarAGS(
    unsigned int        PobSize, 
    unsigned int        NumDeGen,
    const unsigned int *NumBitxGen,
    const long double  *LimSuperior,
    const long double  *LimInferior,
    long double         ProbCruza,
    long double         ProbMuta,
    unsigned int        N_Max_Generaciones
);
void DecodeReal(AGS* p);
void ShowReal(INDIVIDUO* p,unsigned int NdGens_);
void DecodeEntero(AGS* p);
void ShowEntero(INDIVIDUO* p,unsigned int NdGens_);
void ShowIndividuo(AGS *pAG, unsigned int Id);
void ShowPoblacion(AGS *pAG);
void EvaluarPoblacion(AGS *pAG); 
long double FuncionObjetivo(long double *Vr);
void Obj2Fit(AGS *pAG,TIPO_OPT tipo);
void SeleccionRuleta(AGS *pAG);
void Cruza1P(AGS *pAG);
void MutacionDeBit(AGS *pAG);
void NextGeneration(AGS *pAG);
void Elitismo(AGS *pAG);

#endif
