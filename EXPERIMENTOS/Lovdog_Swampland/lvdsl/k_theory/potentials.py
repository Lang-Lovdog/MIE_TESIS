### Este script se basa en el experimento descrito por el artículo
###  Metastable vacua from torsion and machine learning
### de Cesar Damian y Oscar Loaiza-Brito
### https://doi.org/10.1140/epjc/s10052-022-11118-x

## IMPORTS
import sys
import                          matplotlib.pyplot    as plt #type: ignore
import                          sympy                as sp  #type: ignore
from   ..xp              import xp
from   ..xp              import np
from   ..xp              import HAS_GPU
from   .vars              import V_lambda                    as v
from   .vars              import V_lifting_lambda            as v_l
from   .vars              import VHess_lambda                as hess
from   .vars              import V_liftingHess_lambda        as hess_l
from   .vars              import VHess_eig_lambda            as eig
from   .vars              import V_liftingHess_eig_lambda    as eig_l
from   .vars              import V_Hess_tr_lambda            as tr
from   .vars              import V_liftingHess_tr_lambda     as tr_l
from   .vars              import V_gradient_lambda           as dv
from   .vars              import V_lifting_gradient_lambda   as dv_l
from   .vars              import V_Hess_det_lambda           as det
from   .vars              import V_liftingHess_det_lambda    as det_l
from   .vars              import variables_numericas
## IMPORTS



##### Definición de las funciones de error

## Evaluadores
def positive_semidefinite_potential_nolift(_AH3, _AF3, _AF5, _A3N3, _tau, _s):
    val=v(_AH3, _AF3, _AF5, _A3N3, _tau, _s)
    return xp.abs(val)-val

def positive_semidefinite_potential_lift(_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s):
    val=v_l(_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s)
    return xp.abs(val)-val

def positive_definite_trace_nolift(_AH3, _AF3, _AF5, _A3N3, _tau, _s):
    val = tr(_AH3, _AF3, _AF5, _A3N3, _tau, _s)
    return xp.abs(val)-val

def positive_definite_trace_lift(_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s):
    val = tr_l(_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s)
    return xp.abs(val)-val

def modulus_gradient_nolift(_AH3, _AF3, _AF5, _A3N3, _tau, _s):
    diV2 = xp.pow(dv[0](_AH3,_AF3,_AF5,_A3N3,_tau,_s),2) +\
           xp.pow(dv[1](_AH3,_AF3,_AF5,_A3N3,_tau,_s),2)
    return diV2

def modulus_gradient_lift(_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s):
    diV2 = xp.pow(dv_l[0](_AH3,_AF3,_AF5,_A3N3,_tau,_s),2) +\
           xp.pow(dv_l[1](_AH3,_AF3,_AF5,_A3N3,_tau,_s),2)
    return diV2

def tachion_level_nolift(_AH3, _AF3, _AF5, _A3N3, _tau, _s):
    f_val = det(_AH3, _AF3, _AF5, _A3N3, _tau, _s) - tr(_AH3, _AF3, _AF5, _A3N3, _tau, _s)/4.0
    return xp.abs(f_val)-f_val

def tachion_level_lift(_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s):
    f_val = det_l(_AH3, _AF3, _AF5, _A3N3, _tau, _s) - tr_l(_AH3, _AF3, _AF5, _A3N3, _tau, _s)/4.0
    return xp.abs(f_val)-f_val

if HAS_GPU:
##### Función general de error
    def fitness_function_nolift(_AH3, _AF3, _AF5, _A3N3, _tau, _s):
        return xp.asnumpy(
            positive_semidefinite_potential_nolift(_AH3, _AF3, _AF5, _A3N3, _tau, _s) +
            positive_definite_trace_nolift        (_AH3, _AF3, _AF5, _A3N3, _tau, _s) +
            modulus_gradient_nolift               (_AH3, _AF3, _AF5, _A3N3, _tau, _s) +
            tachion_level_nolift                  (_AH3, _AF3, _AF5, _A3N3, _tau, _s)
        )

    def fitness_function_nolift_mealpy(solutions):
        _AH3, _AF3, _AF5, _A3N3, _tau, _s = solutions
        return xp.asnumpy(
            positive_semidefinite_potential_nolift(_AH3, _AF3, _AF5, _A3N3, _tau, _s) +
            positive_definite_trace_nolift        (_AH3, _AF3, _AF5, _A3N3, _tau, _s) +
            modulus_gradient_nolift               (_AH3, _AF3, _AF5, _A3N3, _tau, _s) +
            tachion_level_nolift                  (_AH3, _AF3, _AF5, _A3N3, _tau, _s)
        )

    def fitness_function_lift(_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s):
        return xp.asnumpy(
            positive_semidefinite_potential_lift  (_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s) +
            positive_definite_trace_lift          (_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s) +
            modulus_gradient_lift                 (_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s) +
            tachion_level_lift                    (_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s)
        )

    def fitness_function_lift_mealpy(solutions):
        _AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s = solutions
        return xp.asnumpy(
            positive_semidefinite_potential_lift  (_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s) +
            positive_definite_trace_lift          (_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s) +
            modulus_gradient_lift                 (_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s) +
            tachion_level_lift                    (_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s)
        )

##### Función de error de coeficientes fijos
    def fitness_function_fixedmoduli_nolift(_AH3, _AF3, _AF5, _A3N3):
        global variables_numericas
        return xp.asnumpy(
            positive_semidefinite_potential_nolift(_AH3, _AF3, _AF5, _A3N3, variables_numericas['tau'], variables_numericas['s']) +
            positive_definite_trace_nolift        (_AH3, _AF3, _AF5, _A3N3, variables_numericas['tau'], variables_numericas['s']) +
            modulus_gradient_nolift               (_AH3, _AF3, _AF5, _A3N3, variables_numericas['tau'], variables_numericas['s']) +
            tachion_level_nolift                  (_AH3, _AF3, _AF5, _A3N3, variables_numericas['tau'], variables_numericas['s'])
        )

    def fitness_function_fixedmoduli_nolift_mealpy(solutions):
        global variables_numericas

        _AH3, _AF3, _AF5, _A3N3 = solutions

        return xp.asnumpy(
            positive_semidefinite_potential_nolift(_AH3, _AF3, _AF5, _A3N3, variables_numericas['tau'], variables_numericas['s']) +
            positive_definite_trace_nolift        (_AH3, _AF3, _AF5, _A3N3, variables_numericas['tau'], variables_numericas['s']) +
            modulus_gradient_nolift               (_AH3, _AF3, _AF5, _A3N3, variables_numericas['tau'], variables_numericas['s']) +
            tachion_level_nolift                  (_AH3, _AF3, _AF5, _A3N3, variables_numericas['tau'], variables_numericas['s'])
        )

    def fitness_function_fixedmoduli_lift(_AH3, _AF3, _AF5, _A3N3, _AD5):
        global variables_numericas
        return xp.asnumpy(
            positive_semidefinite_potential_lift  (_AH3, _AF3, _AF5, _A3N3, _AD5, variables_numericas['tau'], variables_numericas['s']) +
            positive_definite_trace_lift          (_AH3, _AF3, _AF5, _A3N3, _AD5, variables_numericas['tau'], variables_numericas['s']) +
            modulus_gradient_lift                 (_AH3, _AF3, _AF5, _A3N3, _AD5, variables_numericas['tau'], variables_numericas['s']) +
            tachion_level_lift                    (_AH3, _AF3, _AF5, _A3N3, _AD5, variables_numericas['tau'], variables_numericas['s'])
        )

    def fitness_function_fixedmoduli_lift_mealpy(solutions):
        global variables_numericas

        _AH3, _AF3, _AF5, _A3N3, _AD5 = solutions

        return xp.asnumpy(
            positive_semidefinite_potential_lift  (_AH3, _AF3, _AF5, _A3N3, _AD5, variables_numericas['tau'], variables_numericas['s']) +
            positive_definite_trace_lift          (_AH3, _AF3, _AF5, _A3N3, _AD5, variables_numericas['tau'], variables_numericas['s']) +
            modulus_gradient_lift                 (_AH3, _AF3, _AF5, _A3N3, _AD5, variables_numericas['tau'], variables_numericas['s']) +
            tachion_level_lift                    (_AH3, _AF3, _AF5, _A3N3, _AD5, variables_numericas['tau'], variables_numericas['s'])
        )

##### Función de error de variables fijas
    def fitness_function_fixedcoeff_nolift(_s, _tau):
        global variables_numericas
        return xp.asnumpy(
            positive_semidefinite_potential_nolift(variables_numericas['AH3'], variables_numericas['AF3'], variables_numericas['AF5'], variables_numericas['A3N3'], _tau, _s) +
            positive_definite_trace_nolift        (variables_numericas['AH3'], variables_numericas['AF3'], variables_numericas['AF5'], variables_numericas['A3N3'], _tau, _s) +
            modulus_gradient_nolift               (variables_numericas['AH3'], variables_numericas['AF3'], variables_numericas['AF5'], variables_numericas['A3N3'], _tau, _s) +
            tachion_level_nolift                  (variables_numericas['AH3'], variables_numericas['AF3'], variables_numericas['AF5'], variables_numericas['A3N3'], _tau, _s)
        )

    def fitness_function_fixedcoeff_lift(_s, _tau):
        global variables_numericas
        return xp.asnumpy(
            positive_semidefinite_potential_lift  (variables_numericas['AH3'], variables_numericas['AF3'], variables_numericas['AF5'], variables_numericas['A3N3'], variables_numericas['AD5'], _tau, _s) +
            positive_definite_trace_lift          (variables_numericas['AH3'], variables_numericas['AF3'], variables_numericas['AF5'], variables_numericas['A3N3'], variables_numericas['AD5'], _tau, _s) +
            modulus_gradient_lift                 (variables_numericas['AH3'], variables_numericas['AF3'], variables_numericas['AF5'], variables_numericas['A3N3'], variables_numericas['AD5'], _tau, _s) +
            tachion_level_lift                    (variables_numericas['AH3'], variables_numericas['AF3'], variables_numericas['AF5'], variables_numericas['A3N3'], variables_numericas['AD5'], _tau, _s)
        )
else:
##### Función general de error
    def fitness_function_nolift(_AH3, _AF3, _AF5, _A3N3, _tau, _s):
        return (
            positive_semidefinite_potential_nolift(_AH3, _AF3, _AF5, _A3N3, _tau, _s) +
            positive_definite_trace_nolift        (_AH3, _AF3, _AF5, _A3N3, _tau, _s) +
            modulus_gradient_nolift               (_AH3, _AF3, _AF5, _A3N3, _tau, _s) +
            tachion_level_nolift                  (_AH3, _AF3, _AF5, _A3N3, _tau, _s)
        )

    def fitness_function_nolift_mealpy(solutions):
        _AH3, _AF3, _AF5, _A3N3, _tau, _s = solutions
        return (
            positive_semidefinite_potential_nolift(_AH3, _AF3, _AF5, _A3N3, _tau, _s) +
            positive_definite_trace_nolift        (_AH3, _AF3, _AF5, _A3N3, _tau, _s) +
            modulus_gradient_nolift               (_AH3, _AF3, _AF5, _A3N3, _tau, _s) +
            tachion_level_nolift                  (_AH3, _AF3, _AF5, _A3N3, _tau, _s)
        )

    def fitness_function_lift(_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s):
        return (
            positive_semidefinite_potential_lift  (_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s) +
            positive_definite_trace_lift          (_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s) +
            modulus_gradient_lift                 (_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s) +
            tachion_level_lift                    (_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s)
        )

    def fitness_function_lift_mealpy(solutions):
        _AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s = solutions
        return (
            positive_semidefinite_potential_lift  (_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s) +
            positive_definite_trace_lift          (_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s) +
            modulus_gradient_lift                 (_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s) +
            tachion_level_lift                    (_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s)
        )

##### Función de error de coeficientes fijos
    def fitness_function_coef_nolift(_AH3, _AF3, _AF5, _A3N3):
        global variables_numericas
        return (
            positive_semidefinite_potential_nolift(_AH3, _AF3, _AF5, _A3N3, variables_numericas['tau'], variables_numericas['s']) +
            positive_definite_trace_nolift        (_AH3, _AF3, _AF5, _A3N3, variables_numericas['tau'], variables_numericas['s']) +
            modulus_gradient_nolift               (_AH3, _AF3, _AF5, _A3N3, variables_numericas['tau'], variables_numericas['s']) +
            tachion_level_nolift                  (_AH3, _AF3, _AF5, _A3N3, variables_numericas['tau'], variables_numericas['s'])
        )

    def fitness_function_coef_nolift_mealpy(solutions):
        global variables_numericas

        _AH3, _AF3, _AF5, _A3N3 = solutions

        return (
            positive_semidefinite_potential_nolift(_AH3, _AF3, _AF5, _A3N3, variables_numericas['tau'], variables_numericas['s']) +
            positive_definite_trace_nolift        (_AH3, _AF3, _AF5, _A3N3, variables_numericas['tau'], variables_numericas['s']) +
            modulus_gradient_nolift               (_AH3, _AF3, _AF5, _A3N3, variables_numericas['tau'], variables_numericas['s']) +
            tachion_level_nolift                  (_AH3, _AF3, _AF5, _A3N3, variables_numericas['tau'], variables_numericas['s'])
        )

    def fitness_function_coef_lift(_AH3, _AF3, _AF5, _A3N3, _AD5):
        global variables_numericas
        return (
            positive_semidefinite_potential_lift  (_AH3, _AF3, _AF5, _A3N3, _AD5, variables_numericas['tau'], variables_numericas['s']) +
            positive_definite_trace_lift          (_AH3, _AF3, _AF5, _A3N3, _AD5, variables_numericas['tau'], variables_numericas['s']) +
            modulus_gradient_lift                 (_AH3, _AF3, _AF5, _A3N3, _AD5, variables_numericas['tau'], variables_numericas['s']) +
            tachion_level_lift                    (_AH3, _AF3, _AF5, _A3N3, _AD5, variables_numericas['tau'], variables_numericas['s'])
        )

    def fitness_function_coef_lift_mealpy(solutions):
        global variables_numericas

        _AH3, _AF3, _AF5, _A3N3, _AD5 = solutions

        return (
            positive_semidefinite_potential_lift  (_AH3, _AF3, _AF5, _A3N3, _AD5, variables_numericas['tau'], variables_numericas['s']) +
            positive_definite_trace_lift          (_AH3, _AF3, _AF5, _A3N3, _AD5, variables_numericas['tau'], variables_numericas['s']) +
            modulus_gradient_lift                 (_AH3, _AF3, _AF5, _A3N3, _AD5, variables_numericas['tau'], variables_numericas['s']) +
            tachion_level_lift                    (_AH3, _AF3, _AF5, _A3N3, _AD5, variables_numericas['tau'], variables_numericas['s'])
        )

##### Función de error de variables fijas
    def fitness_function_fixedcoeff_nolift(_s, _tau):
        global variables_numericas
        return (
            positive_semidefinite_potential_nolift(variables_numericas['AH3'], variables_numericas['AF3'], variables_numericas['AF5'], variables_numericas['A3N3'], _tau, _s) +
            positive_definite_trace_nolift        (variables_numericas['AH3'], variables_numericas['AF3'], variables_numericas['AF5'], variables_numericas['A3N3'], _tau, _s) +
            modulus_gradient_nolift               (variables_numericas['AH3'], variables_numericas['AF3'], variables_numericas['AF5'], variables_numericas['A3N3'], _tau, _s) +
            tachion_level_nolift                  (variables_numericas['AH3'], variables_numericas['AF3'], variables_numericas['AF5'], variables_numericas['A3N3'], _tau, _s)
        )

    def fitness_function_fixedcoeff_lift(_s, _tau):
        global variables_numericas
        return (
            positive_semidefinite_potential_lift  (variables_numericas['AH3'], variables_numericas['AF3'], variables_numericas['AF5'], variables_numericas['A3N3'], variables_numericas['AD5'], _tau, _s) +
            positive_definite_trace_lift          (variables_numericas['AH3'], variables_numericas['AF3'], variables_numericas['AF5'], variables_numericas['A3N3'], variables_numericas['AD5'], _tau, _s) +
            modulus_gradient_lift                 (variables_numericas['AH3'], variables_numericas['AF3'], variables_numericas['AF5'], variables_numericas['A3N3'], variables_numericas['AD5'], _tau, _s) +
            tachion_level_lift                    (variables_numericas['AH3'], variables_numericas['AF3'], variables_numericas['AF5'], variables_numericas['A3N3'], variables_numericas['AD5'], _tau, _s)
        )


### FUNCIONES DE EVALUACIÓN (DESCRIPTORES DEL POTENCIAL)

##### Función de autovalores
def vhess_eigenvals_nolift(_ah3, _af3, _af5, _a3n3, _tau, _s):
    return  eig(_ah3, _af3, _af5, _a3n3, _tau, _s)

def vhess_eigenvals_lift(_ah3, _af3, _af5, _a3n3, _ad5, _tau, _s):
    return  eig_l(_ah3, _af3, _af5, _a3n3, _tau, _s)


##### Evaluación de la función potencial
def effective_potential_nolift(_AH3, _AF3, _AF5, _A3N3, _tau, _s):
    return v(_AH3, _AF3, _AF5, _A3N3, _tau, _s)

def effective_potential_lift(_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s):
    return v_l(_AH3, _AF3, _AF5, _A3N3, _AD5, _tau, _s)

