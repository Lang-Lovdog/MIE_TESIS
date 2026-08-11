### Este script realizado por Lang Lovdog Inu Oókami
### fue diseñado con la finalidad de crear un dataset único
### basado en un conjunto.
### El primer paso es la limpieza (se puede decidir dejar este paso)
### que consiste en extraer únicamente individuos y retirar todo
### _O del dataset, unificando todos los elementos del directorio
### El nombre final del archivo tendrá el formato {parent_dir}_{filename}.csv
### Se puede optar por un prefijo de nombre también

import os
import pandas

def get_files(path):
    ### Explora de manera recursiva los directorios obtenidos
    ### Guarda todas las direcciones a archivos csv
    lista_archivos=[]
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".csv"):
                lista_archivos.append(os.path.join(root, file))
    return lista_archivos

def get_outname(file):
    ## Extracción del primer directorio del path
    ## Así path/to/dir -> "path"
    rd=os.path.split(file)[0]
    ## Extracción del parentdir
    pd=os.path.split(file)[-2]
    return rd+pd

def concatenate_csv_files(file_dict):
    # Inicializar un DataFrame vacío para almacenar los datos concatenados.
    df_list=[]
    concatenated_df = pandas.DataFrame()

    for path, files in file_dict.items():
        # Itera sobre cada archivo en la lista de archivos.
        for file in files:
            full_path = os.path.join(path, file) # Construye el nombre completo del archivo
            try:
                df = pandas.read_csv(full_path)
                df_list.append(df)
            except pandas.errors.ParserError as err:
                # Manejo específico para archivos con líneas o campos corruptos
                reason = str(err).strip().split("\n")[-1]
                print(f"Err: Malformed File -> {full_path}\n     Detail: {reason}")
                continue
            except pandas.errors.EmptyDataError:
                # Manejo específico para archivos totalmente vacíos (0 bytes)
                print(f"Err: Malformed File -> {full_path}\n     Detail: File is completely empty")
                continue
            except FileNotFoundError:
                # Manejo si la ruta no existe en el sistema
                print(f"Err: Missing File -> {full_path}")
                continue
            except Exception as err:
                # Captura cualquier otro error genérico de I/O o del sistema
                print(f"Err: Unexpected Error in {full_path} -> {err}")
                continue
    # Concatena el DataFrame actual con el DataFrame concatenado total.
    concatenated_df = pandas.concat(df_list, ignore_index=True)

    # Elimina las columnas que terminan con '_O'.
    #columns_to_drop = [col for col in concatenated_df.columns if not col.endswith('_O')]
    #concatenated_df.drop(columns=columns_to_drop, inplace=True)
    concatenated_df = concatenated_df[[col for col in concatenated_df.columns if not col.endswith('_O')]]

    # Quitar filas duplicadas.
    concatenated_df.drop_duplicates(inplace=True)

    return concatenated_df


def actualizar_histograma(df, histograma):
    """Clasifica vacíos vectorialmente sin iterar fila por fila."""
    # Máscaras booleanas
    is_ds = df["V"] > 0
    is_ads = df["V"] < 0
    is_stable = df["taquiónico"] == 0
    is_unstable = df["taquiónico"] == 1

    # Conteo vectorial directo
    histograma["dS_stable"] += int((is_ds & is_stable).sum())
    histograma["dS_unstable"] += int((is_ds & is_unstable).sum())
    histograma["AdS_stable"] += int((is_ads & is_stable).sum())
    histograma["AdS_unstable"] += int((is_ads & is_unstable).sum())

    return histograma

dirs=[
    "bm/",
    "nbm/",
    "nnbm/",
    "legacy/",
    "ufbm-a/",
]

files={ str : [any] }
outfiles=[]

for d in dirs:
    a=get_files(d)
    for f in a:
        pd=os.path.split(f)[0]
        bn=os.path.split(f)[1]
        if pd in files.keys():
            files[pd].append(bn)
        else:
            files[pd]=[bn]


outfiles=[of.replace("/", "_").replace("\\", "_") for of in files.keys()]

contador=0
histograma={
    "dS_stable": 0,
    "AdS_stable": 0,
    "dS_unstable": 0,
    "AdS_unstable": 0,
}
for r in files.keys():
    df=concatenate_csv_files({r: files[r]})
    outname=r.replace("/", "_").replace("\\", "_")+".csv"
    outdir=r.split("/")[0]
    #print(df)
    contador=contador+1
    ## dS V>0
    ## AsS V<0
    ## Stable tachionic 0
    ## Unstable tachionic 1
    print(files[r], len(df))
    actualizar_histograma(df, histograma)
   # df.to_csv(os.path.join(outdir, outname))
    del df
    #if contador>3:
    #    break

__import__('pprint').pprint(histograma)
print(f'Scanned files {contador}')

