from pathlib import Path

from vrptw.parser import load_solomon
from vrptw.distance import build_distance_matrix
from vrptw.evaluation import evaluate_solution
from vrptw.construction import build_initial_solution_ready_time
from vrptw.utils import plot_solution, plot_training_history
from vrptw.genetic_algorithm import GeneticAlgorithm

if __name__ == "__main__":
    # konfiguracja ścieżek
    base = Path(__file__).resolve().parents[1]
    data_dir = base / "data" / "solomon_100"
    plots_dir = base / "plots"

    # załadowanie instancji
    instance_file = "r101.txt"
    instance_name, max_vehicles, vehicle_capacity, depot, customers = load_solomon(data_dir / instance_file)

    nodes = [depot] + customers
    dist_matrix = build_distance_matrix(nodes)

    # rozwiązanie początkowe
    sol_init = build_initial_solution_ready_time(nodes, dist_matrix, vehicle_capacity, max_vehicles)
    score_init = evaluate_solution(nodes, dist_matrix, vehicle_capacity, max_vehicles, sol_init)

    print(f"\n--- INSTANCJA: {instance_name} ---")
    print(f"Początkowe - Pojazdy: {score_init.vehicles}, Kara: {score_init.penalty:.2f}, Dystans: {score_init.distance:.2f}\n")
    plot_solution(nodes, sol_init, title=f"Rozwiązanie Początkowe ({instance_name})")

    # optymalizacja GA
    ga = GeneticAlgorithm(nodes, dist_matrix, vehicle_capacity, max_vehicles, pop_size=100)
    ga.create_initial_population(sol_init)
    sol_opt = ga.run(generations=2000) 

    plot_solution(nodes, sol_opt, title="Rozwiązanie Po Optymalizacji")

    plot_training_history(ga.history, plots_dir, instance_name)
