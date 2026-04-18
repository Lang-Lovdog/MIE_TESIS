### Este script se basa en el experimento descrito por el artículo
###  Metastable vacua from torsion and machine learning
### de Cesar Damian y Oscar Loaiza-Brito
### Acceso al experimento original https://doi.org/10.1140/epjc/s10052-022-11118-x

import sys
## IMPORTS
import sympy             as sp  #type: ignore
from   sympy             import lambdify
from   ..xp              import HAS_GPU
## IMPORTS

##### Opciones globales
precision_decimal = 30
##### Opciones globales

##### Definición de las variables principales de la función potencial
AH3  = sp.Symbol('AH3' , real=True)
AF3  = sp.Symbol('AF3' , real=True)
AF5  = sp.Symbol('AF5' , real=True)
A3N3 = sp.Symbol('A3N3', real=True)
AD5  = sp.Symbol('AD5' , real=True)
tau  = sp.Symbol('tau' , real=True)
s    = sp.Symbol('s'   , real=True)
##### Definición de las variables principales de la función potencial
##### Diccionario de valores numéricos globales
variables_numericas={
    "AH3" : 1.0,
    "AF3" : 1.0,
    "AF5" : 1.0,
    "A3N3": 1.0,
    "AD5" : 1.0,
    "tau" : 1.0,
    "s"   : 1.0
}
##### Diccionario de valores numéricos globales

# Función potencial V
V                  =  (AH3*s/(tau**3)) + (AF3/(s*tau**3)) + (AF5/(tau**4)) + (A3N3/(tau**3))
V_lifting          =  (AH3*s/(tau**3)) + (AF3/(s*tau**3)) + (AF5/(tau**4)) + (A3N3/(tau**3)) + (AD5/((s**sp.Rational(1,2)*(tau**sp.Rational(5,2)))))
# Función potencial V

# Matriz Hessiana de la función potencial
VHess              = sp.hessian(V, [s,tau])
V_liftingHess      = sp.hessian(V_lifting, [s,tau])
# Matriz Hessiana de la función potencial

# Autovalores de VHess
VHess_eig          = list(VHess.eigenvals().keys())
V_liftingHess_eig  = list(V_liftingHess.eigenvals().keys())
# Autovalores de VHess

# Traza de hessiana
V_Hess_tr          = VHess.trace()
V_liftingHess_tr   = V_liftingHess.trace()
# Traza de hessiana

# Gradiente del potencial
V_gradient         = sp.derive_by_array(V, [s,tau])
V_lifting_gradient = sp.derive_by_array(V_lifting, [s,tau])
# Gradiente del potencial

# Determinante de la Hessiana
V_Hess_det         = VHess.det()
V_liftingHess_det  = V_liftingHess.det()
# Determinante de la Hessiana

##### Lambdificación de las funciones base
### ELEMENTOS SIMBÓLICOS ###
VARIABLES_LAMBDIFICABLES_LIFT  =(AH3,AF3,AF5,A3N3,AD5,tau,s)
VARIABLES_LAMBDIFICABLES_NOLIFT=(AH3,AF3,AF5,A3N3,    tau,s)
METHOD = "cupy" if HAS_GPU else "numpy"
### ELEMENTOS SIMBÓLICOS ###
### POTENCIAL EFECTIVO ###
V_lambda                   = lambdify(VARIABLES_LAMBDIFICABLES_NOLIFT, V                 , METHOD)
V_lifting_lambda           = lambdify(VARIABLES_LAMBDIFICABLES_LIFT  , V_lifting         , METHOD)
### POTENCIAL EFECTIVO ###
### HESSIANA ###
VHess_lambda               = lambdify(VARIABLES_LAMBDIFICABLES_NOLIFT, VHess             , METHOD)
V_liftingHess_lambda       = lambdify(VARIABLES_LAMBDIFICABLES_LIFT  , V_liftingHess     , METHOD)
### HESSIANA ###
### AUTOVALORES ###
VHess_eig_lambda           = lambdify(VARIABLES_LAMBDIFICABLES_NOLIFT, VHess_eig         , METHOD)
V_liftingHess_eig_lambda   = lambdify(VARIABLES_LAMBDIFICABLES_LIFT  , V_liftingHess_eig , METHOD)
### AUTOVALORES ###
### TRAZA ###
V_Hess_tr_lambda           = lambdify(VARIABLES_LAMBDIFICABLES_NOLIFT, V_Hess_tr         , METHOD)
V_liftingHess_tr_lambda    = lambdify(VARIABLES_LAMBDIFICABLES_LIFT  , V_liftingHess_tr  , METHOD)
### TRAZA ###
### GRADIENTE ###
V_gradient_lambda          = lambdify(VARIABLES_LAMBDIFICABLES_NOLIFT, V_gradient        , METHOD)
V_lifting_gradient_lambda  = lambdify(VARIABLES_LAMBDIFICABLES_LIFT  , V_lifting_gradient, METHOD)
### GRADIENTE ###
### DETERMINANTE ###
V_Hess_det_lambda          = lambdify(VARIABLES_LAMBDIFICABLES_NOLIFT, V_Hess_det        , METHOD)
V_liftingHess_det_lambda   = lambdify(VARIABLES_LAMBDIFICABLES_LIFT  , V_liftingHess_det , METHOD)
### DETERMINANTE ###

##### Definición de valores fijos para búsqueda
def set_fixed_value(values : dict):
    global variables_numericas
    for var in values:
        variables_numericas[var] = values[var]

def set_precision_decimal(val : int):
    global precision_decimal
    precision_decimal = val

def get_precision_decimal():
    return precision_decimal

if __name__ == '__main__':
    sp.init_printing(use_unicode=True)
    ## Imprimir versión de python
    print(f"Version de Python: {sys.version}\n")
    print("Función potencial: V = ")
    sp.pprint(V)
    print("Función potencial: V_lifting = ")
    sp.pprint(V_lifting)
    print("\nMatriz Hessiana: VHess = ")
    sp.pprint(VHess)
    print("\nMatriz Hessiana: V_liftingHess = ")
    sp.pprint(V_liftingHess)
    print("\n")

