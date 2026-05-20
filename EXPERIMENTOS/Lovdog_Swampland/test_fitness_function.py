# Este script está desarrollado con el propósito de validar la función de fitness a través de la definición simbólica de la función potencial.
# El argumento de esta evaluación indirecta es que, si la definición simbólica es correcta, el resto de la función, considerando que
# sigue al pie de la letra las evaluaciones de error, debe ser correcta.
# Debido a las limitaciones del software con el que se cuenta (acceso a software propietario), las medidas indirectas son, en consecuencia,
#la mejor herramienta de validación.

# La validación se realizará de 3 formas diferentes
# 1. Evaluación de eigevalores
# 2. Aproximación metaheurística a través de variables
# 3. Aproximación metaheurística a través de coeficientes

from MetastableVacua import autovalores_VHess as eigenvals
from MetastableVacua import potencial_eval as potencial
from MetastableVacua import get_precision_decimal as decpr
from MetastableVacua import plot_potencial_vars_adS as potplot
from MetastableVacua import set_fixed_value
#from MetastableVacua import diagnostic_plot
from matplotlib import pyplot as plt #type: ignore
import pandas as pd                  #type: ignore
#import numpy as np                   #type: ignore
import sympy as sp                   #type: ignore

pd.set_option("display.float_format",'{:.20f}'.format)

variables = {
     "V"   : "V"   ,
     "s"   : "s"   ,
     "tau" : "τ"   ,
     "AF3" : "AF3" ,
     "AH3" : "AH3" ,
     "A3N3": "AO3" ,
     "AF5" : "AF5" ,
     "AD5" : "AD5" ,
     "Eig1": "ƛ1"  ,
     "Eig2": "ƛ2"
}

#### Obtención de los datos exportados desde mathematica
def datos_del_csv_mathematica(archivo_csv: str, D5_Fluxes: bool = False):
    df = pd.read_csv(archivo_csv,index_col=None, header=None, sep=",", dtype=str)
    df2=df.copy()
    # Print columns separately
    if D5_Fluxes:
        names = [ "V"  , "s"  , "τ"  , "AF3", "AH3", "AO3", "AF5", "AD5", "ƛ1" , "ƛ2" ]
    else:
        names = [ "V"  , "s"  , "τ"  , "AF3", "AH3", "AO3", "AF5", "ƛ1" , "ƛ2" ]
    i=0
    for col in df.columns:
        df2[col]=df[col].replace(
            r'.*->(.*)`.*', r'\1', regex=True
        ).apply(lambda x: sp.Float(x, decpr()) if pd.notnull(x) else sp.Float(0,decpr()))
        df2.rename(columns={col: names[i]}, inplace=True)
        i=i+1
    return df2

def funcion_potencial_eval(df : pd.DataFrame):
    comparacion = None
    for fila in df.iterrows():
        pot=potencial(
            fila[1][variables["AH3" ]],
            fila[1][variables["AF3" ]],
            fila[1][variables["AF5" ]],
            fila[1][variables["A3N3"]],
            fila[1][variables["tau" ]],
            fila[1][variables["s"   ]]
        )
        diferencia = fila[1][variables["V"]]-pot
        diferencia_error = sp.log(abs(diferencia),10).evalf(decpr()) if diferencia !=0 else 0
        cmpdict = {
            "Original"   : [ fila[1][variables["V"]] ],
            "Actual"     : [ pot ],
            "Diferencia" : [ diferencia ],
            "Error"      : [ diferencia_error ]
        }
        if comparacion is None:
            comparacion = pd.DataFrame(cmpdict)
        else:
            comparacion = pd.concat([comparacion, pd.DataFrame(cmpdict)])
    print(comparacion)

#### Evaluación de eigenvalores
def auto_valores_eval(df : pd.DataFrame):
    comparacion = None
    for fila in df.iterrows():
        eig=eigenvals(
            fila[1][variables["AH3" ]],
            fila[1][variables["AF3" ]],
            fila[1][variables["AF5" ]],
            fila[1][variables["A3N3"]],
            fila[1][variables["tau" ]],
            fila[1][variables["s"   ]]
        )
        diferencia =[
            fila[1][variables["Eig1"]]-eig[0],
            fila[1][variables["Eig2"]]-eig[1]
        ]
        diferencia_error = [ sp.log(abs(x), 10).evalf(decpr()) if x != 0 else 0 for x in diferencia ]
        cmpdict = {
            "Original1"   : [ fila[1][variables["Eig1"]] ],
            "Original2"   : [ fila[1][variables["Eig2"]] ],
            "Actual1"     : [ eig[0] ],
            "Actual2"     : [ eig[1] ],
            "Diferencia1" : [ diferencia[0] ],
            "Diferencia2" : [ diferencia[1] ] ,
            "Error1"      : [ diferencia_error[0] ],
            "Error2"      : [ diferencia_error[1] ]
        }
        if comparacion is None:
            comparacion = pd.DataFrame(cmpdict)
        else:
            comparacion = pd.concat([comparacion, pd.DataFrame(cmpdict)])
    print(comparacion)

#### Graficación de una solucón
def plot_potencial_vs_autovalores(df : pd.DataFrame):
    global variables

    ## Aquí se saca el mínimo de cada autovalor de la solución encontrada
    ## registrado en el csv
    autovals = [
        min([
            fila[1][variables["Eig1"]],
            fila[1][variables["Eig2"]]
        ]) for fila in df.iterrows()
    ]

    ## Los registros de cada valor de la función potencial de la solución
    ## encontrada registrados en el csv
    potenciales = [
        fila[1][variables["V"]] for fila in df.iterrows()
    ]

    autovals_sympy = [
        min(eigenvals(
            fila[1][variables["AH3" ]],
            fila[1][variables["AF3" ]],
            fila[1][variables["AF5" ]],
            fila[1][variables["A3N3"]],
            fila[1][variables["tau" ]],
            fila[1][variables["s"   ]]
        )) for fila in df.iterrows()
    ]

    ## Graficación de los dos pares, el primero considerando los autovalores
    ## originales y el otro considerando los autovalores obtenidos por el método
    ## implementado.
    ## Potencial vs autovalores y otro gráfico Potencial vs sympy autovalores
    figura, axiales = plt.subplots(1, 2)
    axiales[0].scatter(autovals, potenciales, color="red", s=2, linewidth=0.5)
    axiales[1].scatter(autovals_sympy, potenciales, color="blue", s=2, linewidth=0.5)
    axiales[0].set_title("Originales")
    axiales[1].set_title("Sympy")
    axiales[0].set_xlabel("Autovalores")
    axiales[1].set_xlabel("Autovalores")
    axiales[0].set_ylabel("Potencial")
    axiales[1].set_ylabel("Potencial")
    axiales[0].grid()
    axiales[1].grid()
    plt.show()


if __name__ == '__main__':
    archivo_csv = "../CESAR-BRITO_ORIGINAL-DATA/Calibracion_no_lifting.csv"
    df = datos_del_csv_mathematica(archivo_csv)
    for col in df.columns:
        print(df[col])
    funcion_potencial_eval(df)
    auto_valores_eval(df)
    plot_potencial_vs_autovalores(df)
