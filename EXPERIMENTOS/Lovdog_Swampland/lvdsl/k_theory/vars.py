### Este script se basa en el experimento descrito por el artículo
###  Metastable vacua from torsion and machine learning
### de Cesar Damian y Oscar Loaiza-Brito
### Acceso al experimento original https://doi.org/10.1140/epjc/s10052-022-11118-x

## IMPORTS
import sympy             as sp  #type: ignore
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
V         =  (AH3*s/(tau**3)) + (AF3/(s*tau**3)) + (AF5/(tau**4)) + (A3N3/(tau**3))
V_lifting =  (AH3*s/(tau**3)) + (AF3/(s*tau**3)) + (AF5/(tau**4)) + (A3N3/(tau**3)) + (AD5/((s**sp.Rational(1,2)*(tau**sp.Rational(5,2)))))
# Función potencial V

# Matriz Hessiana de la función potencial
VHess         = sp.hessian(V, [s,tau])
V_liftingHess = sp.hessian(V_lifting, [s,tau])
# Matriz Hessiana de la función potencial

# Autovalores de VHess
VHess_eig         = VHess.eigenvals()
V_liftingHess_eig = V_liftingHess.eigenvals()
# Autovalores de VHess

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
