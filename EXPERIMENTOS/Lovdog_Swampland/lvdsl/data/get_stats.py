## Este script tiene la finalidad de hacer un conteo de las soluciones obtenidas en las carpetas VacuaFound.
## Las estadísticas relevantes al momento serán
##   - Número de soluciones totales
##   - Número de soluciones taquiónicas
##   - Número de soluciones no taquiónicas
##   - Relación de soluciones taquiónico/total
##   - Medidas de tendencia central por campo (en el mismo csv)
##   - Medidas de tendencia central por campo (de todos los csv en conjunto, separados por modelo)

### Para hacer funcionar este script tendrá una función que recibirá el directorio a analizar


from ..xp import xp
import pandas
import os
import re

statistics={
    "total_solutions"     : 0,
    "taquionic_solutions" : 0,
    "negative_V"          : 0,
    "positive_V"          : 0,
    "negative_A3N3"       : 0,
    "positive_A3N3"       : 0
}


#### La estructura del directorio se supone de la forma:
#### |--- lvdsl_outputs/
#### |=-
#### |--- ;VacuaFound_[DDMMYYYY]_[HH]/; > Las salidas de la búsqueda metaheurística.||
#### |=-
#### |----- ;[MODEL];/
#### |=-
#### |-- __this__dir__
#### |-- ;[MODEL]-[4d][.csv].csv; > Resultados de la búsqueda metaheurística. ||
#### |==
#### |==
#### |==

def get_stats(directory):
    pass

def get_model_dirs(directory):
    model_dirs : list[str] = []
    for filename in os.listdir(directory):
        if os.path.isdir(directory+"/"+filename):
            model_dirs.append(filename)
    return model_dirs

def get_dataframes(directory):
    dataframes_list : list[pandas.DataFrame] = []
    for filename in os.listdir(directory):
        ## Corroboraremos que el formato sea el correcto para evitar archivos no deseados
        ## Ej: AG-0002.csv
        ## Ej: AG-0002.csv.csv
        template=[ "[\w]*-[0-9][0-9][0-9][0-9].csv", "[\w]*-[0-9][0-9][0-9][0-9].csv.csv" ]
        if not re.match(template[0], filename):
            continue
        if not re.match(template[1], filename):
            continue
        df=pandas.read_csv(directory+"/"+filename)
        dataframes_list.append(df)
    return dataframes_list

# Pruebas por si acaso
if __name__ == "__main__":
    import sys
    indir=sys.argv[1]
    mdirs=get_model_dirs(indir)
    for mdir in mdirs:
        dfs=get_dataframes(indir+"/"+mdir)
        print(mdir)
        for df in dfs:
            print(df)

