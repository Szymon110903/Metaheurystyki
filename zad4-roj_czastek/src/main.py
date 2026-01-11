import matplotlib.pyplot as plt
from particle_swarm_optimization import ParticleSwarmOptimization
from functions import *

parametry = {
    'objective_function': booth_function,
    'bounds': [(-10, 10), (-10, 10)], # this indicates in what dimension it will work
    'num_particles': 50,
    'num_iterations': 100,
    'w': 0.75, # inertia constant
    'c1': 1.0, # cognative constant
    'c2': 2.0, # social constant,
    'v_max': 1.0,
    'minimization': True
}

bounds = [(-10, 10), (-10, 10)]
pso = ParticleSwarmOptimization(
    parametry['objective_function'],
    parametry['bounds'],
    parametry['num_particles'],
    parametry['num_iterations'],
    parametry['w'],
    parametry['c1'],
    parametry['c2'],
    parametry['v_max'],
    parametry['minimization']
)
best_pos, best_val, history = pso.run(patience=20, plot=True, pause=0.05)
print("best_pos:", best_pos)
print("best_val:", best_val)