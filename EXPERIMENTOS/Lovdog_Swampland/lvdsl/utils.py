## Utilities such as directory search and stuff

import os


def get_file_list(dirname :  str, depth=1, savepath=True):
    filelist = {}
    if savepath:
        filelist["Path"]=os.path.abspath(dirname)
    for e in os.listdir(dirname):
        d = os.path.basename(dirname)
        if os.path.isdir(os.path.join(dirname, e)):
            if depth > 1:
                ls=get_file_list(os.path.join(dirname, e), depth-1,False)
                filelist={**filelist, **ls} # Merge dictionaries
            else:
                if d not in filelist:
                    filelist[d]=[]
                filelist[d].append(e)
        else:
            if d not in filelist:
                filelist[d]=[]
            filelist[d].append(e)
    return filelist

def get_file_list_by_extension(dirname :  str, extension: str, depth=1):
    return [f for f in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, f)) and f.endswith(extension)]


def filter_by_extension(filelist: dict, extension: str):
    filtered_filelist = {}
    for key in filelist:
        if isinstance(filelist[key],dict):
            filtered_filelist[key] = filter_by_extension({key:filelist[key]}, extension)
        elif isinstance(filelist[key],list):
            filtered_list =  [f for f in filelist[key] if isinstance(f, str) and f.endswith(extension)]
            if filtered_list:
                filtered_filelist[key] = filtered_list
            else:
                filtered_filelist[key] = []
    return filtered_filelist

def filter_by_pattern(filelist: dict, pattern: str):
    ### Patterns are like "%4d-name.csv" or "file-%d%d%d.csv"
    return [f for f in filelist if f.startswith(pattern)]

def sort_serialized_files(filelist: dict, ascendent=True):
    sorted_filelist = {}
    for key in filelist:
        if isinstance(filelist[key],dict):
            sorted_filelist[key] = sort_serialized_files({key:filelist[key]}, ascendent)
        elif isinstance(filelist[key],list):
            sorted_filelist[key] = sorted(filelist[key], reverse=not ascendent)
    return sorted_filelist

def get_serialized_file_index(filelist: list, filepattern: str):
    if type(filelist) is not list:
        filelist = [filelist]
    if type(filepattern) is not str:
        print(f"ERROR: filepattern must be a string\n   >>> Got '{filepattern}'")
        return -1
    for idx,f in enumerate(filelist):
        if f.startswith(filepattern):
            return idx
    return -1

