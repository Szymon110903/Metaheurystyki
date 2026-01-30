from pathlib import Path
from vrptw.parser import load_solomon
from vrptw.distance import build_distance_matrix
from vrptw.models import *
from vrptw.evaluation import evaluate_solution
from vrptw.construction import can_append_feasible, build_initial_solution_ready_time

if __name__ == "__main__":
    base = Path(__file__).resolve().parents[1]
    data_dir = base / "data" / "solomon_100"
    # odczytanie danych za pomoca parsera z pliku
    name, max_vehicles, capacity, depot, customers = load_solomon(data_dir / "r101.txt")
    # print(name, max_vehicles, capacity, depot, customers)

    nodes = [depot] + customers
    dist = build_distance_matrix(nodes)

    sol = build_initial_solution_ready_time(nodes, dist, capacity, max_vehicles)
    score = evaluate_solution(nodes, dist, capacity, max_vehicles, sol)

    print("Initial solution (ready_time heuristic):", score)
    print("Routes:", len(sol.routes))
    print("First route length:", len(sol.routes[0].stops))