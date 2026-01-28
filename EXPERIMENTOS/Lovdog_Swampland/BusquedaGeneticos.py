import mealpy as mp
from MetastableVacua import fitness_function as ff

#### Creación de un genético simple para minimización de la función ff
genetico = mp.GeneticAlgorithm(
    pop_size=100,
    mutation_prob=0.1,
    mutation_distrib=[-0.1, 0.1],
    crossover_prob=0.9,
    elit_ratio=0.1,
    parents_portion=0.3,
    mutation_by_replacement=True,
    mutation_step=0.1,
    mutation_by_neighborhood=True,
    mutation_neighborhood_size=5,
    mutation_distrib_size=10,
    fitness_func=ff,
    maximize=True,
    verbose=1
)
#### Creación de un genético simple para minimización de la función ff

genetico.run()

print(genetico.best_individual())

print(genetico.best_fitness())

print(genetico.best_chromosome())

print(genetico.best_solution())
