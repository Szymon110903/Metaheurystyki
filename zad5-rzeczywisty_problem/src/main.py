from pathlib import Path
import numpy as np
import random # Dodane dla powtarzalności (opcjonalnie)

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
        'mutation_rate': 0.1,     
        'elitism_rate': 0.2       
    }
}

def run_single_test(nodes, dist_matrix, capacity, max_vehicles, sol_init, config_ga):
    '''Przeprowadza jeden pełny bieg algorytmu GA z nowymi parametrami.'''
    ga = GeneticAlgorithm(
        nodes,
        dist_matrix,
        capacity,
        max_vehicles,
        pop_size=config_ga['pop_size'],
        mutation_rate=config_ga['mutation_rate'], 
        elitism_rate=config_ga['elitism_rate']    
    )
    ga.create_initial_population(sol_init)

    # uruchomienie algorytmu
    sol_opt = ga.run(generations=config_ga['generations'])

    # ewaluacja końcowa
    score_opt = evaluate_solution(nodes, dist_matrix, capacity, max_vehicles, sol_opt)

    return sol_opt, score_opt, ga.history

if __name__ == "__main__":
    # Konfiguracja ścieżek
    base = Path(__file__).resolve().parents[1]
    data_path = base / "data" / "solomon_100" / config["instance_file"]
    plots_dir = base / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True) # Upewnij się, że folder na wykresy istnieje

    # Załadowanie instancji
    instance_name, max_vehicles, vehicle_capacity, depot, customers = load_solomon(data_path)
    nodes = [depot] + customers
    dist_matrix = build_distance_matrix(nodes)

    # Rozwiązanie początkowe
    sol_init = build_initial_solution_ready_time(nodes, dist_matrix, vehicle_capacity, max_vehicles)
    score_init = evaluate_solution(nodes, dist_matrix, vehicle_capacity, max_vehicles, sol_init)

    print(f"\n" + '='*60)
    print(f"--- EKSPERYMENT VRPTW: {instance_name} ---")
    print(f"Parametry: Pop={config['ga_params']['pop_size']}, Gen={config['ga_params']['generations']}, "
          f"Mut={config['ga_params']['mutation_rate']}, Elite={config['ga_params']['elitism_rate']}")
    print(f"Start: Pojazdy={score_init.vehicles}, Kara={score_init.penalty:.2f}, Dyst={score_init.distance:.2f}")
    print('='*60)

    # Wizualizacja pajęczyny początkowej
    plot_solution(nodes, sol_init, title=f"Rozwiązanie Początkowe ({instance_name})")

    # Pętla eksperymentów
    all_scores = []
    best_overall_sol = None
    best_overall_score_obj = None 
    all_histories = []

    for i in range(config['num_runs']):
        print(f"\n>>> Próba {i+1}/{config['num_runs']}...")

        sol_opt, score_opt, history = run_single_test(
            nodes, dist_matrix, vehicle_capacity, max_vehicles, sol_init, config['ga_params']
        )

        all_scores.append(score_opt)
        all_histories.append(history)

        print(f"    Bieg {i+1} Wynik: Dystans = {score_opt.distance:.2f}, Kara = {score_opt.penalty:.2f}, Pojazdy = {score_opt.vehicles}")

        # Hierarchiczne porównanie: Penalty > Vehicles > Distance
        if best_overall_score_obj is None or score_opt.key() < best_overall_score_obj.key():
            best_overall_score_obj = score_opt
            best_overall_sol = sol_opt

    # Analiza statystyczna (na podstawie dystansu dla rozwiązań najlepszych pod kątem hierarchicznym)
    distances = [s.distance for s in all_scores]
    print("\n" + "=" * 45)
    print(f"PODSUMOWANIE STATYSTYCZNE: {instance_name}")
    print("=" * 45)
    print(f"Najlepszy (Best Dyst):  {np.min(distances):.2f}")
    print(f"Najgorszy (Worst Dyst): {np.max(distances):.2f}")
    print(f"Średnia (Mean):         {np.mean(distances):.2f}")
    print(f"Odchylenie (Std):       {np.std(distances):.2f}")
    print(f"Finałowa liczba aut:    {best_overall_score_obj.vehicles}")
    print("=" * 45)

    # Wizualizacja najlepszego wyniku i historii ostatniej próby
    if best_overall_sol:
        plot_solution(nodes, best_overall_sol, title=f"Najlepsza Trasa GA ({instance_name})")

    # Wykresy zbieżności
    plot_training_history(all_histories[-1], plots_dir, instance_name)