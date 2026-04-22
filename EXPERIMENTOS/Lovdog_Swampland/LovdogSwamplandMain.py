from lvdsl.bioinspired import  defs

defs.run_model(
    model_name  = "PSO",
    csv_input   = "../CESAR-BRITO_ORIGINAL-DATA/Calibracion_lifting.csv",
    csv_format  = "Mathematica",
    lifting     = True,
    output      = True
)
