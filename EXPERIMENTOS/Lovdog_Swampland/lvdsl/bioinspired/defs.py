import mealpy as mp # type: ignore
import pandas as pd # type: ignore
from mealpy                    import FloatVar
from lvdsl.k_theory.potentials import fitness_function_nolift_mealpy               as ff1
from lvdsl.k_theory.potentials import fitness_function_lift_mealpy                 as ff2
from lvdsl.k_theory.potentials import fitness_function_fixedmoduli_nolift_mealpy   as ff3
from lvdsl.k_theory.potentials import fitness_function_fixedmoduli_lift_mealpy     as ff4
from lvdsl.bioinspired.EDAs    import UMDA
from lvdsl.bioinspired.EDAs    import PBIL
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

precision_decimal = 30

def get_precision_decimal():
    return precision_decimal

def set_precision_decimal(val : int):
    global precision_decimal
    precision_decimal = val

def setup_filename():
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y")
    dirname = "VacuaFound_" + dt_string
    return dirname

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

    vacua_parametros_nolift = {
        "obj_func": ff1,
        "bounds": FloatVar(
            #    AH3   AF3   AF5   A3N3    s      tau
            lb=lb_nolift,
            ub=ub_nolift
        ),
        "minmax": "min",
        "log_to": "MetastableVacuaReprise.log"
    }

    vacua_parametros___lift = {
        "obj_func": ff2,
        "bounds": FloatVar(
            #    AH3   AF3   AF5   A3N3   AD5    s      tau
            lb=lb___lift,
            ub=ub___lift
        ),
        "minmax": "min",
        "log_to": "MetastableVacuaRepriseAdS.log"
    }

    vacua_parametros_nolift_fv = {
        "obj_func": ff3,
        "bounds": FloatVar(
            #    AH3   AF3   AF5   A3N3 
            lb=lb_nomoduli_nolift,
            ub=ub_nomoduli_nolift
        ),
        "minmax": "min",
        "log_to": "MetastableVacuaReprise.log"
    }

    vacua_parametros___lift_fv = {
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
    params={
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
    def get_model(self, name):
        if name == "GA":
            return mp.GA.BaseGA(
                epoch    = self.params.get("ga").get("epoch"),
                pop_size = self.params.get("ga").get("pop_size"),
                pc       = self.params.get("ga").get("pc"),
                pm       = self.params.get("ga").get("pm")
            )
        elif name == "PSO":
            return mp.PSO.AIW_PSO(
                epoch    = self.params.get("pso").get("epoch"),
                pop_size = self.params.get("pso").get("pop_size"),
                c1       = self.params.get("pso").get("c1"),
                c2       = self.params.get("pso").get("c2")
            )
        elif name == "UMDA":
            return UMDA(
                epoch           = self.params.get("eda").get("epoch"),
                pop_size        = self.params.get("eda").get("pop_size"),
                selection_ratio = self.params.get("eda").get("selection_ratio")
            )
        elif name == "PBIL":
            return PBIL(
                epoch         = self.params.get("eda").get("epoch"),
                pop_size      = self.params.get("eda").get("pop_size"),
                learning_rate = self.params.get("eda").get("learning_rate"),
            )
        elif name == "IWO":
            return mp.IWO.OriginalIWO(
                epoch       = self.params.get("iwo").get("epoch"),
                pop_size    = self.params.get("iwo").get("pop_size"),
                seed_min    = self.params.get("iwo").get("seed_min"),
                seed_max    = self.params.get("iwo").get("seed_max"),
                exponent    = self.params.get("iwo").get("exponent"),
                sigma_start = self.params.get("iwo").get("sigma_start"),
                sigma_end   = self.params.get("iwo").get("sigma_end")
            )
        elif name == "ACO":
            return mp.ACOR.OriginalACOR(
                epoch         = self.params.get("aco").get("epoch"),
                pop_size      = self.params.get("aco").get("pop_size"),
                sample_count  = self.params.get("aco").get("sample_count"),
                intent_factor = self.params.get("aco").get("intent_factor"),
                zeta          = self.params.get("aco").get("zeta")
        )
        elif name == "VCS":
            return mp.VCS.DevVCS(
                epoch    = self.params.get("vcs").get("epoch"),
                pop_size = self.params.get("vcs").get("pop_size"),
                lamda    = self.params.get("vcs").get("lamda"),
                sigma    = self.params.get("vcs").get("sigma")
            )
        elif name == "ASO":
            return mp.ASO.OriginalASO(
                epoch    = self.params.get("aso").get("epoch"),
                pop_size = self.params.get("aso").get("pop_size"),
                alpha    = self.params.get("aso").get("alpha"),
                beta     = self.params.get("aso").get("beta")
            )
        else:
            print("Model not found: ", name)


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

