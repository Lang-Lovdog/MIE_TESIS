import pandas as pd
import sympy as sp
from lvdsl.globals import get_precision_decimal as decpr

# Configuración de visualización
pd.set_option("display.float_format", '{:.20f}'.format)

# Fuente única de verdad para nombres de columnas
variables = {
     "V"         : "V"   ,
     "s"         : "s"   ,
     "tau"       : "τ"   ,
     "AF3"       : "AF3" ,
     "AH3"       : "AH3" ,
     "A3N3"      : "AO3" ,
     "AF5"       : "AF5" ,
     "AD5"       : "AD5" ,
     "lambda1"   : "ƛ1"  ,
     "lambda2"   : "ƛ2"  ,
     "taquiónico": None
}

def read_mathematica_format(archivo_csv: str, D5_Fluxes: bool = False):
    df = pd.read_csv(archivo_csv, index_col=None, header=None, sep=",", dtype=str)

    # Construcción dinámica de nombres basada en el diccionario
    # Filtramos los que no son None y respetamos la bandera de D5
    names = [v for k, v in variables.items() if v is not None]
    if not D5_Fluxes and "AD5" in names:
        names.remove("AD5")

    df2 = pd.DataFrame()
    for i, col in enumerate(df.columns):
        if i >= len(names): break

        # Limpieza de formato Mathematica: {x -> 1.234`20}
        clean_serie = df[col].replace(r'.*->(.*)`.*', r'\1', regex=True)
        # Convertir a SymPy Float con la precisión configurada
        df2[names[i]] = clean_serie.apply(
            lambda x: float(x) if pd.notnull(x) else float(0)
        )

    # Cálculo del estado taquiónico (basado en los nombres del diccionario)
    l1, l2 = variables["lambda1"], variables["lambda2"]
    if l1 in df2.columns and l2 in df2.columns:
        df2["taquiónico"] = df2.apply(
            lambda row: int(1 if float(row[l1]) < 0 or float(row[l2]) < 0 else 0),
            axis=1
        )

    print(df2)
    return df2

def read_native_format(archivo_csv: str):
    df = pd.read_csv(archivo_csv, index_col=None, header=0, sep=",", dtype=str)
    ### Drop all suffixed with _O
    df = df.loc[:, ~df.columns.str.endswith('_O')]
    return df

def save_comparative_csv(
    df_found        : pd.DataFrame       ,
    df_original     : pd.DataFrame       ,
    df_original_id  : int          = 0   ,
    filename        : str          ="out",
    fixed_elements  : list[str]    =[]
):
    """
    Genera un CSV comparativo intercalando columnas encontradas y originales.
    Usa el diccionario 'variables' para mapear nombres de columnas.
    """
    original_row = df_original.iloc[df_original_id]
    data_dict = {}

    # Definimos el orden de las columnas para el CSV final
    # (V, fitness, flujos, coordenadas, autovalores, taquiónico)
    output_keys = [ key for key in variables.keys() ]

    for key in output_keys:
        # Obtenemos el nombre "público" del diccionario (ej: "tau" -> "τ")
        name = variables.get(key)

        # Si el valor en el diccionario es None (como en taquiónico), usamos el key
        col_name = name if name is not None else key

        if key not in df_found.columns and col_name not in df_original.columns:
            continue

        # 1. Insertar valor encontrado (del algoritmo)
        data_dict[key] = df_found[key].values

        # 2. Insertar columna de fitness (especial, no está en variables)
        if key == "V" and "fitness" in df_found.columns:
            data_dict["fitness"] = df_found["fitness"].values

        # 3. Insertar valor original de comparación (_O)
        # s, tau y fijos no llevan comparación según tu muestra
        no_comparar = fixed_elements
        if key not in no_comparar:
            # Buscamos en la fila original usando el nombre mapeado
            if col_name in original_row:
                data_dict[key + "_O"] = original_row[col_name]

    # Crear DataFrame y guardar
    df_out = pd.DataFrame(data_dict)
    df_out.to_csv(f"{filename}.csv")
    print(f"Reporte generado: {filename}.csv con el mapeo de '{list(variables.values())}'")

