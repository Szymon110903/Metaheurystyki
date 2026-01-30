from pathlib import Path
from vrptw.parser import load_solomon
from vrptw.distance import build_distance_matrix
from vrptw.models import *
from vrptw.evaluation import evaluate_solution

if __name__ == "__main__":
    base = Path(__file__).resolve().parents[1]
    data_dir = base / "data" / "solomon_100"
    # odczytanie danych za pomoca parsera z pliku
    name, max_vehicles, capacity, depot, customers = load_solomon(data_dir / "r101.txt")
    # print(name, max_vehicles, capacity, depot, customers)

    #stworzenie Instance
    nodes = [depot] + customers
    dist = build_distance_matrix(nodes)

    routes = []
    cid = 1
    while cid <= 100:
        routes.append(Route([cid, cid + 1, cid + 2, cid + 3]))
        cid += 4

    sol = Solution(routes=routes)
    score = evaluate_solution(nodes, dist, capacity, max_vehicles, sol)
    print("Score test:", score)