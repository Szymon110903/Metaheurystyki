import pandas as pd
from genetic_algorithm import GeneticAlgorithm
import os
import matplotlib.pyplot as plt

# ----- import danych -----
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, 'data', 'problem_plecakowy_dane_tabulatory.csv')
df = pd.read_csv(filepath_or_buffer=data_path, sep='\t')

# usuniecie spacji z liczb i konwersja na int
df["Waga (kg)"] = df["Waga (kg)"].str.replace(" ", "").astype(int)
df["Wartość (zł)"] = df["Wartość (zł)"].str.replace(" ", "").astype(int)

# stworzenie list
weights = df["Waga (kg)"].tolist()
values = df["Wartość (zł)"].tolist()

# ----- wywołanie algorytmu -----

parametry_algorytmu = {
    "lista_wag": weights,
    "lista_wartosci": values,
    "pojemnosc_plecaka": 6404180,
    "wielkosc_populacji": 100,
    "ilosc_iteracji": 1000,
    "Pc": 0.8,
    "Pm": 0.05,
    "metoda_selekcji": 'roulette', # 'roulette' | 'tournament' | 'ranking'
    "metoda_krzyżowania": 'uniform', # 'one_point' | 'two_point' | 'uniform'
    "metoda_mutacji": 'bit_flip'
}


ga = GeneticAlgorithm(
    weights=parametry_algorytmu["lista_wag"],
    values=parametry_algorytmu["lista_wartosci"],
    capacity=parametry_algorytmu["pojemnosc_plecaka"],
    population_size=parametry_algorytmu["wielkosc_populacji"],
    generations=parametry_algorytmu["ilosc_iteracji"],
    crossover_prob=parametry_algorytmu["Pc"],
    mutation_prob=parametry_algorytmu["Pm"],
    selection_method=parametry_algorytmu["metoda_selekcji"],
    crossover_method=parametry_algorytmu["metoda_krzyżowania"],
    mutation_method=parametry_algorytmu["metoda_mutacji"],
)

result = ga.run()

print("Najlepszy wynik (zł): ", result["best_value"])
print("Osiągnięta waga (kg) rozwiazania: ", result["best_weight"])
print("Różnica wartości wag: capacity - best_weight = ", (6404180 - result["best_weight"]))
print("Najlepszy osobnik: ", result["best_individual"])
print("Czas wykonania: ", result["execution_time"], "s")
print("Generowanie wykresów...")

best_history = result["best_history"]
avg_history = result["avg_solutions_history"]
worst_history = result["worst_history"]
iterations = range(1, len(best_history) + 1)

plt.figure(figsize=(10, 6))
plt.plot(iterations, best_history, label='Najlepszy wynik (osobnik najlepszy)', color='green')
plt.plot(iterations, avg_history, label='Średni wynik dla populacji', color='blue')


plt.title('Zbieżność Algorytmu Genetycznego')
plt.xlabel('Iteracja')
plt.ylabel('Wartość funkcji przystosowania (Fitness)')
plt.legend()
plt.grid(True)
plt.show()