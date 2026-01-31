from pathlib import Path
from vrptw.parser import load_solomon
from vrptw.distance import build_distance_matrix
from vrptw.models import *
from vrptw.evaluation import evaluate_solution
from vrptw.construction import build_initial_solution_ready_time
from vrptw.utils import plot_solution
from vrptw.genetic_algorithm import GeneticAlgorithm
from matplotlib import pyplot as plt

if __name__ == "__main__":
    base = Path(__file__).resolve().parents[1]
    data_dir = base / "data" / "solomon_100"
    name, max_vehicles, capacity, depot, customers = load_solomon(data_dir / "r101.txt")

    nodes = [depot] + customers
    dist = build_distance_matrix(nodes)

    sol_init = build_initial_solution_ready_time(nodes, dist, capacity, max_vehicles)
    score_init = evaluate_solution(nodes, dist, capacity, max_vehicles, sol_init)

    print("\n--- ROZWIĄZANIE POCZĄTKOWE ---")
    print(f"Pojazdy: {score_init.vehicles}, Kara: {score_init.penalty:.2f}, Dystans: {score_init.distance:.2f}\n")
    plot_solution(nodes, sol_init, title="Rozwiązanie Początkowe")

    ga = GeneticAlgorithm(nodes, dist, capacity, max_vehicles, pop_size=100)
    ga.create_initial_population(sol_init)
    sol_opt = ga.run(generations=2000) 

    import matplotlib.pyplot as plt
    plot_solution(nodes, sol_opt, title="Rozwiązanie Po Optymalizacji")
    history = ga.history
    if not history:
        print("BŁĄD: Lista history jest pusta!")
    else:
        gens = [h['gen'] for h in history]
        best_penalties = [h['best_penalty'] for h in history]
        avg_penalties = [h['avg_penalty'] for h in history]
        distances = [h['best_dist'] for h in history]

        # Wykres 1: Kara
        plt.figure(figsize=(10, 5))
        plt.plot(gens, best_penalties, label='Najlepsza Kara', color='red')
        plt.plot(gens, avg_penalties, label='Średnia Kara', alpha=0.3, color='orange')
        plt.title("Analiza poprawy wykonalności (Penalty)")
        plt.xlabel("Generacja")
        plt.ylabel("Wartość kary")
        plt.legend()
        plt.grid(True)
        plt.savefig("analiza_penalty.png")
        print("Zapisano: analiza_penalty.png")
        plt.show() # Zobaczysz wykres na ekranie
        plt.close() # Czyści pamięć

        # Wykres 2: Dystans
        plt.figure(figsize=(10, 5))
        plt.plot(gens, distances, color='green', linewidth=2)
        plt.title("Zmiana całkowitego dystansu w czasie")
        plt.xlabel("Generacja")
        plt.ylabel("Dystans")
        plt.grid(True)
        plt.savefig("analiza_dystansu.png")
        print("Zapisano: analiza_dystansu.png")
        plt.show()
        plt.close()