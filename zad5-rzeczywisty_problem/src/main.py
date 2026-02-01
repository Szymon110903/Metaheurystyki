from pathlib import Path
import numpy as np

from vrptw.parser import load_solomon
from vrptw.distance import build_distance_matrix
from vrptw.evaluation import evaluate_solution
from vrptw.construction import build_initial_solution_ready_time
from vrptw.utils import plot_solution, plot_training_history
from vrptw.genetic_algorithm import GeneticAlgorithm

# ==========================================
# KONFIGURACJA EKSPERYMENTU
# ==========================================
config = {
    'instance_file': "r101.txt",  # nazwa pliku z folderu data/solomon_100/
    'num_runs': 5,                # Ile razy powtórzyć test (dla statystyki)
    'ga_params': {
        'pop_size': 100,
        'generations': 1000,
        # 'mutation_rate': 0.1,
    }
}

def run_single_test(nodes, dist_matrix, capacity, max_vehicles, sol_init, config_ga):
    '''Przeprowadza jeden pełny bieg algorytmu GA.'''
    ga = GeneticAlgorithm(
        nodes,
        dist_matrix,
        capacity,
        max_vehicles,
        pop_size=config_ga['pop_size']
    )
    ga.create_initial_population(sol_init)

    # uruchomienie algorytmu
    sol_opt = ga.run(generations=config_ga['generations'])

    # ewaluacja
    score_opt = evaluate_solution(nodes, dist_matrix, capacity, max_vehicles, sol_opt)

    return sol_opt, score_opt, ga.history

if __name__ == "__main__":
    # konfiguracja ścieżek
    base = Path(__file__).resolve().parents[1]
    data_path = base / "data" / "solomon_100" / config["instance_file"]
    plots_dir = base / "plots"

    # załadowanie instancji
    instance_name, max_vehicles, vehicle_capacity, depot, customers = load_solomon(data_path)
    nodes = [depot] + customers
    dist_matrix = build_distance_matrix(nodes)

    # rozwiązanie początkowe
    sol_init = build_initial_solution_ready_time(nodes, dist_matrix, vehicle_capacity, max_vehicles)
    score_init = evaluate_solution(nodes, dist_matrix, vehicle_capacity, max_vehicles, sol_init)

    print(f"\n" + '='*50)
    print(f"\n--- INSTANCJA: {instance_name} ---")
    print(f"Parametry GA: {config['ga_params']}")
    print(f"Początkowe - Pojazdy: {score_init.vehicles}, Kara: {score_init.penalty:.2f}, Dystans: {score_init.distance:.2f}\n")
    print("="*50)

    plot_solution(nodes, sol_init, title=f"Rozwiązanie Początkowe ({instance_name})")

    # pętla eksperymentów
    all_scores = []
    best_overall_sol = None
    best_overall_score = float('inf')
    all_histories = []

    for i in range(config['num_runs']):
        print(f"\n>>> Próba {i+1}/{config['num_runs']}...")

        sol_opt, score_opt, history = run_single_test(
            nodes, dist_matrix, vehicle_capacity, max_vehicles, sol_init, config['ga_params']
        )

        all_scores.append(score_opt)
        all_histories.append(history)

        print(f"    Wynik: Dystans = {score_opt.distance:.2f}, Kara = {score_opt.penalty:.2f}")

        # Zapamiętaj najlepsze rozwiązanie ze wszystkich prób
        if score_opt.distance < best_overall_score and score_opt.penalty == 0:
            best_overall_score = score_opt.distance
            best_overall_sol = sol_opt

    # Analiza statystyczna (na podstawie dystansu)
    distances = [s.distance for s in all_scores]
    print("\n" + "=" * 40)
    print(f"PODSUMOWANIE DLA {instance_name}")
    print("=" * 40)
    print(f"Najlepszy (Best):  {np.min(distances):.2f}")
    print(f"Najgorszy (Worst): {np.max(distances):.2f}")
    print(f"Średnia (Mean):    {np.mean(distances):.2f}")
    print(f"Odchylenie (Std):  {np.std(distances):.2f}")
    print("=" * 40)

    # Wizualizacja najlepszego wyniku i historii ostatniej próby
    if best_overall_sol:
        plot_solution(nodes, best_overall_sol, title=f"Najlepsza Trasa - {instance_name}")

    # Wykresy zbieżności dla ostatniej próby (możesz też przerobić funkcję, by rysowała średnią ze wszystkich)
    plot_training_history(all_histories[-1], plots_dir, instance_name)