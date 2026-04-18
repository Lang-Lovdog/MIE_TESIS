import numpy as np
from deap import base, creator, tools
from ..xp import xp

def meallike_repr(cls):
    def __repr__(self):
        # Extraemos los atributos definidos en el __init__
        params = ", ".join([f"{k}={v}" for k, v in self.__dict__.items()
                           if not k.startswith('_') and k != 'toolbox'])
        return f"{self.__class__.__name__}({params})"

    cls.__repr__ = __repr__
    cls.__str__ = __repr__
    return cls

@meallike_repr
class UMDA:
    def __init__(self, epoch=100, pop_size=50, selection_ratio=0.2):
        self.epoch = epoch
        self.pop_size = pop_size
        self.sel_ratio = selection_ratio

        # Evitar re-crear clases si se llama múltiples veces
        if not hasattr(creator, "FitnessMin"):
            creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
            creator.create("Individual", list, fitness=creator.FitnessMin)

        self.toolbox = base.Toolbox()

    def solve(self, problem_dict):
        lb = problem_dict['bounds'].lb
        ub = problem_dict['bounds'].ub
        fit_func = problem_dict['obj_func']
        dim = len(lb)

        # Población inicial
        pop = [creator.Individual(np.random.uniform(lb, ub, dim).tolist()) for _ in range(self.pop_size)]

        for g in range(self.epoch):
            # EVALUACIÓN VECTORIZADA: Convertimos a CuPy una sola vez por generación
            pop_matrix = xp.array([list(ind) for ind in pop])
            fitnesses = fit_func(pop_matrix)

            for ind, fit in zip(pop, fitnesses):
                ind.fitness.values = (float(fit),)

            # Selección del top (UMDA se basa en la élite para re-estimar)
            selected = tools.selBest(pop, int(self.pop_size * self.sel_ratio))

            # Estimación de la distribución en GPU
            sel_matrix = xp.array([list(ind) for ind in selected])
            mu = xp.mean(sel_matrix, axis=0)
            sigma = xp.std(sel_matrix, axis=0) + 1e-6

            # Generar siguiente generación
            pop = []
            for _ in range(self.pop_size):
                # Muestreo y clipping físico
                child = np.random.normal(xp.asnumpy(mu), xp.asnumpy(sigma))
                child = np.clip(child, lb, ub)
                pop.append(creator.Individual(child.tolist()))

        best_ind = tools.selBest(pop, 1)[0]
        return np.array(best_ind), best_ind.fitness.values[0]


@meallike_repr
class PBIL:
    def __init__(self, epoch=100, pop_size=50, learning_rate=0.1):
        self.epoch = epoch
        self.pop_size = pop_size
        self.lr = learning_rate

        if not hasattr(creator, "FitnessMin"):
            creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
            creator.create("Individual", list, fitness=creator.FitnessMin)

    def solve(self, problem_dict):
        lb = np.array(problem_dict['bounds'].lb)
        ub = np.array(problem_dict['bounds'].ub)
        fit_func = problem_dict['obj_func']
        dim = len(lb)

        # Vectores de probabilidad (inicializados al centro de los bounds)
        mu_vec = (lb + ub) / 2.0
        sigma_vec = (ub - lb) / 4.0

        for g in range(self.epoch):
            # Muestreo basado en el vector actual
            pop = []
            for _ in range(self.pop_size):
                child = np.random.normal(mu_vec, sigma_vec)
                child = np.clip(child, lb, ub)
                pop.append(creator.Individual(child.tolist()))

            # Evaluación en GPU
            pop_matrix = xp.array([list(ind) for ind in pop])
            fitnesses = fit_func(pop_matrix)

            for ind, fit in zip(pop, fitnesses):
                ind.fitness.values = (float(fit),)

            # PBIL: Aprendizaje incremental del mejor
            best_ind = tools.selBest(pop, 1)[0]

            # Actualizamos el vector mu hacia el mejor individuo
            mu_vec = (1.0 - self.lr) * mu_vec + self.lr * np.array(best_ind)

        best_ind = tools.selBest(pop, 1)[0]
        return np.array(best_ind), best_ind.fitness.values[0]

