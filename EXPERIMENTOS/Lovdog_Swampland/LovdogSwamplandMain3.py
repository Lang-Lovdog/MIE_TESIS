from lvdsl.bioinspired import  defs
import datetime

dst_dir=""
recover=False

def sys_notibash_log(simulation, startend=True):
    import datetime
    import os
    try:
        command = "alarma 1s "
        started_at = datetime.datetime.now().strftime("%Y:%m:%d-%H:%M:%S")
        mesage  = f"{simulation} started at {started_at}" if startend else f"{simulation} finished at {started_at}"
        os.system(f"{command} \"{mesage}\"", )
    except Exception:
        pass


params_ga = {
        "epoch"       : [50, 100, 200, 300, 400],
        "pop_size"    : [20,  60, 100, 140, 180, 220, 260, 300],
        "pc"          : [i/100 for i in range(0, 100, 2)],
        "pm"          : [i/100 for i in range(0, 100, 2)]
    }

params_pso = {
        "epoch"       : [50, 100, 200, 300, 400],
        "pop_size"    : [20,  60, 100, 140, 180, 220, 260, 300],
        "c1"          : [0.02, 0.04, 0.08, 0.2, 0.4],
        "c2"          : [0.02, 0.04, 0.08, 0.2, 0.4]
    }

params_iwo = {
    "epoch"           : [50, 100, 200, 300, 400],
    "pop_size"        : [20,  60, 100, 140, 180, 220, 260, 300],
    "seed_min"        : [1, 2, 3, 4, 5, 6, 7, 8, 9],
    "seed_max"        : [4, 5, 6, 7, 8, 9, 10],
    "exponent"        : [2, 3, 4],
    "sigma_start"     : [0.5, 1.0, 1.5, 2.0, 2.5],
    "sigma_end"       : [0.05, 0.10, 0.15, 0.20, 0.25]
}

params_umda = {
    "epoch"           : [50, 100, 200, 300, 400],
    "pop_size"        : [20,  60, 100, 140, 180, 220, 260, 300],
    "selection_ratio" : [i/100 for i in range(1, 100, 2)]
}

params_pbil = {
    "epoch"           : [50, 100, 200, 300, 400],
    "pop_size"        : [20,  60, 100, 140, 180, 220, 260, 300],
    "learning_rate"   : [i/100.00 for i in range(1, 200, 1)]
}

params_aco = {
    "epoch"           : [50, 100, 200, 300, 400],
    "pop_size"        : [20,  60, 100, 140, 180, 220, 260, 300],
    "sample_count"    : [20,  60, 100, 140, 180, 220, 260, 300],
    "intent_factor"   : [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
    "zeta"            : [0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2]
}

params_vcs = {
    "epoch"           : [50, 100, 200, 300, 400],
    "pop_size"        : [20,  60, 100, 140, 180, 220, 260, 300],
    "lamda"           : [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
    "sigma"           : [i/10 for i in range(10,50)]
}

params_aso = {
    "epoch"           : [50, 100, 200, 300, 400],
    "pop_size"        : [20,  60, 100, 140, 180, 220, 260, 300],
    "alpha"           : [i/10 for i in range(100,501,2)],
    "beta"            : [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
}


GridS={
    "GA"  : params_ga  ,
    "PSO" : params_pso ,
    "IWO" : params_iwo ,
    "UMDA": params_umda,
    "PBIL": params_pbil,
    "ACO" : params_aco ,
    "VCS" : params_vcs ,
    "ASO" : params_aso
}


### Built Grid for Randon Search

def build_grid(model, params):
    built_params=[]
    if model=="GA":
        for ep in params["epoch"]:
            for ps in params["pop_size"]:
                for pc in params["pc"]:
                    for pm in params["pm"]:
                        built_params.append({"epoch":ep, "pop_size":ps, "pc":pc, "pm":pm})
    if model=="PSO":
        for ep in params["epoch"]:
            for ps in params["pop_size"]:
                for c1 in params["c1"]:
                    for c2 in params["c2"]:
                        built_params.append({"epoch":ep, "pop_size":ps, "c1":c1, "c2":c2})

    if model=="IWO":
        for ep in params["epoch"]:
            for ps in params["pop_size"]:
                for seed_min in params["seed_min"]:
                    for seed_max in params["seed_max"]:
                        for exponent in params["exponent"]:
                            for sigma_start in params["sigma_start"]:
                                for sigma_end in params["sigma_end"]:
                                    built_params.append({"epoch":ep, "pop_size":ps, "seed_min":seed_min, "seed_max":seed_max, "exponent":exponent, "sigma_start":sigma_start, "sigma_end":sigma_end})

    if model == "UMDA":
       for ep in params["epoch"]:
           for ps in params["pop_size"]:
               for sr in params["selection_ratio"]:
                   built_params.append({"epoch":ep, "pop_size":ps, "selection_ratio":sr})

    if model == "PBIL":
        for ep in params["epoch"]:
            for ps in params["pop_size"]:
                for lr in params["learning_rate"]:
                    built_params.append({"epoch":ep, "pop_size":ps, "learning_rate":lr})

    if model == "ACO":
        for ep in params["epoch"]:
            for ps in params["pop_size"]:
                for sc in params["sample_count"]:
                    for ifa in params["intent_factor"]:
                        for z in params["zeta"]:
                            built_params.append({"epoch":ep, "pop_size":ps, "sample_count":sc, "intent_factor":ifa, "zeta":z})

    if model == "VCS":
        for ep in params["epoch"]:
            for ps in params["pop_size"]:
                for lb in params["lamda"]:
                    for s in params["sigma"]:
                        built_params.append({"epoch":ep, "pop_size":ps, "lamda":lb, "sigma":s})

    if model == "ASO":
        for ep in params["epoch"]:
            for ps in params["pop_size"]:
                for a in params["alpha"]:
                    for b in params["beta"]:
                        built_params.append({"epoch":ep, "pop_size":ps, "alpha":a, "beta":b})

    return built_params

def start_it(params):
    model_to_optimize, built_params_main, built_params_indx = params
    i=0
    for par in built_params_main:
        with open("log_RS.txt", "a") as f:
            this_moment = datetime.datetime.now().strftime("%Y:%m:%d-%H:%M:%S")
            f.write(f"{model_to_optimize} :: {built_params_indx[i]} started at {this_moment}\n")

        print(f"Testing {par}", flush=True)
        defs.set_name_suffix("_" + str(built_params_indx[i]))
        defs.run_model(
            model_name  = model_to_optimize,
            params      = par,
            csv_input   = "../CESAR-BRITO_ORIGINAL-DATA/Calibracion_lifting.csv",
            csv_format  = "Mathematica",
            lifting     = True,
            output      = True,
        )

        with open("lvdsl_outputs/log_RS.txt", "a") as f:
            this_moment = datetime.datetime.now().strftime("%Y:%m:%d-%H:%M:%S")
            f.write(f"{model_to_optimize} :: {built_params_indx[i]} ended at {this_moment}\n")

        i+=1


if __name__ == "__main__":
    import sys
    import random
    from   multiprocessing import Pool

    built_params_main = []
    built_params_indx = []

    ## This script only uses a value and a name for Random Search (RS)
    ### so to say ./Main GA 16 which will perform a RS over 16 hyper-parameter configurations for GA

    date = datetime.datetime.now().strftime("%Y%m%d")

    if len(sys.argv) > 2:
        model_to_optimize = sys.argv[1].upper()
        amount_to_test = int(sys.argv[2])
        built_params=build_grid(model_to_optimize, GridS[model_to_optimize])
        built_params_indx = random.sample([i for i in range(len(built_params))], amount_to_test)
        built_params_main = [built_params[i] for i in built_params_indx]
        print(f"{len(built_params)} models built | testing {amount_to_test}")
    else:
        print("No model specified use as: this_script OPTIMIZER_NAME_UPPERCASE [models to test]")
        print("Optimizers: GA, PSO, IWO:")
        for model_to_optimize in GridS.keys():
            print(f"{model_to_optimize}\t has \t{len(build_grid(model_to_optimize, GridS[model_to_optimize]))}\t poßible configurations.")
        exit(0)

    print(built_params_main)

    max_subprocesses = 4

    ## Making groups of {max_subprocesses} per group for multiprocessing
    pool_params = [
        (
            model_to_optimize,
            built_params_main[minp: minp+max_subprocesses],
            built_params_indx[minp: minp+max_subprocesses]
        ) for minp in range(0, len(built_params_main), max_subprocesses)
    ]

    print("\n" + "*"*50)
    __import__('pprint').pprint(pool_params)
    print("*"*50)


    with Pool() as pool:
        pool.map(start_it, pool_params)

