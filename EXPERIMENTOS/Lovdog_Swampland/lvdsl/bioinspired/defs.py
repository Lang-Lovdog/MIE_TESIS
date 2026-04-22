import mealpy as mp # type: ignore
import pandas as pd # type: ignore
from mealpy                    import FloatVar
from lvdsl.k_theory.potentials import fitness_function_nolift_mealpy               as ff1
from lvdsl.k_theory.potentials import fitness_function_lift_mealpy                 as ff2
from lvdsl.k_theory.potentials import fitness_function_fixedmoduli_nolift_mealpy   as ff3
from lvdsl.k_theory.potentials import fitness_function_fixedmoduli_lift_mealpy     as ff4
from lvdsl.k_theory.vars       import V_liftingHess_eig_lambda
from lvdsl.k_theory.vars       import V_lifting_lambda
from lvdsl.k_theory.vars       import set_fixed_value
from lvdsl.bioinspired.EDAs    import UMDA
from lvdsl.bioinspired.EDAs    import PBIL
from lvdsl.data.from_csv       import read_mathematica_format
from lvdsl.data.from_csv       import read_native_format
from lvdsl.data.from_csv       import save_comparative_csv
from lvdsl.data.from_csv       import variables                                    as vnms
#from lvdsl.k_theory.potentials import autovalores_VHess
#from lvdsl.k_theory.potentials import autovalores_VHess_AdS
#from lvdsl.k_theory.potentials import potencial_eval
#from lvdsl.k_theory.potentials import potencial_eval_AdS
#from lvdsl.k_theory.potentials import set_fixed_value
#from test_fitness_function import datos_del_csv_mathematica                        as from_csv
#from test_fitness_function import variables                                        as vnms      # Convierte del convenio de este proyecto al del de mathematica

### Datetime as DDMMYYYY for directory name
from datetime import datetime
import os


def setup_filename():
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y_%H")
    dirname = "lvdsl_outputs/VacuaFound_" + dt_string
    return dirname

def build_dir_name(model_name : str):
    dir_time=setup_filename()
    dirname = dir_time + "/" + model_name
    return dirname

def write_model_description(model, dirname : str):
    if not os.path.exists(dirname):
        print(f"WARN: {dirname} not found, creating it.")
        os.makedirs(dirname)
    filename = dirname + "/model_description.txt"
    with open(filename, "w") as f:
        print(model, file=f)

class natureinspired_problems_k_theory:

    AH3_limits  = { "lb": -100    , "ub": 100     }
    AF3_limits  = { "lb": -100    , "ub": 100     }
    AF5_limits  = { "lb": -100    , "ub": 100     }
    A3N3_limits = { "lb": -100    , "ub":  -1e-20 }
    AD5_limits  = { "lb": -100    , "ub": 100     }
    s_limits    = { "lb":    1e-20, "ub":   1     }
    tau_limits  = { "lb":    1e-20, "ub":   1     }

    lb___lift=[AH3_limits.get("lb"), AF3_limits.get("lb"), AF5_limits.get("lb"), A3N3_limits.get("lb"), AD5_limits.get("lb"), s_limits.get("lb"), tau_limits.get("lb")]
    ub___lift=[AH3_limits.get("ub"), AF3_limits.get("ub"), AF5_limits.get("ub"), A3N3_limits.get("ub"), AD5_limits.get("ub"), s_limits.get("ub"), tau_limits.get("ub")]
    lb_nolift=[AH3_limits.get("lb"), AF3_limits.get("lb"), AF5_limits.get("lb"), A3N3_limits.get("lb"),                       s_limits.get("lb"), tau_limits.get("lb")]
    ub_nolift=[AH3_limits.get("ub"), AF3_limits.get("ub"), AF5_limits.get("ub"), A3N3_limits.get("ub"),                       s_limits.get("ub"), tau_limits.get("ub")]
    ## No moduli version
    lb_nomoduli___lift=[AH3_limits.get("lb"), AF3_limits.get("lb"), AF5_limits.get("lb"), A3N3_limits.get("lb"), AD5_limits.get("lb")]
    ub_nomoduli___lift=[AH3_limits.get("ub"), AF3_limits.get("ub"), AF5_limits.get("ub"), A3N3_limits.get("ub"), AD5_limits.get("ub")]
    lb_nomoduli_nolift=[AH3_limits.get("lb"), AF3_limits.get("lb"), AF5_limits.get("lb"), A3N3_limits.get("lb"),                     ]
    ub_nomoduli_nolift=[AH3_limits.get("ub"), AF3_limits.get("ub"), AF5_limits.get("ub"), A3N3_limits.get("ub"),                     ]

    vacua_parameters_nolift = {
        "obj_func": ff1,
        "bounds": FloatVar(
            #    AH3   AF3   AF5   A3N3    s      tau
            lb=lb_nolift,
            ub=ub_nolift
        ),
        "minmax": "min",
        "log_to": "MetastableVacuaReprise.log"
    }

    vacua_parameters___lift = {
        "obj_func": ff2,
        "bounds": FloatVar(
            #    AH3   AF3   AF5   A3N3   AD5    s      tau
            lb=lb___lift,
            ub=ub___lift
        ),
        "minmax": "min",
        "log_to": "MetastableVacuaRepriseAdS.log"
    }

    vacua_parameters_nolift_fv = {
        "obj_func": ff3,
        "bounds": FloatVar(
            #    AH3   AF3   AF5   A3N3 
            lb=lb_nomoduli_nolift,
            ub=ub_nomoduli_nolift
        ),
        "minmax": "min",
        "log_to": "MetastableVacuaReprise.log"
    }

    vacua_parameters___lift_fv = {
        "obj_func": ff4,
        "bounds": FloatVar(
            #    AH3   AF3   AF5   A3N3   AD5
            lb=lb_nomoduli___lift,
            ub=ub_nomoduli___lift
        ),
        "minmax": "min",
        "log_to": "MetastableVacuaRepriseAdS.log"
    }


class natureinspired_models:
    def __init__ (self):
        self.params={
            "ga": {
                "epoch":50,
                "pop_size":20,
                "pc":0.9,
                "pm":0.4
            },
            "pso": {
                "epoch":50,
                "pop_size":20,
                "c1":2.05,
                "c2":2.05
            },
            "eda": {
                "epoch": 100,
                "pop_size": 50,
                "learning_rate": 0.1,
                "selection_ratio": 0.2,
                "p_mutation": 0.05,
                "p_external": 0.02
            },
            "aco": {
                "epoch" : 10000,
                "pop_size" : 100,
                "sample_count" : 25,
                "intent_factor" : 0.5,
                "zeta" : 1.0
            },
            "iwo": {
                "epoch" : 10000,
                "pop_size" : 100,
                "seed_min" : 2,
                "seed_max" : 10,
                "exponent" : 2,
                "sigma_start" : 1.0,
                "sigma_end" : 0.01
            },
            "vcs": {
                "epoch": 10000,
                "pop_size": 100,
                "lamda": 0.5,
                "sigma": 1.5
            },
            "aso": {
                "epoch": 10000,
                "pop_size": 100,
                "alpha": 10,
                "beta": 0.2
            },
        }

    def set_model_param(self, name, param, value):
        if type(name) is list or type(name) is tuple:
            for n in name:
                self.set_model_param(n, param, value)
            return
        else:
            self.params[name][param] = value

    def get_model(self, name):
        if name == "GA":
            return_model = mp.GA.BaseGA(
                epoch    = self.params.get("ga").get("epoch"),
                pop_size = self.params.get("ga").get("pop_size"),
                pc       = self.params.get("ga").get("pc"),
                pm       = self.params.get("ga").get("pm")
            )
        elif name == "PSO":
            return_model = mp.PSO.AIW_PSO(
                epoch    = self.params.get("pso").get("epoch"),
                pop_size = self.params.get("pso").get("pop_size"),
                c1       = self.params.get("pso").get("c1"),
                c2       = self.params.get("pso").get("c2")
            )
        elif name == "UMDA":
            return_model = UMDA(
                epoch           = self.params.get("eda").get("epoch"),
                pop_size        = self.params.get("eda").get("pop_size"),
                selection_ratio = self.params.get("eda").get("selection_ratio")
            )
        elif name == "PBIL":
            return_model = PBIL(
                epoch         = self.params.get("eda").get("epoch"),
                pop_size      = self.params.get("eda").get("pop_size"),
                learning_rate = self.params.get("eda").get("learning_rate"),
            )
        elif name == "IWO":
            return_model = mp.IWO.OriginalIWO(
                epoch       = self.params.get("iwo").get("epoch"),
                pop_size    = self.params.get("iwo").get("pop_size"),
                seed_min    = self.params.get("iwo").get("seed_min"),
                seed_max    = self.params.get("iwo").get("seed_max"),
                exponent    = self.params.get("iwo").get("exponent"),
                sigma_start = self.params.get("iwo").get("sigma_start"),
                sigma_end   = self.params.get("iwo").get("sigma_end")
            )
        elif name == "ACO":
            return_model = mp.ACOR.OriginalACOR(
                epoch         = self.params.get("aco").get("epoch"),
                pop_size      = self.params.get("aco").get("pop_size"),
                sample_count  = self.params.get("aco").get("sample_count"),
                intent_factor = self.params.get("aco").get("intent_factor"),
                zeta          = self.params.get("aco").get("zeta")
        )
        elif name == "VCS":
            return_model = mp.VCS.DevVCS(
                epoch    = self.params.get("vcs").get("epoch"),
                pop_size = self.params.get("vcs").get("pop_size"),
                lamda    = self.params.get("vcs").get("lamda"),
                sigma    = self.params.get("vcs").get("sigma")
            )
        elif name == "ASO":
            return_model = mp.ASO.OriginalASO(
                epoch    = self.params.get("aso").get("epoch"),
                pop_size = self.params.get("aso").get("pop_size"),
                alpha    = self.params.get("aso").get("alpha"),
                beta     = self.params.get("aso").get("beta")
            )
        else:
            print("Model not found: ", name)
            return
        return [ return_model, build_dir_name(name) ]

def run_model(
    model_name  : str,
    params      : dict ={}       ,
    csv_input   : str  =""       ,
    csv_format  : str  ="Native" ,
    lifting     : bool =True     ,
    output      : bool =False    ,
    iterations  : int  =100
):
    ni_models_object = natureinspired_models()
    if params is not None:
        for param, value in params.items():
            ni_models_object.set_model_param(model_name, param, value)
    model_instance, out_dir = ni_models_object.get_model(model_name)
    #### If integrated CSV
    if csv_input is not None:
        if   csv_format == "Native":
            df = read_native_format(csv_input)
        elif csv_format == "Mathematica":
            df = read_mathematica_format(csv_input, D5_Fluxes=lifting)
        else:
            print("CSV format not supported: ", csv_format)
            return
        if "AD5" not in df.columns and lifting:
            print("lifting: No AD5 column found")
            return
        if output:
            write_model_description(model_instance, out_dir)
        fixed = [ "s", "tau" ]
        for ridx,row in df.iterrows():
            set_fixed_value({
                "s"   : row[vnms["s"  ]],
                "tau" : row[vnms["tau"]],
            })
            s, tau = row[vnms["s"  ]], row[vnms["tau"]]
            problem_to_optimize = natureinspired_problems_k_theory.vacua_parameters___lift_fv
            found_solutions = []
            for fidx in range(iterations):
                print(f"Registro {ridx} Iteración {fidx}")
                #### Creación de un genético simple para minimización de la función ff
                result = model_instance.solve(problem_to_optimize)
                if hasattr(model_instance, 'g_best'):
                    best_solution = model_instance.g_best.solution
                    best_fitness  = model_instance.g_best.target.fitness
                else:
                    best_solution, best_fitness = result
                #### Creación de un genético simple para minimización de la función ff
                #### Imprimir solución
                print(f"Solución: {best_solution}, Fitness: {best_fitness}")
                AH3, AF3, AF5, A3N3, AD5 = best_solution
                avalores  = V_liftingHess_eig_lambda(AH3, AF3, AF5, A3N3, AD5, tau, s)
                potencial = V_lifting_lambda        (AH3, AF3, AF5, A3N3, AD5, tau, s)
                found_solutions.append({
                    "V"         : potencial       ,
                    "fitness"   : best_fitness    ,
                    "AH3"       : best_solution[0],
                    "AF3"       : best_solution[1],
                    "AF5"       : best_solution[2],
                    "A3N3"      : best_solution[3],
                    "AD5"       : best_solution[4],
                    "s"         : s               ,
                    "tau"       : tau             ,
                    "lambda1"   : avalores[0]     ,
                    "lambda2"   : avalores[1]     ,
                    "taquiónico": "1" if min(avalores) < 0 else "0"
                })
                if output and fidx % 10 == 0:
                    found_solutions_tmp = pd.DataFrame(found_solutions)
                    out_filename= f"{out_dir}/{model_name}-{ridx:04d}.csv"
                    save_comparative_csv(
                        found_solutions_tmp   ,
                        df                    ,
                        ridx                  ,
                        out_filename          ,
                        fixed_elements = fixed
                    )
            if output:
                found_solutions = pd.DataFrame(found_solutions)
                out_filename= f"{out_dir}/{model_name}-{ridx:04d}.csv"
                save_comparative_csv(
                    found_solutions       ,
                    df                    ,
                    ridx                  ,
                    out_filename          ,
                    fixed_elements = fixed
                )
    #### If full search



if __name__ == "__main__":
    print("Problems and Models definitions")
    Models=natureinspired_models()
    print("Model GA")
    print(Models.get_model("GA"))
    print("Model PSO")
    print(Models.get_model("PSO"))
    print("Model UMDA")
    print(Models.get_model("UMDA"))
    print("Model PBIL")
    print(Models.get_model("PBIL"))
    print("Model ACO")
    print(Models.get_model("ACO"))
    print("Model IWO")
    print(Models.get_model("IWO"))
    print("Model VCS")
    print(Models.get_model("VCS"))
    print("Model ASO")
    print(Models.get_model("ASO"))

