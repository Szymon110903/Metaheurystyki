import matplotlib.pyplot as plt
from particle_swarm_optimization import ParticleSwarmOptimization
from functions import *
import numpy as np

# # booth_function
# # himmelblaus_function
parametry = {
    'objective_function': booth_function,
    'bounds': [(-10, 10), (-10, 10)], 
    'num_particles': 50,
    'num_iterations': 100,
    'w': 0.75, 
    'c1': 1.0, 
    'c2': 2.0, 
    'v_max': 1.0,
    'minimization': True
}

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



# NAZWA_BADANIA = "4 - Funkcja Bootha - v_max = 5.0   "

# # booth_function
# # himmelblaus_function

# parametry = {
#     'objective_function': booth_function, 
#     'bounds': [(-10, 10), (-10, 10)], 
#     'num_particles': 50,
#     'num_iterations': 200,
#     'w': 0.75,     # Inercja
#     'c1': 1.5,     # Kognitywny
#     'c2': 1.5,     # Socjalny
#     'v_max': 5.0,
#     'minimization': True 
# }



# print(f"\n=== ROZPOCZYNAM: {NAZWA_BADANIA} ===")
# print("Trwa obliczanie 5 niezależnych przebiegów...")

# wyniki_val = []  
# historie = []   

# for i in range(5):
#     pso = ParticleSwarmOptimization(
#         parametry['objective_function'],
#         parametry['bounds'],
#         parametry['num_particles'],
#         parametry['num_iterations'],
#         parametry['w'],
#         parametry['c1'],
#         parametry['c2'],
#         parametry['v_max'],
#         parametry['minimization']
#     )
    
#     best_pos, best_val, history = pso.run(patience=20, plot=False)
    
#     wyniki_val.append(best_val)
#     historie.append(history)
    
#     x = best_pos[0]
#     y = best_pos[1]
    
#     print(f"  Próba {i+1}: Wynik = {best_val:.6e} | Znaleziono w: x={x:.6f}, y={y:.6f}")

# best = np.min(wyniki_val)
# worst = np.max(wyniki_val)
# mean = np.mean(wyniki_val)
# median = np.median(wyniki_val)
# std = np.std(wyniki_val)

# print("\n" + "="*40)
# print(f"TABELA WYNIKÓW: {NAZWA_BADANIA}")
# print("="*40)
# print(f"Najlepszy (Best):   {best:.6e}")
# print(f"Najgorszy (Worst):  {worst:.6e}")
# print(f"Średnia (Mean):     {mean:.6e}")
# print(f"Mediana:            {median:.6e}")
# print(f"Odchylenie (Std):   {std:.6e}")
# print("="*40)


# plt.figure(figsize=(10, 6))

# for idx, hist in enumerate(historie):
#     plt.plot(hist, label=f'Próba {idx+1}', alpha=0.6)

# max_len = max(len(h) for h in historie)
# histories_padded = []
# for h in historie:
#     histories_padded.append(h + [h[-1]] * (max_len - len(h)))
# mean_history = np.mean(histories_padded, axis=0)

# plt.plot(mean_history, color='black', linewidth=2.5, linestyle='--', label='Średnia')

# plt.title(f"Zbieżność algorytmu PSO\n{NAZWA_BADANIA}")
# plt.xlabel("Iteracja")
# plt.ylabel("Wartość funkcji celu (skala log)")
# plt.yscale('log') 
# plt.grid(True, which="both", ls="-", alpha=0.4)
# plt.legend()

# plt.show()