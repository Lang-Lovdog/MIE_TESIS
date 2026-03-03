### Este script se basa en el experimento descrito por el artículo
###  Metastable vacua from torsion and machine learning
### de Cesar Damian y Oscar Loaiza-Brito
### https://doi.org/10.1140/epjc/s10052-022-11118-x

## IMPORTS
import sys
import numpy             as np  #type: ignore
import matplotlib.pyplot as plt #type: ignore
#import pandas            as pd  #type: ignore
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
V = (AH3*s/(tau**3)) + (AF3/(s*tau**3)) + (AF5/(tau**4)) + (A3N3/(tau**3))
V_lifting =  (AH3*s/(tau**3)) + (AF3/(s*tau**3)) + (AF5/(tau**4)) + (A3N3/(tau**3)) + (AD5/((s**sp.Rational(1,2)*(tau**sp.Rational(5,2)))))
#V_lifting =  (AH3*s/(tau**3)) + (AF3/(s*tau**3)) + (AF5/(tau**4)) + (A3N3/(tau**3)) + (AD5/((s**(1/2)*(tau**(5/2)))))
# Función potencial V

# Matriz Hessiana de la función potencial
VHess = sp.hessian(V, [s,tau])
V_liftingHess = sp.hessian(V_lifting, [s,tau])
# Matriz Hessiana de la función potencial

# Autovalores de VHess
eigenvals_VHess = VHess.eigenvals()
eigenvals_VHess_lifting = V_liftingHess.eigenvals()
# Autovalores de VHess

##### Definición de las funciones de error

## Evaluadores

def potencial_semidefinido_positivo(_AH3, _AF3, _AF5, _A3N3, _tau, _s):
    val=V.subs([
        (AH3, _AH3),
        (AF3, _AF3),
        (AF5, _AF5),
        (A3N3, _A3N3),
        (tau, _tau),
        (s, _s)
    ]).evalf()
    return np.abs(val)-val

def potencial_semidefinido_positivo_AdS(_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s):
    val=V_lifting.subs([
        (AH3, _AH3),
        (AF3, _AF3),
        (AF5, _AF5),
        (A3N3, _A3N3),
        (AD5, _AD5),
        (tau, _tau),
        (s, _s)
    ]).evalf()
    return np.abs(val)-val

def traza_definida_positiva(_AH3, _AF3, _AF5, _A3N3, _tau, _s):
    val = VHess.trace().subs([
        (AH3, _AH3),
        (AF3, _AF3),
        (AF5, _AF5),
        (A3N3, _A3N3),
        (tau, _tau),
        (s, _s)
    ]).evalf()
    return np.abs(val)-val

def traza_definida_positiva_AdS(_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s):
    val = V_liftingHess.trace().subs([
        (AH3, _AH3),
        (AF3, _AF3),
        (AF5, _AF5),
        (A3N3, _A3N3),
        (AD5, _AD5),
        (tau, _tau),
        (s, _s)
    ]).evalf()
    return np.abs(val)-val

def gradient_modulus(_AH3, _AF3, _AF5, _A3N3, _tau, _s):
    diV  = sp.derive_by_array(V, [s,tau])
    diV2 = diV[0]*diV[0] + diV[1]*diV[1]
    diV2 = diV2.subs([
        (AH3, _AH3),
        (AF3, _AF3),
        (AF5, _AF5),
        (A3N3, _A3N3),
        (tau, _tau),
        (s, _s)
    ]).evalf()
    return diV2

def gradient_modulus_AdS(_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s):
    diV  = sp.derive_by_array(V_lifting, [s,tau])
    diV2 = diV[0]*diV[0] + diV[1]*diV[1]
    diV2 = diV2.subs([
        (AH3, _AH3),
        (AF3, _AF3),
        (AF5, _AF5),
        (A3N3, _A3N3),
        (AD5, _AD5),
        (tau, _tau),
        (s, _s)
    ]).evalf()
    return diV2

def no_taquionico(_AH3, _AF3, _AF5, _A3N3, _tau, _s):
    s_val = VHess.det() - VHess.trace()/4.0
    f_val = s_val.subs([
        (AH3, _AH3),
        (AF3, _AF3),
        (AF5, _AF5),
        (A3N3, _A3N3),
        (tau, _tau),
        (s, _s)
    ]).evalf()
    return np.abs(f_val)-f_val

def no_taquionico_AdS(_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s):
    s_val = V_liftingHess.det() - V_liftingHess.trace()/4.0
    f_val = s_val.subs([
        (AH3, _AH3),
        (AF3, _AF3),
        (AF5, _AF5),
        (A3N3, _A3N3),
        (AD5, _AD5),
        (tau, _tau),
        (s, _s)
    ]).evalf()
    return np.abs(f_val)-f_val

##### Función general de error
def fitness_function(_AH3, _AF3, _AF5, _A3N3, _tau, _s):
    return (
        potencial_semidefinido_positivo(_AH3, _AF3, _AF5, _A3N3, _tau, _s) +
        traza_definida_positiva        (_AH3, _AF3, _AF5, _A3N3, _tau, _s) +
        gradient_modulus               (_AH3, _AF3, _AF5, _A3N3, _tau, _s) +
        no_taquionico                  (_AH3, _AF3, _AF5, _A3N3, _tau, _s)
    )

def fitness_function_mealpy(solutions):
    _AH3, _AF3, _AF5, _A3N3, _tau, _s = solutions
    return (
        potencial_semidefinido_positivo(_AH3, _AF3, _AF5, _A3N3, _tau, _s) +
        traza_definida_positiva        (_AH3, _AF3, _AF5, _A3N3, _tau, _s) +
        gradient_modulus               (_AH3, _AF3, _AF5, _A3N3, _tau, _s) +
        no_taquionico                  (_AH3, _AF3, _AF5, _A3N3, _tau, _s)
    )

def fitness_function_AdS(_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s):
    return (
        potencial_semidefinido_positivo_AdS(_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s) +
        traza_definida_positiva_AdS        (_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s) +
        gradient_modulus_AdS               (_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s) +
        no_taquionico_AdS                  (_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s)
    )

def fitness_function_AdS_mealpy(solutions):
    _AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s = solutions
    return (
        potencial_semidefinido_positivo_AdS(_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s) +
        traza_definida_positiva_AdS        (_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s) +
        gradient_modulus_AdS               (_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s) +
        no_taquionico_AdS                  (_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s)
    )

##### Función de error de coeficientes fijos
def fitness_function_coef(_AH3, _AF3, _AF5, _A3N3):
    global variables_numericas
    return (
        potencial_semidefinido_positivo(_AH3, _AF3, _AF5, _A3N3, variables_numericas['tau'], variables_numericas['s']) +
        traza_definida_positiva        (_AH3, _AF3, _AF5, _A3N3, variables_numericas['tau'], variables_numericas['s']) +
        gradient_modulus               (_AH3, _AF3, _AF5, _A3N3, variables_numericas['tau'], variables_numericas['s']) +
        no_taquionico                  (_AH3, _AF3, _AF5, _A3N3, variables_numericas['tau'], variables_numericas['s'])
    )

def fitness_function_coef_mealpy(solutions):
    global variables_numericas

    _AH3, _AF3, _AF5, _A3N3 = solutions

    return (
        potencial_semidefinido_positivo(_AH3, _AF3, _AF5, _A3N3, variables_numericas['tau'], variables_numericas['s']) +
        traza_definida_positiva        (_AH3, _AF3, _AF5, _A3N3, variables_numericas['tau'], variables_numericas['s']) +
        gradient_modulus               (_AH3, _AF3, _AF5, _A3N3, variables_numericas['tau'], variables_numericas['s']) +
        no_taquionico                  (_AH3, _AF3, _AF5, _A3N3, variables_numericas['tau'], variables_numericas['s'])
    )

def fitness_function_coef_AdS(_AH3, _AF3, _AF5, _A3N3, _AD5):
    global variables_numericas
    return (
        potencial_semidefinido_positivo_AdS(_AH3, _AF3, _AF5, _A3N3, _AD5, variables_numericas['tau'], variables_numericas['s']) +
        traza_definida_positiva_AdS        (_AH3, _AF3, _AF5, _A3N3, _AD5, variables_numericas['tau'], variables_numericas['s']) +
        gradient_modulus_AdS               (_AH3, _AF3, _AF5, _A3N3, _AD5, variables_numericas['tau'], variables_numericas['s']) +
        no_taquionico_AdS                  (_AH3, _AF3, _AF5, _A3N3, _AD5, variables_numericas['tau'], variables_numericas['s'])
    )

def fitness_function_coef_AdS_mealpy(solutions):
    global variables_numericas

    _AH3, _AF3, _AF5, _A3N3, _AD5 = solutions

    return (
        potencial_semidefinido_positivo_AdS(_AH3, _AF3, _AF5, _A3N3, _AD5, variables_numericas['tau'], variables_numericas['s']) +
        traza_definida_positiva_AdS        (_AH3, _AF3, _AF5, _A3N3, _AD5, variables_numericas['tau'], variables_numericas['s']) +
        gradient_modulus_AdS               (_AH3, _AF3, _AF5, _A3N3, _AD5, variables_numericas['tau'], variables_numericas['s']) +
        no_taquionico_AdS                  (_AH3, _AF3, _AF5, _A3N3, _AD5, variables_numericas['tau'], variables_numericas['s'])
    )

##### Función de error de variables fijas
def fitness_function_vars(_s, _tau):
    global variables_numericas
    return (
        potencial_semidefinido_positivo    (variables_numericas['AH3'], variables_numericas['AF3'], variables_numericas['AF5'], variables_numericas['A3N3'], _tau, _s) +
        traza_definida_positiva            (variables_numericas['AH3'], variables_numericas['AF3'], variables_numericas['AF5'], variables_numericas['A3N3'], _tau, _s) +
        gradient_modulus                   (variables_numericas['AH3'], variables_numericas['AF3'], variables_numericas['AF5'], variables_numericas['A3N3'], _tau, _s) +
        no_taquionico                      (variables_numericas['AH3'], variables_numericas['AF3'], variables_numericas['AF5'], variables_numericas['A3N3'], _tau, _s)
    )

def fitness_function_vars_AdS(_s, _tau):
    global variables_numericas
    return (
        potencial_semidefinido_positivo_AdS(variables_numericas['AH3'], variables_numericas['AF3'], variables_numericas['AF5'], variables_numericas['A3N3'], variables_numericas['AD5'], _tau, _s) +
        traza_definida_positiva_AdS        (variables_numericas['AH3'], variables_numericas['AF3'], variables_numericas['AF5'], variables_numericas['A3N3'], variables_numericas['AD5'], _tau, _s) +
        gradient_modulus_AdS               (variables_numericas['AH3'], variables_numericas['AF3'], variables_numericas['AF5'], variables_numericas['A3N3'], variables_numericas['AD5'], _tau, _s) +
        no_taquionico_AdS                  (variables_numericas['AH3'], variables_numericas['AF3'], variables_numericas['AF5'], variables_numericas['A3N3'], variables_numericas['AD5'], _tau, _s)
    )


### FUNCIONES DE EVALUACIÓN (DESCRIPTORES DEL POTENCIAL)

##### Función de autovalores
def autovalores_VHess(_AH3, _AF3, _AF5, _A3N3, _tau, _s):
    return [
        ev.subs([
            (AH3, _AH3),
            (AF3, _AF3),
            (AF5, _AF5),
            (A3N3, _A3N3),
            (tau, _tau),
            (s, _s)
        ]).evalf()
        for ev in eigenvals_VHess.keys()
    ]

def autovalores_VHess_AdS(_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s):
    return [
        ev.subs([
            (AH3, _AH3),
            (AF3, _AF3),
            (AF5, _AF5),
            (A3N3, _A3N3),
            (AD5, _AD5),
            (tau, _tau),
            (s, _s)
        ]).evalf()
        for ev in eigenvals_VHess_lifting.keys()
    ]

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

##### Evaluación de la función potencial
def potencial_eval(_AH3, _AF3, _AF5, _A3N3, _tau, _s):
    global precision_decimal
    val=V.subs([
        (AH3, _AH3),
        (AF3, _AF3),
        (AF5, _AF5),
        (A3N3, _A3N3),
        (tau, _tau),
        (s, _s)
    ]).evalf(precision_decimal)
    return val

def potencial_eval_AdS(_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s):
    global precision_decimal
    val=V.subs([
        (AH3, _AH3),
        (AF3, _AF3),
        (AF5, _AF5),
        (A3N3, _A3N3),
        (AD5, _AD5),
        (tau, _tau),
        (s, _s)
    ]).evalf(precision_decimal)
    return val

##### Graficar funcion potencial
def plot_potencial_vars(_tau, _s, show=True, save=None):
    global variables_numericas
    global precision_decimal

    print("Graficando con los valores", variables_numericas["AH3"], variables_numericas["AF3"], variables_numericas["AF5"], variables_numericas["A3N3"], _tau, _s)

    lims = {
        "s": {
            "min": _s * 0.9,
            "max": _s * 1.1
        },
        "tau": {
            "min": _tau * 0.9,
            "max": [ _tau * 2.1, _tau * 1.1 ]
        }
    }

    s_vals   = np.linspace(lims["s"  ]["min"], lims["s"  ]["max"]   , 1000)
    tau_vals = np.linspace(lims["tau"]["min"], lims["tau"]["max"][1], 1000)

    V_s  = V.subs([
        (AH3, variables_numericas["AH3"]),
        (AF3, variables_numericas["AF3"]),
        (AF5, variables_numericas["AF5"]),
        (A3N3, variables_numericas["A3N3"]),
        (tau, _tau),
    ])
    V_tau= V.subs([
        (AH3,  variables_numericas["AH3"]),
        (AF3,  variables_numericas["AF3"]),
        (AF5,  variables_numericas["AF5"]),
        (A3N3, variables_numericas["A3N3"]),
        (s, _s)
    ])

    vs_vals   = [ V_s.subs  (s, s_val    ).evalf(precision_decimal) for s_val   in s_vals   ]
    vtau_vals = [ V_tau.subs(tau, tau_val).evalf(precision_decimal) for tau_val in tau_vals ]

    figura, axiales = plt.subplots(1, 2, figsize=(12, 5))

    axiales[0].plot(s_vals, vs_vals, 'r-', linewidth=2)
    axiales[0].set_xlabel('s', fontsize=14)
    axiales[0].set_ylabel('V(s, τ₀)', fontsize=14)
    axiales[0].set_title(f'V(s) with τ fixed at {_tau:.4f}', fontsize=16)
    axiales[0].grid(True, alpha=0.3)
    axiales[0].axhline(y=0, color='k', linestyle=':', alpha=0.5)

    axiales[1].plot(tau_vals, vtau_vals, 'r-', linewidth=2)
    axiales[1].set_xlabel('τ', fontsize=14)
    axiales[1].set_ylabel('V(s₀, τ)', fontsize=14)
    axiales[1].set_title(f'V(τ) with s fixed at {_s:.4f}', fontsize=16)
    axiales[1].grid(True, alpha=0.3)
    axiales[1].axhline(y=0, color='k', linestyle=':', alpha=0.5)

    if save:
        plt.savefig(save)

    if show:
        plt.show()

def plot_potencial_vars_adS(s_adS, tau_adS, show=True, save=None):
    global variables_numericas
    global precision_decimal
    global V

    # Ranges for RED plots
    # s: ×1.1, τ: ×1.1 (narrower range for red)
    s_vals = np.linspace(s_adS * 0.9, s_adS * 1.1, 1000)
    tau_vals = np.linspace(tau_adS * 0.9, tau_adS * 1.1, 1000)  # ×1.1 for red!

    # V(s) with τ fixed at AdS τ value
    V_s_red = V.subs([
        (AH3, variables_numericas["AH3"]),
        (AF3, variables_numericas["AF3"]),
        (AF5, variables_numericas["AF5"]),
        (A3N3, variables_numericas["A3N3"]),
        (tau, tau_adS),  # Fixed at AdS τ
    ])

    # V(τ) with s fixed at AdS s value
    V_tau_red = V.subs([
        (AH3,  variables_numericas["AH3"]),
        (AF3,  variables_numericas["AF3"]),
        (AF5,  variables_numericas["AF5"]),
        (A3N3, variables_numericas["A3N3"]),
        (s, s_adS),  # Fixed at AdS s
    ])

    # Evaluate
    vs_vals_red = [float(V_s_red.subs(s, s_val).evalf(precision_decimal))
                   for s_val in s_vals]
    vtau_vals_red = [float(V_tau_red.subs(tau, tau_val).evalf(precision_decimal))
                     for tau_val in tau_vals]

    # Create subplots
    figura, axiales = plt.subplots(1, 2, figsize=(12, 5))

    # RED Plot 1: V(s) at AdS τ
    axiales[0].plot(s_vals, vs_vals_red, 'r-', linewidth=2)
    axiales[0].set_xlabel('s', fontsize=14)
    axiales[0].set_ylabel('V(s, τₐ)', fontsize=14)
    axiales[0].set_title(f'Red: V(s) with τ fixed at {tau_adS:.4f} (AD5=0)', fontsize=16)
    axiales[0].grid(True, alpha=0.3)
    axiales[0].axhline(y=0, color='k', linestyle=':', alpha=0.5)
    axiales[0].scatter([s_adS], [float(V_s_red.subs(s, s_adS).evalf(precision_decimal))],
                       color='red', s=80, zorder=5)

    # RED Plot 2: V(τ) at AdS s (narrow range)
    axiales[1].plot(tau_vals, vtau_vals_red, 'r-', linewidth=2)
    axiales[1].set_xlabel('τ', fontsize=14)
    axiales[1].set_ylabel('V(sₐ, τ)', fontsize=14)
    axiales[1].set_title(f'Red: V(τ) with s fixed at {s_adS:.4f} (AD5=0, range ×1.1)', fontsize=16)
    axiales[1].grid(True, alpha=0.3)
    axiales[1].axhline(y=0, color='k', linestyle=':', alpha=0.5)
    axiales[1].scatter([tau_adS], [float(V_tau_red.subs(tau, tau_adS).evalf(precision_decimal))],
                       color='red', s=80, zorder=5)

    plt.tight_layout()

    if save:
        plt.savefig(save, dpi=300, bbox_inches='tight')

    if show:
        plt.show()

    return figura


def plot_potencial_coef(_AH3, _AF3, _AF5, _A3N3):
    pass

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
