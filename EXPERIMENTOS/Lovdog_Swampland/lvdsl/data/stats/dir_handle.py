import os
import re
import pandas                      as pd
from   natsort import humansorted         # type: ignore

###############################################################
# Clase para el manejo de directorios del benchmark
class DirHandle:

    test_dirs = { str: any }
    test_data = { str: any }
    N_list = None

    ###########################################################
    # Esta función está diseñada para recibir contenedores de
    # directorios de pruebas (VacuaFoundXXYYZZZZ).
    # El sistema no comprueba este nombre, por lo que es
    # necesario que el usuario sea consciente de la estructura
    # de su proyecto.
    def __init__(self, path=[]):
        if len(path) == 0:
            return

        if type(path) is not list and type(path) is not str:
            raise TypeError

        if type(path) is str:
            path = [path]
        self.path = path
    ###########################################################


    ###########################################################
    # Si se desea limitar la cantidad de registros a analizar
    def set_max_record(self, N):
        self.N_list = N
    ###########################################################


    ###########################################################
    # Esta función está diseñada para recibir contenedores de
    # directorios de pruebas (VacuaFoundXXYYZZZZ).
    # El sistema no comprueba este nombre, por lo que es
    # necesario que el usuario sea consciente de la estructura
    # de su proyecto.
    def add_dir(self, path):
        if type(path) is not list and type(path) is not str:
            raise TypeError

        if type(path) is str:
            if path in self.path:
                return
            path = [path]

        for p in path:
            if not os.path.exists(p):
                print("Ruta inexistente:", p, "ignorado")
                continue
            if p not in self.path:
                self.path.append(p)
    ###########################################################


    ###########################################################
    # Esta función está diseñada para obtener los subdirectorios
    # dentro de los directorios listados en un diccionario, así
    # cada prueba es identificada por contenedor y modelo.
    # El nombre de cada subdirectorio es considerado el nombre
    # del modelo.
    def get_test_dirs(self):
        self.test_dirs = {}
        for p in self.path:
            self.test_dirs[p] = [
                d for d in os.listdir(p)
                    ## Asegurarse de que es un directorio
                    ## En este nivel se asumen directorios que
                    ## contienen las salidas del benchmark.
                    if os.path.isdir(os.path.join(p, d))
            ]

        return self.test_dirs
    ###########################################################


    ###########################################################
    # Esta función está diseñada para obtener los archivos del
    # benchmark. En este proceso se obtiene todo archivo csv en
    # la llave "csv", y el archivo de modelo, contenido en un
    # txt (se asume sin extensión), el cual se leerá y cuyo
    # contenido se almacenará en la llave "model_desc".
    def get_test_files(self):
        if len(self.test_dirs) == 0:
            self.get_test_dirs()

        self.test_files = {}
        ## Recorre todos los VacuaFound
        for p in self.test_dirs:
            ## Recorre los modelos dentro de cada VacuaFound
            print("Procesando:", p)
            self.test_files[p] = {}
            for n in self.test_dirs[p]:
                print("\tModelo:", n, "encontrado")
                ## Guarda un registro Parent/Model/Files
                self.test_files[p][n] = {
                    "csv": [],
                    "model_desc": {}
                }
                ## Construye la ruta
                path=os.path.join(p, n)
                ## Recorre el directorio
                lst=humansorted(os.listdir(path))
                lstcsv=[f for f in lst
                        if f.endswith(".csv") and
                        ## Ignora todo subdirectorio, en este
                        ## nivel se asumen únicamente archivos
                        ## de texto
                        not os.path.isdir(os.path.join(path,f))
                ]
                dsc=[f for f in lst
                        if not f.endswith(".csv") and
                        ## Ignora todo subdirectorio, en este
                        ## nivel se asumen únicamente archivos
                        ## de texto
                        not os.path.isdir(os.path.join(path,f))
                ]
                if self.N_list is not None:
                    lstcsv=lstcsv[:self.N_list]

                for f in lstcsv:
                    self.test_files[p][n]["csv"].append(f)
                    continue

                # Guardado de los datos del modelo
                with open(os.path.join(path,dsc[0]), "r") as m:
                    decriptor=m.read()
                    match = re.match(
                        r'(\w+)\((.*?)\)',
                        decriptor
                    )
                    if match:
                        model_name=match.group(1)
                        params_str=match.group(2)
                        param_pair=[
                            param.strip().split("=")
                              for param in
                                params_str.split(",")
                        ]
                        param_dict={
                            pair[0]:pair[1]
                              for pair in param_pair
                        }
                        self.test_files[p][n]["model_desc"]={
                            "name": model_name,
                            **param_dict
                        }
                ## Files count
                self.test_files[p][n]["tests_count"] = len(self.test_files[p][n]["csv"])

        return self.test_files
    ###########################################################


    ###########################################################
    # Regresa los elementos del objeto
    def get(self, p, n=None, k=None):
        if n is None and k is not None:
            return {}
        if n is not None and k is not None:
            return self.test_files[p][n][k]
        if k is not None:
            return self.test_files[p][k]
        return self.test_files[p]
    ###########################################################


    ###########################################################
    # Regresa los elementos del objeto (lista de llaves)
    def list(self, p=None, n=None, k=None):
        if k is not None and n is None:
            return {}
        if k is not None:
            return list(self.test_files[p][n][k].keys())
        if n is not None:
            return list(self.test_files[p][n].keys())
        if p is not None:
            return list(self.test_files[p].keys())
        return list(self.test_files.keys())
    ###########################################################


    ###########################################################
    # Get resume of the directory
    def resume(self, p=None, n=None, k=None):
        if p is None and n is None and k is None:
            out=self.test_files
            # Drop directory file list
            for p in out:
                for n in out[p]:
                    del out[p][n]["csv"]
            return out
        return self.get(p=p, n=n, k=k)
    ###########################################################


    ###########################################################
    # Genera un DataFrame de Pandas con la configuración de hiperparámetros
    # de todos los modelos cargados de forma nativa desde model_desc.
    def models_to_dataframe(self, fill_na="-"):

        rows = []

        # Iterar sobre las carpetas cargadas usando la API interna
        for parent_dir in self.list():
            for model_name in self.list(p=parent_dir):

                # Acceso seguro a la metadata interna estructurada
                model_entry = self.test_files.get(parent_dir, {}).get(model_name, {})
                model_desc = model_entry.get("model_desc", {})

                if not model_desc:
                    continue

                # Construcción de la fila mezclando metadatos de rutas con hiperparámetros
                row_data = {
                    "ParentDir": parent_dir,
                    "Name": model_name,
                    "Algorithm": model_desc.get("name", "N/A")
                }

                # Inyección dinámica de todos los parámetros dentro de model_desc
                for param_key, param_value in model_desc.items():
                    if param_key != "name":  # El nombre del algoritmo ya se mapeó
                        try:
                            # Casar tipos de datos numéricos automáticamente
                            if '.' in str(param_value):
                                row_data[param_key] = float(param_value)
                            else:
                                row_data[param_key] = int(param_value)
                        except ValueError:
                            row_data[param_key] = param_value

                rows.append(row_data)

        if not rows:
            return pd.DataFrame() # Regresa un DataFrame vacío si no hay metadata

        df = pd.DataFrame(rows)

        # Indexación y ordenamiento inteligente de columnas
        fixed_headers = ["ParentDir", "Name", "Algorithm"]
        other_headers = sorted([col for col in df.columns if col not in fixed_headers])
        df = df[fixed_headers + other_headers]

        # Rellenar los vacíos estructurales de los parámetros de familias cruzadas (PSO vs IWO)
        return df.fillna(fill_na)
    ###########################################################


###############################################################


if __name__ == "__main__":
    import sys
    from pprint import pprint

    dir = sys.argv[1:]
    d=DirHandle(dir)
    #d.set_max_record(4)
    pprint(d.get_test_dirs())
    pprint(d.get_test_files())
    for p in d.list():
        print("Procesando:", p)
        for n in d.list(p=p):
            print("\tModelo:", n, "encontrado")
            for k in d.list(p=p, n=n):
                print("\t\t", k)
                pprint(d.get(p=p, n=n, k=k))
    pprint(d.resume())
    pprint(d.models_to_dataframe())

