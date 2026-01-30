from pathlib import Path
from vrptw.parser import load_solomon
from vrptw.distance import build_distance_matrix
from vrptw.models import *

def quick_print(file_path: Path) -> None:
    inst = load_solomon(file_path)
    dist = build_distance_matrix(inst.depot, inst.customers)

    print("=" * 60)
    print(f"Instance: {inst.name}")
    print(f"Capacity: {inst.capacity}")
    print(f"Depot: {inst.depot}")
    print(f"Customers count: {len(inst.customers)}")
    print("First 3 customers:", inst.customers[:3])
    print(f"dist(depot->1) = {dist[0][1]:.4f}")
    print(f"matrix size = {len(dist)} x {len(dist[0])}")

if __name__ == "__main__":
    base = Path(__file__).resolve().parents[1]
    data_dir = base / "data" / "solomon_100"
    # odczytanie danych za pomoca parsera z pliku
    name, max_vehicles, capacity, depot, customers = load_solomon(data_dir / "r101.txt")
    # print(name, max_vehicles, capacity, depot, customers)

    #stworzenie Instance
    nodes = [depot] + customers
    dist = build_distance_matrix(nodes)

    print("nodes size:", len(nodes))  # 101
    print("matrix size:", len(dist), len(dist[0]))  # 101 101
    print("depot id:", nodes[0].id)  # 0
    print("customer 1 id:", nodes[1].id)  # 1
    print("dist[0][1]:", dist[0][1])