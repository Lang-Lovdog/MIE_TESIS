from lvdsl.bioinspired import  defs
import sys

dst_dir=""
row_start=0

def run_ga():
  ## GA
  defs.run_model(
      model_name  = "GA",
      csv_input   = "../CESAR-BRITO_ORIGINAL-DATA/Calibracion_lifting.csv",
      csv_format  = "Mathematica",
      lifting     = True,
      output      = True,
      start_row   = row_start,
      destination = dst_dir

  )


def run_pso():
  ## PSO
  defs.run_model(
      model_name  = "PSO",
      csv_input   = "../CESAR-BRITO_ORIGINAL-DATA/Calibracion_lifting.csv",
      csv_format  = "Mathematica",
      lifting     = True,
      output      = True,
      start_row   = row_start,
      destination = dst_dir

  )


def run_umda():
  ## UMDA
  defs.run_model(
      model_name  = "UMDA",
      csv_input   = "../CESAR-BRITO_ORIGINAL-DATA/Calibracion_lifting.csv",
      csv_format  = "Mathematica",
      lifting     = True,
      output      = True,
      start_row   = row_start,
      destination = dst_dir

  )


def run_pbil():
  ## PBIL
  defs.run_model(
      model_name  = "PBIL",
      csv_input   = "../CESAR-BRITO_ORIGINAL-DATA/Calibracion_lifting.csv",
      csv_format  = "Mathematica",
      lifting     = True,
      output      = True,
      start_row   = row_start,
      destination = dst_dir

  )


def run_aco():
  ## ACO
  defs.run_model(
      model_name  = "ACO",
      csv_input   = "../CESAR-BRITO_ORIGINAL-DATA/Calibracion_lifting.csv",
      csv_format  = "Mathematica",
      lifting     = True,
      output      = True,
      start_row   = row_start,
      destination = dst_dir

  )


def run_iwo():
  ## IWO
  defs.run_model(
      model_name  = "IWO",
      csv_input   = "../CESAR-BRITO_ORIGINAL-DATA/Calibracion_lifting.csv",
      csv_format  = "Mathematica",
      lifting     = True,
      output      = True,
      start_row   = row_start,
      destination = dst_dir

  )


def run_vcs():
  ## VCS
  defs.run_model(
      model_name  = "VCS",
      csv_input   = "../CESAR-BRITO_ORIGINAL-DATA/Calibracion_lifting.csv",
      csv_format  = "Mathematica",
      lifting     = True,
      output      = True,
      start_row   = row_start,
      destination = dst_dir

  )


def run_aso():
  ## ASO
  defs.run_model(
      model_name  = "ASO",
      csv_input   = "../CESAR-BRITO_ORIGINAL-DATA/Calibracion_lifting.csv",
      csv_format  = "Mathematica",
      lifting     = True,
      output      = True,
      start_row   = row_start,
      destination = dst_dir
  )

if __name__ == "__main__":
    import os
    import datetime

    #global dst_dir
    #global row_start

    if len(sys.argv) < 2:
        print("Uso: python LovdogSwamplandMain.py <MODELO> [-d=<OUTPUT DIR>] [-s=<START ROW>]")
        print("Modelos disponibles: GA, PSO, UMDA, PBIL, ACO, IWO, VCS, ASO")
        sys.exit(1)

    for arg in sys.argv:
        if arg.startswith("-d"):
            dst_dir = arg.split("=")[1]
        elif arg.startswith("-s"):
            row_start = int(arg.split("=")[1])
        else:
            simulation = arg.upper()

    models = {
        "GA":   run_ga,
        "PSO":  run_pso,
        "UMDA": run_umda,
        "PBIL": run_pbil,
        "ACO":  run_aco,
        "IWO":  run_iwo,
        "VCS":  run_vcs,
        "ASO":  run_aso,
    }

    if simulation in models:
        ## Send alarm if alarma command exists
        #### alarma 1s "{model} started at {full_date_time}"
        try:
            command = "alarma 1s "
            started_at = datetime.datetime.now().strftime("%Y:%m:%d-%H:%M:%S")
            mesage  = f"{simulation} started at {started_at}"
            os.system(f"{command} \"{mesage}\"")
        except Exception:
            pass

        #### Run model
        models[simulation]()

        ### Stop model
        try:
            command = "alarma 1s "
            ended_at = datetime.datetime.now().strftime("%Y:%m:%d-%H:%M:%S")
            mesage  = f"{simulation} ended at {ended_at}"
            os.system(f"{command} \"{mesage}\"")
        except Exception:
            pass
    else:
        print(f"Modelo '{simulation}' no reconocido.")
        print("Disponibles:", ", ".join(models.keys()))
        sys.exit(1)


