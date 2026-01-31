import matplotlib.pyplot as plt

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