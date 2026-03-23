#ifndef __lovdog__pso__header__
#define __lovdog__pso__header__

typedef int lovdog_log_var;

#ifndef lovdog_log_setup
#define lovdog_log_setup extern lovdog_log_var lovdog_log

#define lovdog_startlog      if(lovdog_log & 0b1000){
#define lovdog_endlog        }

#define lovdog_startverb(vl) if(lovdog_log & vl){
#define lovdog_endverb       }
#endif

#include <stdio.h>

void lovdog_log_level(lovdog_log_var vl);

// Definición de la estructura Patícula
// Esta partícula representa a un individuo
// El individuo buscará tener la mejor posición
// Habrán dos criterios: En el primero, ve la mejor
// posición que ha tenido durante su existencia; en
// el segundo, ve qué partícula tiene la mejor posición
// en ese momento.
// Recalcula su valor de paso (velocidad) y, a partir de
// ahí, suma el paso a su posición actual, obteniendo el
// nuevo valor de posición.
// La partícula requiere saber en cuántas dimensiones
// estará moviéndose. Dichas dimensiones definirán al vector
// posición y al vector velocidad.
typedef struct PARTICULA{ 
  long double *Xi;   //Posicion
  long double *Vi;   //Velocidad
  long double *Pi;   //Mejor Posicion Historica
  long double  Xfit; //Valor de Fitnes para la posicion actual
  long double  Pfit; //Valor de Fitnes para la Mejor Posicion Historica
}PARTICULA;

// Definición de la estructura Enjambre
// El enjambre es un conjunto de partículas
// Este conjunto actuará para encontrar soluciones
// Cada solución es repensada según los valores históricos
// y valores presentes.
typedef struct ENJAMBRE{ // Iniciando en 2N+3
  PARTICULA         *Part;                    // Arreglo de partículas
  unsigned int       CantidadDeParticulas;    // Número de partículas [0]
  unsigned int       CantidadDeDimensiones;   // Número de dimensiones del espacio de búsqueda
  unsigned int       MejorParticulaDelGrupo;  // ID de la mejor partícula del grupo
  unsigned int       MaximoDeIteraciones;     // Número máximo d'iteraciones a realizar  [1]
  long double        C1;                      // Coeficiente de influencia individual    [2]
  long double        C2;                      // Coeficiente de influencia social        [3]
  const long double *LimitesSuperiores;       // Limites Superiores de las dimensions del espacio de búsqueda
  const long double *LimitesInferiores;       // Limites Inferiores de las dimensions del espacio de búsqueda
  long double        K;                       // Factor de constricción (convergencia)   [4]
  long double        W;                       // Peso de inercia                         [5]
  long double        Constriccion;            // Factor de constricción (convergencia)   [6]
  unsigned char      TipoPSO;                 // Tipo de Actualización                   [7]
                                              // 0b1(maximiza) 0b0(minimiza) 0b01(clamp) 0b001(constrain) 0b0001(inercia)
}ENJAMBRE;


/* La función a evaluar, regresa el valor de fitness (precisión)
 * Requiere ser definida para l'evaluación d'as partículas
 * Valores De Parametros .... (arreglo long double)
 * Cantidad De Parametros ... (int)
 * Parametros De Operacion .. (arreglo long double)
*/
typedef long double (*FitnessFunction)(
    long double          *__ValoresDeParametros__,
    unsigned int          __CantidadDeParametros__,
    const long double    *__ParametrosDeOperacion__);

/* Esta estructura fungirá en la versión 0.0.2 del framework
* estará planificada para póstumos usos de la biblioteca en
* aplicaciones más extensibles.
* Los descriptores variarán según el bio inspirado a utilizar,
* sin embargo, los elementos base serán siempre los mismos
* [0]:          Dimensiones del espacio de búsqueda
* [1,N]:        Límites superiores
* [N+1,2N]:     Límites inferiores
* [2N+1]:       Bioinspirado a utilizar
* [2N+2,...]:   Elementos del bioinspirado
*/ 

typedef struct BIO_PROCESO {
  long double         *__descriptores__;
  unsigned int         __iteraciones__;
  char*                __log__;
  char*                __results__;
  unsigned int         __nivel_de_log__;
  FitnessFunction      __FuncionDeFitness__;
  const long double   *__ParametrosDeOperacion__;
} BIO_PROCESO;

// Operadores generales

/* Creación de archivo de log */
void CrearLog(
   char *__ArchivoDeLog__,
   FILE** __log__
);

/*Crear archivo de resultados */
void CrearResultados(
   char *__ArchivoDeResultados__,
   FILE** __results__
);


// Operadores del enjambre (métodos)

/* Creador de enjambres:
 * Recibe el número de partículas y el número de parámetros
 * (variables del problema)*/
ENJAMBRE* CrearEnjambre(
    //ENJAMBRE     *__Enjambre__,
    unsigned int  __CantidadDeParticulas__,
    unsigned int  __CantidadDeParametros__
  );
/* Inicializador de enajmbres:
 * Defie los valoes predeterminados (de inicio), de los individuos.
 * Recibe el enjambre, la posición inicial, las variables del problema,
 * y los límites*/
void InicializarEnjambre(
    ENJAMBRE          *__Enjambre__,
    long double        __FactorConstriccion__,
    long double        __PesoDeInercia__,
    long double        __ValorDePeso_C1__,
    long double        __ValorDePeso_C2__,
    unsigned int       __MaximoDeIteraciones__,
    const long double *__LimitesInferiores__,
    const long double *__LimitesSuperiores__
  );
/* Una vez terminado el programa, ésta función liberará la memoria
 * que se reservó durante la creación del enjambre. Como argumento,
 * recibe al apuntador del enjambre.*/
void EliminarEnjambre(
    ENJAMBRE *__Enjambre__
  );
/* Nos permite visualizar los parámetros de la partícula.*/
void ImprimeParticulaID(
    ENJAMBRE     *__Enjambre__,
    unsigned int  __ID_Particula__
  );
/*Imprime la particula sin enjambre*/
void ImprimeParticula(
  const PARTICULA    *__Particula__,
  const unsigned int  __CantidadDeParametros__
  );
/* Función para copiar partícula a partícula*/
void CopiaParticula(
    PARTICULA* __Destino__,
    PARTICULA* __Origen__,
    const unsigned int __CantidadDeParametros__
);
/* Permite visualizar los parámetros del enjambre, y las partículas
 * que le componen.*/
void ImprimeEnjambre(
    ENJAMBRE *__Enjambre__
  );
/* Permite valorar al enjambre, según los criterios del PSO
 * y de la función objetivo*/
void EvaluarEnjambreMin(
    ENJAMBRE    *__Enjambre__,
    const long double *__ParametrosDeOperacion__
  );
void EvaluarEnjambreMax(
    ENJAMBRE    *__Enjambre__,
    const long double *__ParametrosDeOperacion__
  );
/* Similar a EvaluarEnjambre, con la particularidad de que Inicializa
 * los valores de Mejor Posicion Historica, de las particulas*/
void EvaluacionInicialEnjambreMin(
    ENJAMBRE    *__Enjambre__,
    const long double *__ParametrosDeOperacion__
  );
void EvaluacionInicialEnjambreMax(
    ENJAMBRE    *__Enjambre__,
    const long double *__ParametrosDeOperacion__
  );
/* Renueva la valocidad basado en los vectores de
 * Posición Actual,
 * Mejor Posicion Historica y
 * Mejor Posicion Global Actual*/
void ActualizarVelocidad(
    ENJAMBRE *__Enjambre__
  );
void ActualizarVelocidadClamping(
    ENJAMBRE *__Enjambre__
  );
void ActualizarVelocidadInerciaW(
    ENJAMBRE *__Enjambre__
  );
void ActualizarVelocidadConstriction(
    ENJAMBRE *__Enjambre__
  );
/* Suma los valores de velocidad a la posición actual de
 * cada partícula.*/
void ActualizarPosicion(
    ENJAMBRE *__Enjambre__
  );
/* Valora, en cada partícula, si el valor actual es mejor que'l mejor
 * valor histórico; si los valores actuales son mejores, actualiza
 * los parametros. */
void ActualizarMejoresPosicionesMin(
    ENJAMBRE *__Enjambre__
  );
void ActualizarMejoresPosicionesMax(
    ENJAMBRE *__Enjambre__
  );

/* Funcion que se puede definir para realizar el procesamiento pso,
 * puede ser ignorado o definido y consta d'os sig. elementos, en
 * el orden en que se presentan a continuación:
 * Numero De Particulas ................. (long double)
 * Dimension ............................ (long double)
 * Límites Superiores ................... (arreglo long double)
 * Límite Inferiores .................... (arreglo long double)
 * Numero Máximo De Iteraciones ......... (int)
 * Factor De Constriccion O De Inercia .. (long double)
 * Valor Peso C1: Mejor Personal ........ (long double)
 * Valor Peso C2: Mejor Global .......... (long double)
 * Parametros De Operacion .............. (arreglo long double) */
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
  );

void EjecutaBioinspirado(const BIO_PROCESO* __ProcesoBioinspirado__);

#endif
