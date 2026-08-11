import glob
import re
import sys
import os
import pandas as pd

def verify_csv_chain(input_args):
    files = []

    # 1. Recolectar archivos si se pasa un directorio o una lista de archivos del shell
    for arg in input_args:
        if os.path.isdir(arg):
            files.extend(glob.glob(os.path.join(arg, "*"), recursive=True))
        else:
            files.append(arg)

    # Regex que extrae los 4 dígitos antes de cualquier combinación de .csv
    def extract_number(filepath):
        match = re.search(r'(\d{4})(?:\.csv)+$', filepath, re.IGNORECASE)
        return int(match.group(1)) if match else -1

    # Filtrar y ordenar por número de secuencia
    valid_files = sorted([f for f in files if extract_number(f) != -1], key=extract_number)

    if not valid_files:
        print("No se encontraron archivos válidos con el sufijo %04d.")
        return

    print(f"Se encontraron {len(valid_files)} archivos en la secuencia:")
    for f in valid_files:
        print(f"  - {f}")
    print("-" * 65)

    # Cargar y extraer registros únicos de cada CSV
    file_data = []
    for f in valid_files:
        try:
            df = pd.read_csv(f)
            rows_set = set(tuple(x) for x in df.to_numpy())
            file_data.append((f, len(df), rows_set))
        except Exception as e:
            print(f"[ERROR] No se pudo leer {f}: {e}")
            return

    all_passed = True

    # 2. Comparación consecutiva
    for i in range(len(file_data) - 1):
        prev_file, prev_count, prev_set = file_data[i]
        curr_file, curr_count, curr_set = file_data[i+1]

        if prev_set.issubset(curr_set):
            diff = curr_count - prev_count
            print(f"[OK] {prev_file} ({prev_count} filas) está en {curr_file} ({curr_count} filas) [+{diff} filas nuevas].")
        else:
            missing = len(prev_set - curr_set)
            print(f"[ERROR] {prev_file} NO está completamente en {curr_file}. Faltan {missing} filas.")
            all_passed = False

    print("-" * 65)

    # 3. Verificación contra el último archivo de la secuencia
    last_file, last_count, last_set = file_data[-1]
    for prev_file, prev_count, prev_set in file_data[:-1]:
        if not prev_set.issubset(last_set):
            missing = len(prev_set - last_set)
            print(f"[FALLO] El archivo final {last_file} NO contiene todas las filas de {prev_file} (faltan {missing} filas).")
            all_passed = False

    if all_passed:
        print(f"\nÉXITO: El archivo final ({last_file}) contiene el 100% de las filas acumuladas de los {len(valid_files)} archivos.")

if __name__ == "__main__":
    args = sys.argv[1:] if len(sys.argv) > 1 else ["."]
    verify_csv_chain(args)
