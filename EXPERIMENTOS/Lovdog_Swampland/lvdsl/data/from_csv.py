import pandas                                            as pd            #type: ignore
import sympy                                             as sp
from lvdsl.bioinspired.defs import get_precision_decimal as decpr

pd.set_option("display.float_format",'{:.20f}'.format)

variables = {
     "V"      : "V"   ,
     "s"      : "s"   ,
     "tau"    : "τ"   ,
     "AF3"    : "AF3" ,
     "AH3"    : "AH3" ,
     "A3N3"   : "AO3" ,
     "AF5"    : "AF5" ,
     "AD5"    : "AD5" ,
     "lambda1": "ƛ1"  ,
     "lambda2": "ƛ2"
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

