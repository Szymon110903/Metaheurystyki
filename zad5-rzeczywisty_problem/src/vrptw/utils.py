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

def plot_training_history(history, plots_dir: Path, instance_name: str, test_param: str = ""):
    """
    Generuje wykresy z informacją o testowanym parametrze.
    test_param: np. "Pop_50", "Elite_0.2" itp.
    """
    if not history:
        print("BŁĄD: Historia jest pusta.")
        return

    plots_dir.mkdir(exist_ok=True)
    suffix = f"_{test_param}" if test_param else ""

    gens = [h['gen'] for h in history]
    best_penalties = [h['best_penalty'] for h in history]
    avg_penalties = [h['avg_penalty'] for h in history]
    distances = [h['best_dist'] for h in history]

    # Wykres 1: Kara
    plt.figure(figsize=(10, 5))
    plt.plot(gens, best_penalties, label='Najlepsza Kara', color='red')
    plt.plot(gens, avg_penalties, label='Średnia Kara', alpha=0.3, color='orange')
    plt.title(f"Analiza wykonalności - {instance_name} ({test_param})")
    plt.xlabel("Generacja")
    plt.ylabel("Wartość kary")
    plt.legend()
    plt.grid(True)

    path_penalty = plots_dir / f"{instance_name}{suffix}_penalty.png"
    plt.savefig(path_penalty)
    plt.show()
    plt.close()

    # Wykres 2: Dystans
    plt.figure(figsize=(10, 5))
    plt.plot(gens, distances, color='green', linewidth=2)
    plt.title(f"Zmiana całkowitego dystansu - {instance_name} ({test_param})")
    plt.xlabel("Generacja")
    plt.ylabel("Dystans")
    plt.grid(True)

    path_distance = plots_dir / f"{instance_name}{suffix}_distance.png"
    plt.savefig(path_distance)
    plt.show()
    plt.close()