import os
import sys

xp=None
np=None
HAS_GPU = True

def get_nvidia_configs():
    ## Obtiene la información del entorno virtual en el que se está corriendo
    venv_path = os.environ.get('VIRTUAL_ENV')
    if venv_path:
        cuda_lib_path = os.path.join(venv_path, 'lib', f'python{sys.version_info.major}.{sys.version_info.minor}', 'site-packages', 'nvidia')
        if os.path.exists(cuda_lib_path):
            os.environ['CUDA_PATH'] = cuda_lib_path
            # Añadimos las subcarpetas de nvrtc y cuda_runtime al PATH del sistema
            os.environ['LD_LIBRARY_PATH'] = f"{cuda_lib_path}/cuda_runtime/lib:{cuda_lib_path}/nvrtc/lib:{cuda_lib_path}:{os.environ.get('LD_LIBRARY_PATH', '')}"
    else:
        print("No se encontro ninguna virtual environment activa.")
        print("Por favor, configure una virtual environment antes de ejecutar este script.")
        sys.exit(1)

def import_numeric_handle():
    global np, xp, HAS_GPU
    import numpy
    try:
        import cupy #type: ignore
        HAS_GPU = True
        xp = cupy
        np = numpy
    except ImportError:
        print("No se pudo importar cupy. Usando numpy.")
        np    = numpy
        xp    = np
get_nvidia_configs()
import_numeric_handle()

