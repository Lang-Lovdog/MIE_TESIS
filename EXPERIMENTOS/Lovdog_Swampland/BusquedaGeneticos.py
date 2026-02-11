import mealpy as mp # type: ignore
from mealpy                import FloatVar, get_optimizer_by_name
from MetastableVacua       import fitness_function_mealpy as ff
from test_fitness_function import plot_potencial_vs_autovalores

vacua_parametros__dS = {
    "obj_func": ff,
    "bounds": FloatVar(
        #    AH3   AF3   AF5   A3N3   s      tau
        lb=[-100, -100, -100, -100, 1e-20, 1e-20, ],
        ub=[ 100,  100,  100,  100,   100,   100, ]
    ),
    "minmax": "min",
    "log_to": "MetastableVacuaReprise.log"
}

vacua_parametros_AdS = {
    "obj_func": ff,
    "bounds": FloatVar(
        #    AH3   AF3   AF5   A3N3  AD5    s      tau
        lb=[-100, -100, -100, -100, -100, 1e-20, 1e-20, ],
        ub=[ 100,  100,  100,  100,  100,   100,   100, ]
    ),
    "minmax": "min",
    "log_to": "MetastableVacuaReprise.log"
}

#### Creación de un genético simple para minimización de la función ff
genetico = mp.GA.BaseGA(epoch=500, pop_size=50, pc=0.8, pm=0.2)
genetico.solve(vacua_parametros__dS)
#### Creación de un genético simple para minimización de la función ff
#### Imprimir solución
print(f"Solución: {genetico.g_best.solution}, Fitness: {genetico.g_best.target.fitness}")
