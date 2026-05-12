from lvdsl.bioinspired import  defs

dst_dir=""
recover=False

defs.set_full_datetime()


params_ga = {
        "epoch":   [50, 100, 200, 300, 400],
        "pop_size":[20,  60, 100, 140, 180, 220, 260, 300],
        "pc":[0.1, 0.3, 0.5, 0.7, 0.9],
        "pm":[0.2, 0.4, 0.6, 0.8]
    }

built_params=[]

for ep in params_ga["epoch"]:
    for ps in params_ga["pop_size"]:
        for pc in params_ga["pc"]:
            for pm in params_ga["pm"]:
                built_params.append({"epoch":ep, "pop_size":ps, "pc":pc, "pm":pm})


if __name__ == "__main__":
    import sys

    print(f"{len(built_params)} models built")
    built_params_main = []

    if len(sys.argv) > 1:
        for element in sys.argv[1:]:
            built_params_main.append(built_params[int(element)])
    else:
        built_params_main = built_params
    print(f'{len(built_params_main)} to test')

    print(built_params_main)

    ##

    for par in built_params_main:
        print(f"Testing {par}")
        defs.run_model(
            model_name  = "GA",
            params      = par,
            csv_input   = "../CESAR-BRITO_ORIGINAL-DATA/Calibracion_lifting.csv",
            csv_format  = "Mathematica",
            lifting     = True,
            output      = True,
        )

