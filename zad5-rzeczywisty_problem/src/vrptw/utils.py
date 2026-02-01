import matplotlib.pyplot as plt
from pathlib import Path

def plot_solution(nodes, solution, title="Trasy VRPTW"):
    plt.figure(figsize=(10, 8))
    
    for i, c in enumerate(nodes):
        if i == 0:  # Depo
            plt.scatter(c.x, c.y, c='red', marker='s', s=100, label='Depot')
        else:
            plt.scatter(c.x, c.y, c='blue', s=20, alpha=0.6)
    depot = nodes[0]
    colors = plt.cm.get_cmap('tab20', len(solution.routes)) # Różne kolory dla tras

    for idx, route in enumerate(solution.routes):
        route_nodes = [depot] + [nodes[cid] for cid in route.stops] + [depot]
        xs = [n.x for n in route_nodes]
        ys = [n.y for n in route_nodes]
        
        plt.plot(xs, ys, color=colors(idx), linewidth=1.5, alpha=0.8)

    plt.title(title)
    plt.xlabel("Współrzędna X")
    plt.ylabel("Współrzędna Y")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='upper right')
    plt.show()

def plot_training_history(history, plots_dir: Path, instance_name: str):
    """generuje i zapisuje wykresy kary oraz dystansu na podstawie historii GA."""
    if not history:
        print("BŁĄD: Historia jest pusta, nie można wygenerować wykresów.")
        return

    plots_dir.mkdir(exist_ok=True)

    gens = [h['gen'] for h in history]
    best_penalties = [h['best_penalty'] for h in history]
    avg_penalties = [h['avg_penalty'] for h in history]
    distances = [h['best_dist'] for h in history]

    # wykres 1: kara (wykonalność)
    plt.figure(figsize=(10, 5))
    plt.plot(gens, best_penalties, label='Najlepsza Kara', color='red')
    plt.plot(gens, avg_penalties, label='Średnia Kara', alpha=0.3, color='orange')
    plt.title(f"Analiza poprawy wykonalności - {instance_name}")
    plt.xlabel("Generacja")
    plt.ylabel("Wartość kary")
    plt.legend()
    plt.grid(True)

    path_penalty = plots_dir / f"{instance_name}_analiza_penalty.png"
    plt.savefig(path_penalty)
    print(f"Zapisano: {path_penalty}")
    plt.show()
    plt.close()

    # wykres 2: dystans
    plt.figure(figsize=(10, 5))
    plt.plot(gens, distances, color='green', linewidth=2)
    plt.title(f"Zmiana całkowitego dystansu - {instance_name}")
    plt.xlabel("Generacja")
    plt.ylabel("Dystans")
    plt.grid(True)

    path_distance = plots_dir / f"{instance_name}_anazlia_distance.png"
    plt.savefig(path_distance)
    print(f"Zapisano: {path_distance}")
    plt.show()
    plt.close()

    print(f"Wykresy zostały zapisane w folderze: {plots_dir}")