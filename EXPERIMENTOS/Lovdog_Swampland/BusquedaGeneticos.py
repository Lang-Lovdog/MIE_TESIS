import mealpy as mp # type: ignore
import pandas as pd # type: ignore
from mealpy                import FloatVar, get_optimizer_by_name
from MetastableVacua       import fitness_function_mealpy as ff
from MetastableVacua       import fitness_function_AdS_mealpy as ff2
from MetastableVacua       import autovalores_VHess
from MetastableVacua       import autovalores_VHess_AdS
from MetastableVacua       import potencial_eval
from MetastableVacua       import potencial_eval_AdS

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
    "obj_func": ff2,
    "bounds": FloatVar(
        #    AH3   AF3   AF5   A3N3  AD5    s      tau
        lb=[-100, -100, -100, -100, -100, 1e-20, 1e-20, ],
        ub=[ 100,  100,  100,  100,  100,   100,   100, ]
    ),
    "minmax": "min",
    "log_to": "MetastableVacuaRepriseAdS.log"
}

genetico = mp.GA.BaseGA(epoch=50, pop_size=50, pc=0.8, pm=0.2)

def dS_search():

    global vacua_parametros__dS
    global genetico

    found_solutions_rows = []
    for i in range(1,100):
        print(f"Iteración {i}")
        #### Creación de un genético simple para minimización de la función ff
        genetico.solve(vacua_parametros__dS)
        #### Creación de un genético simple para minimización de la función ff
        #### Imprimir solución
        print(f"Solución: {genetico.g_best.solution}, Fitness: {genetico.g_best.target.fitness}")
        avalores = autovalores_VHess(
            genetico.g_best.solution[0],
            genetico.g_best.solution[1],
            genetico.g_best.solution[2],
            genetico.g_best.solution[3],
            genetico.g_best.solution[4],
            genetico.g_best.solution[5],
        )
        potencial = potencial_eval(
            genetico.g_best.solution[0],
            genetico.g_best.solution[1],
            genetico.g_best.solution[2],
            genetico.g_best.solution[3],
            genetico.g_best.solution[4],
            genetico.g_best.solution[5],
        )
        data_collected = {
            "V": potencial,
            "fitness": genetico.g_best.target.fitness,
            "AH3": genetico.g_best.solution[0],
            "AF3": genetico.g_best.solution[1],
            "AF5": genetico.g_best.solution[2],
            "A3N3": genetico.g_best.solution[3],
            "s": genetico.g_best.solution[4],
            "tau": genetico.g_best.solution[5],
            "lambda1": avalores[0],
            "lambda2": avalores[1],
        }
        found_solutions_rows.append(data_collected)

    found_solutions = pd.DataFrame(found_solutions_rows)
    found_solutions.to_csv("found_solutions__dS.csv")

def AdS_search():

    global vacua_parametros_AdS
    global genetico

    found_solutions_rows = []
    for i in range(1,3):
        print(f"Iteración {i}")
        #### Creación de un genético simple para minimización de la función ff
        genetico.solve(vacua_parametros_AdS)
        #### Creación de un genético simple para minimización de la función ff
        #### Imprimir solución
        print(f"Solución: {genetico.g_best.solution}, Fitness: {genetico.g_best.target.fitness}")
        #### Calcular los autovalores de la solución encontrada
        av=autovalores_VHess_AdS(
            genetico.g_best.solution[0],
            genetico.g_best.solution[1],
            genetico.g_best.solution[2],
            genetico.g_best.solution[3],
            genetico.g_best.solution[4],
            genetico.g_best.solution[5],
            genetico.g_best.solution[6],
        )
        potencial = potencial_eval_AdS(
            genetico.g_best.solution[0],
            genetico.g_best.solution[1],
            genetico.g_best.solution[2],
            genetico.g_best.solution[3],
            genetico.g_best.solution[4],
            genetico.g_best.solution[5],
            genetico.g_best.solution[6],
        )
        data_collected = {
            "V": potencial,
            "fitness": genetico.g_best.target.fitness,
            "AH3": genetico.g_best.solution[0],
            "AF3": genetico.g_best.solution[1],
            "AF5": genetico.g_best.solution[2],
            "A3N3": genetico.g_best.solution[3],
            "AD5": genetico.g_best.solution[4],
            "s": genetico.g_best.solution[5],
            "tau": genetico.g_best.solution[6],
            "lambda1": av[0],
            "lambda2": av[1],
        }
        found_solutions_rows.append(data_collected)

    found_solutions = pd.DataFrame(found_solutions_rows)
    found_solutions.to_csv("found_solutions_AdS.csv")


if __name__ == "__main__":
    #dS_search()
    AdS_search()
