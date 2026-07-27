from lvdsl.bioinspired import  defs

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
        "epoch"    : [50, 100, 200, 300, 400],
        "pop_size" : [20,  60, 100, 140, 180, 220, 260, 300],
        "pc"       : [0.1, 0.3, 0.5, 0.7, 0.9],
        "pm"       : [0.2, 0.4, 0.6, 0.8]
    }

params_pso = {
        "epoch"    : [50, 100, 200, 300, 400],
        "pop_size" : [20,  60, 100, 140, 180, 220, 260, 300],
        "c1"       : [0.02, 0.04, 0.08, 0.2, 0.4],
        "c2"       : [0.02, 0.04, 0.08, 0.2, 0.4]
    }

params_iwo = {
    "epoch"        : [50, 100, 200, 300, 400],
    "pop_size"     : [20,  60, 100, 140, 180, 220, 260, 300],
    "seed_min"     : [1, 2, 3, 4, 5, 6, 7, 8, 9],
    "seed_max"     : [4, 5, 6, 7, 8, 9, 10],
    "exponent"     : [2, 3, 4],
    "sigma_start"  : [0.5, 1.0, 1.5, 2.0, 2.5],
    "sigma_end"    : [0.05, 0.10, 0.15, 0.20, 0.25]
}

GridS={
    "GA"  : params_ga,
    "PSO" : params_pso,
    "IWO" : params_iwo
}

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

    return built_params


if __name__ == "__main__":
    import sys

    built_params_main = []
    built_params_indx = []

    if len(sys.argv) > 2:
        model_to_optimize = sys.argv[1]
        built_params=build_grid(model_to_optimize, GridS[model_to_optimize])
        print(f"{len(built_params)} models built")
        if sys.argv[2]=="-1":
            exit(0)
        for element in sys.argv[2:]:
            built_params_indx.append(element)
            built_params_main.append(built_params[int(element)])
    elif len(sys.argv) > 1:
        model_to_optimize = sys.argv[1]
        built_params_main=build_grid(model_to_optimize, GridS[model_to_optimize])
        built_params_indx=[str(i) for i in range(len(built_params_main))]
        print(f"{len(built_params_main)} models built")
    else:
        print("No model specified use as: this_script OPTIMIZER_NAME_UPPERCASE [models to test]")
        print("Optimizers: GA, PSO, IWO:")
        for model_to_optimize in GridS.keys():
            print(f"{model_to_optimize} has \t{len(build_grid(model_to_optimize, GridS[model_to_optimize]))} possible configurations.")
        exit(0)
    print(f'{len(built_params_main)} to test')

    print(built_params_main)

    i=0
    for par in built_params_main:
        sys_notibash_log(model_to_optimize+" "+built_params_indx[i])
        print(f"Testing {par}", flush=True)
        defs.set_name_suffix(built_params_indx[i])
        defs.run_model(
            model_name  = model_to_optimize,
            params      = par,
            csv_input   = "../CESAR-BRITO_ORIGINAL-DATA/Calibracion_lifting.csv",
            csv_format  = "Mathematica",
            lifting     = True,
            output      = True,
        )
        sys_notibash_log(model_to_optimize+" "+built_params_indx[i], False)
        i+=1

