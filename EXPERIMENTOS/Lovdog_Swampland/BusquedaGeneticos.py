import mealpy as mp # type: ignore
import pandas as pd # type: ignore
from mealpy                import FloatVar, get_optimizer_by_name
from MetastableVacua       import fitness_function_mealpy          as ff1
from MetastableVacua       import fitness_function_AdS_mealpy      as ff2
from MetastableVacua       import fitness_function_coef_mealpy     as ff3
from MetastableVacua       import fitness_function_coef_AdS_mealpy as ff4
from MetastableVacua       import autovalores_VHess
from MetastableVacua       import autovalores_VHess_AdS
from MetastableVacua       import potencial_eval
from MetastableVacua       import potencial_eval_AdS
from MetastableVacua       import set_fixed_value
from test_fitness_function import datos_del_csv_mathematica        as from_csv
from test_fitness_function import variables                        as vnms      # Convierte del convenio de este proyecto al del de mathematica

### Datetime as DDMMYYYY for directory name
from datetime import datetime
import os
now = datetime.now()
dt_string = now.strftime("%d%m%Y")
dirname = "VacuaFound_" + dt_string

vacua_parametros__dS = {
    "obj_func": ff1,
    "bounds": FloatVar(
        #    AH3   AF3   AF5   A3N3    s      tau
        lb=[-100, -100, -100,  -100, 1e-20, 1e-20, ],
        ub=[ 100,  100,  100,-1e-20,     1,     1, ]
    ),
    "minmax": "min",
    "log_to": "MetastableVacuaReprise.log"
}

vacua_parametros_AdS = {
    "obj_func": ff2,
    "bounds": FloatVar(
        #    AH3   AF3   AF5   A3N3   AD5    s      tau
        lb=[-100, -100, -100,  -100, -100, 1e-20, 1e-20, ],
        ub=[ 100,  100,  100,-1e-20,  100,     1,     1, ]
    ),
    "minmax": "min",
    "log_to": "MetastableVacuaRepriseAdS.log"
}

vacua_parametros__dS_fv = {
    "obj_func": ff3,
    "bounds": FloatVar(
        #    AH3   AF3   AF5   A3N3 
        lb=[-100, -100, -100,  -100,],
        ub=[ 100,  100,  100,-1e-20,]
    ),
    "minmax": "min",
    "log_to": "MetastableVacuaReprise.log"
}

vacua_parametros_AdS_fv = {
    "obj_func": ff4,
    "bounds": FloatVar(
        #    AH3   AF3   AF5   A3N3   AD5
        lb=[-100, -100, -100,  -100, -100 ],
        ub=[ 100,  100,  100,-1e-20,  100 ]
    ),
    "minmax": "min",
    "log_to": "MetastableVacuaRepriseAdS.log"
}

genetico = mp.GA.BaseGA(epoch=50, pop_size=20, pc=0.9, pm=0.4)

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
            "V"         : potencial,
            "fitness"   : genetico.g_best.target.fitness,
            "AH3"       : genetico.g_best.solution[0],
            "AF3"       : genetico.g_best.solution[1],
            "AF5"       : genetico.g_best.solution[2],
            "A3N3"      : genetico.g_best.solution[3],
            "s"         : genetico.g_best.solution[4],
            "tau"       : genetico.g_best.solution[5],
            "lambda1"   : avalores[0],
            "lambda2"   : avalores[1],
            "taquiónico": "1" if min(avalores) < 0 else "0"
        }
        found_solutions_rows.append(data_collected)

    found_solutions = pd.DataFrame(found_solutions_rows)
    found_solutions.to_csv(f"{dirname}/found_solutions__dS.csv")

def AdS_search():

    global vacua_parametros_AdS
    global genetico

    found_solutions_rows = []
    for i in range(1,100):
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
            "fitness"   : genetico.g_best.target.fitness,
            "AH3"       : genetico.g_best.solution[0],
            "AF3"       : genetico.g_best.solution[1],
            "AF5"       : genetico.g_best.solution[2],
            "A3N3"      : genetico.g_best.solution[3],
            "AD5"       : genetico.g_best.solution[4],
            "s"         : genetico.g_best.solution[5],
            "tau"       : genetico.g_best.solution[6],
            "lambda1"   : av[0],
            "lambda2"   : av[1],
            "taquiónico": "1" if min(av) < 0 else "0",
        }
        found_solutions_rows.append(data_collected)

    found_solutions = pd.DataFrame(found_solutions_rows)
    found_solutions.to_csv(f"{dirname}/found_solutions_AdS.csv")

def dS_search_fixed_vars():

    global vacua_parametros__dS_fv
    global genetico

    csv_data = from_csv("../CESAR-BRITO_ORIGINAL-DATA/Calibracion_no_lifting.csv")

    k=0
    for row in csv_data.iterrows():
        row = row[1]

        set_fixed_value({
            "s"   : row[vnms["s"  ]],
            "tau" : row[vnms["tau"]],
        })

        found_solutions_rows = []
        for i in range(1,100):
            print(f"Iteración {i}")
            #### Creación de un genético simple para minimización de la función ff
            genetico.solve(vacua_parametros__dS_fv)
            #### Creación de un genético simple para minimización de la función ff
            #### Imprimir solución
            print(f"Solución: {genetico.g_best.solution}, Fitness: {genetico.g_best.target.fitness}")
            avalores = autovalores_VHess(
                genetico.g_best.solution[0],
                genetico.g_best.solution[1],
                genetico.g_best.solution[2],
                genetico.g_best.solution[3],
                row[vnms["s"  ]],
                row[vnms["tau"]],
            )
            potencial = potencial_eval(
                genetico.g_best.solution[0],
                genetico.g_best.solution[1],
                genetico.g_best.solution[2],
                genetico.g_best.solution[3],
                row[vnms["s"  ]],
                row[vnms["tau"]],
            )
            data_collected = {
                "V": potencial,
                "V_O"          : row[vnms["V"    ]],
                "fitness"      : genetico.g_best.target.fitness,
                "AH3"          : genetico.g_best.solution[0],
                "AH3_O"        : row[vnms["AH3"  ]],
                "AF3"          : genetico.g_best.solution[1],
                "AF3_O"        : row[vnms["AF3"  ]],
                "AF5"          : genetico.g_best.solution[2],
                "AF5_O"        : row[vnms["AF5"  ]],
                "A3N3"         : genetico.g_best.solution[3],
                "A3N3_O"       : row[vnms["A3N3" ]],
                "s"            : row[vnms["s"  ]],
                "tau"          : row[vnms["tau"]],
                "lambda1"      : avalores[0],
                "lambda1_O"    : row[vnms["Eig1"]],
                "lambda2"      : avalores[1],
                "lambda2_O"    : row[vnms["Eig2"]],
                "taquiónico"   : "1" if min(avalores) < 0 else "0",
                "taquiónico_O" : "1" if min([row[vnms["Eig1"]],row[vnms["Eig2"]]]) < 0 else "0",
            }
            found_solutions_rows.append(data_collected)

        found_solutions = pd.DataFrame(found_solutions_rows)
        found_solutions.to_csv(f"{dirname}/found_solutions__dS_fv_{k}.csv")
        k+=1

def AdS_search_fixed_vars():

    global vacua_parametros_AdS
    global genetico

    csv_data = from_csv("../CESAR-BRITO_ORIGINAL-DATA/Calibracion_lifting.csv", True)

    k=0
    for row in csv_data.iterrows():
        row = row[1]

        set_fixed_value({
            "s"   : row[vnms["s"  ]],
            "tau" : row[vnms["tau"]],
        })

        found_solutions_rows = []
        for i in range(1,100):
            print(f"Iteración {i}")
            #### Creación de un genético simple para minimización de la función ff
            genetico.solve(vacua_parametros_AdS_fv)
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
                row[vnms["s"  ]],
                row[vnms["tau"]],
            )
            potencial = potencial_eval_AdS(
                genetico.g_best.solution[0],
                genetico.g_best.solution[1],
                genetico.g_best.solution[2],
                genetico.g_best.solution[3],
                genetico.g_best.solution[4],
                row[vnms["s"  ]],
                row[vnms["tau"]],
            )
            data_collected = {
                "V": potencial,
                "V_O"          : row[vnms["V"    ]],
                "fitness"      : genetico.g_best.target.fitness,
                "AH3"          : genetico.g_best.solution[0],
                "AH3_O"        : row[vnms["AH3"  ]],
                "AF3"          : genetico.g_best.solution[1],
                "AF3_O"        : row[vnms["AF3"  ]],
                "AF5"          : genetico.g_best.solution[2],
                "AF5_O"        : row[vnms["AF5"  ]],
                "A3N3"         : genetico.g_best.solution[3],
                "A3N3_O"       : row[vnms["A3N3" ]],
                "AD5"          : genetico.g_best.solution[4],
                "AD5_O"        : row[vnms["AD5"  ]],
                "s"            : row[vnms["s"  ]],
                "tau"          : row[vnms["tau"]],
                "lambda1"      : av[0],
                "lambda1_O"    : row[vnms["Eig1"]],
                "lambda2"      : av[1],
                "lambda2_O"    : row[vnms["Eig2"]],
                "taquiónico"   : "1" if min(av) < 0 else "0",
                "taquiónico_O" : "1" if min([row[vnms["Eig1"]],row[vnms["Eig2"]]]) < 0 else "0",
            }
            found_solutions_rows.append(data_collected)

        found_solutions = pd.DataFrame(found_solutions_rows)
        found_solutions.to_csv(f"{dirname}/found_solutions_AdS_fv_{k}.csv")
        k+=1


if __name__ == "__main__":
    os.makedirs(dirname, exist_ok=True)
    AdS_search()
    AdS_search_fixed_vars()
    dS_search()
    dS_search_fixed_vars()
