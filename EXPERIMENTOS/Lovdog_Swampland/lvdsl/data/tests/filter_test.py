import lvdsl.utils as utils
import pandas as pd
import os

# utils:
# def get_file_list(dirname :  str):
# 
# def filter_by_extension(filelist: list, extension: str):
# 
# def filter_by_pattern(filelist: list, pattern: str):
# 
# def get_file_list_by_extension(dirname :  str, extension: str):
# 
# def sort_serialized_files(filelist: list, ascendent=True):
# 
# def get_serialized_file_index(filelist: list, filepattern: str):

files=utils.get_file_list(
    "/home/lang_lovdog/Documentos/ACAD/MAESTRÍA/MIE_TESIS/EXPERIMENTOS/Lovdog_Swampland/lvdsl_outputs/VacuaFound_22042026_16/",
    depth=2
)

path=files["Path"]

for key in files:
    print(key)
    for f in files[key]:
        print(f'\t{f}')

files=utils.filter_by_extension(files, ".csv")

for key in files:
    print(key)
    for f in files[key]:
        print(f'\t{f}')

files=utils.sort_serialized_files(files)

for key in files:
    print(key)
    for f in files[key]:
        print(f'\t{f}')

for key in files:
    length=len(files[key])
    file=os.path.join(path,key,files[key][-1])
    df=pd.read_csv(file)
    lastfilelenght=len(df)
    print(f'{key}: Has stopped at {length} record, iteration {lastfilelenght}')
