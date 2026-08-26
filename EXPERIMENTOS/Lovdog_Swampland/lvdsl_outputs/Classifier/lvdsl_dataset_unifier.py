### Este script realizado por Lang Lovdog Inu Oókami
### fue diseñado con la finalidad de crear un dataset único
### basado en un conjunto.
### El primer paso es la limpieza (se puede decidir dejar este paso)
### que consiste en extraer únicamente individuos y retirar todo
### _O del dataset, unificando todos los elementos del directorio
### El nombre final del archivo tendrá el formato {parent_dir}_{filename}.csv
### Se puede optar por un prefijo de nombre también

import os
import pandas #type: ignore

def get_blacklisted_and_outputs(
        outfiles_fp:list[str]=["lvdsl_dataset_unifier_outputs.txt"],
        blacklist_fp:list[str]=["blacklist.txt"]) -> tuple[list[str], list[str]]:
    blacklist=[]
    outfiles=[]
    for fp in blacklist_fp:
        if not os.path.exists(fp):
            print(f"El archivo {fp} no existe, ignorando...")
            continue
        with open(fp) as f:
            blacklist.extend([line.strip() for line in f.readlines()])
    for fp in outfiles_fp:
        if not os.path.exists(fp):
            print(f"El archivo {fp} no existe, ignorando...")
            continue
        with open(fp) as f:
            outfiles.extend([line.strip() for line in f.readlines()])
    return blacklist, outfiles

def get_files(path:str, blacklist:list[str]=[]) -> list[str]:
    ### Explora de manera recursiva los directorios obtenidos
    ### Guarda todas las direcciones a archivos csv
    lista_archivos:list[str]=[]
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.join(root,file) in blacklist or file in blacklist:
                print(f"El archivo {file} se encuentra en la blacklist, ignorando...")
                continue
            if file.endswith(".csv"):
                lista_archivos.append(os.path.join(root, file))
    return lista_archivos

def get_outname(file:str) -> str:
    ## Extracción del primer directorio del path
    ## Así path/to/dir -> "path"
    rd=os.path.split(file)[0]
    ## Extracción del parentdir
    pd=os.path.split(file)[-2]
    return rd+pd

def concatenate_csv_files(file_dict:dict) -> pandas.DataFrame:
    # Inicializar un DataFrame vacío para almacenar los datos concatenados.
    df_list=[]
    concatenated_df = pandas.DataFrame()

    for path, files in file_dict.items():
        # Itera sobre cada archivo en la lista de archivos.
        for file in files:
            full_path = os.path.join(path, file) # Construye el nombre completo del archivo
            try:
                ### First column is index
                ### First row is column names
                df = pandas.read_csv(full_path, index_col=0, header=0)
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
    concatenated_df = concatenated_df[[col for col in concatenated_df.columns if not col.endswith('_O')]]

    # Agrega la columna dS_AdS donde dS es V > 0 y AdS es V < 0
    concatenated_df['type'] = concatenated_df['V'].apply(lambda x: 1 if x > 0 else -1)

    # Quitar filas duplicadas.
    concatenated_df.drop_duplicates(inplace=True)

    return concatenated_df


def actualizar_histograma(df:pandas.DataFrame, histograma:dict) -> dict:
    ## dS V>0
    ## AsS V<0
    ## Stable tachionic 0
    ## Unstable tachionic 1

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

def main(replace:bool=False, print_logs:bool=False) -> None:
    dirs:list[str]=[
        "bm/",
        "nbm/",
        "nnbm/",
        "legacy/",
        "ufbm-a/",
    ]
    blacklist:list[str]=[]
    files: dict[str, list[str]] = {}
    outfiles:list[str]=[]

    blacklist, outfiles = get_blacklisted_and_outputs()
    if print_logs:
        __import__('pprint').pprint(blacklist)
        __import__('pprint').pprint(outfiles)

    for d in dirs:
        a=get_files(d,blacklist + outfiles)
        for f in a:
            pd=os.path.split(f)[0]
            bn=os.path.split(f)[1]
            if pd in files.keys():
                files[pd].append(bn)
            else:
                files[pd]=[bn]

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
        outpath=os.path.join(outdir, outname)
        if print_logs:
            print(df)
        contador=contador+1
        print(r, len(files[r]), len(df))
        actualizar_histograma(df, histograma)
        if replace and outpath in outfiles:
            df.to_csv(os.path.join(outdir, outname))
        elif outpath not in outfiles:
            df.to_csv(os.path.join(outdir, outname))
            outfiles.append(outpath)
        else:
            print(f"El archivo {outpath} ya existe, ignorando...")
        del df

    with open("lvdsl_dataset_unifier_outputs.txt", "w") as lduo_fp:
        for fout in outfiles:
            lduo_fp.write(f"{fout}\n")

    __import__('pprint').pprint(histograma)
    print(f'Scanned files {contador}')

if __name__ == "__main__":
    main(replace=True)

