import numpy as np
import random
import matplotlib.pyplot as plt
import time

class Ant:
    def __init__(self, start_node, num_nodes):
        self.visited = [start_node]
        self.current_node = start_node
        self.total_distance = 0.0
        self.num_nodes = num_nodes

    def move(self, distance_matrix, pheromone_matrix, alpha, beta, p_random):
        # Nieodwiedzone miasta
        unvisited = [node for node in range(self.num_nodes) if node not in self.visited]
        
        if not unvisited:
            return

        if random.random() < p_random:
            next_node = random.choice(unvisited) # ruch losowy
        else:
            # Wyliczanie prawdopodobieństw
            probabilities = []
            denominator = 0.0
            
            # liczniki dla każdego nieodzwiedzonego miasta
            numerators = []
            for node in unvisited:
                dist = distance_matrix[self.current_node][node]
                if dist == 0: dist = 0.0001
                
                heuristic = 1.0 / dist
                tau = pheromone_matrix[self.current_node][node]
                
                numerator = (tau ** alpha) * (heuristic ** beta)
                numerators.append(numerator)
                denominator += numerator

            # Obliczanie prawdopodobieństw
            if denominator == 0:
                probabilities = [1.0 / len(unvisited)] * len(unvisited)
            else:
                probabilities = [num / denominator for num in numerators]

            next_node = np.random.choice(unvisited, p=probabilities)

        dist_to_next = distance_matrix[self.current_node][next_node]
        self.total_distance += dist_to_next
        self.visited.append(next_node)
        self.current_node = next_node

    def return_to_start(self, distance_matrix):
        start_node = self.visited[0]
        dist = distance_matrix[self.current_node][start_node]
        self.total_distance += dist
        self.visited.append(start_node)

class AntColony:
    def __init__(self, num_ants, num_iterations, Q, A, B, rho, p_random, data):
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.Q = Q          # Stała feromonowa
        self.alpha = A      # Waga feromonu
        self.beta = B       # Waga heurystyki
        self.rho = rho      # Współczynnik parowania
        self.p_random = p_random # Prawdopodobieństwo ruchu losowego
        
        self.coords = np.array([(d[1], d[2]) for d in data])
        self.ids = [d[0] for d in data]
        self.num_nodes = len(data)

        # inicjalizacja macierzy odległości i feromonów
        self.distance_matrix = self._calculate_distance_matrix()
        self.pheromone_matrix = np.ones((self.num_nodes, self.num_nodes)) 

        self.best_route_history = []
        self.best_route = None
        self.best_distance = float('inf')

    # obliczanie macierzy odległości euklidesowych
    def _calculate_distance_matrix(self):
        matrix = np.zeros((self.num_nodes, self.num_nodes))
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                if i != j:
                    matrix[i][j] = np.linalg.norm(self.coords[i] - self.coords[j])
        return matrix


    def run(self, verbose=True):
        start_time = time.time()
        
        for iteration in range(self.num_iterations):
            ants = []
            
            for _ in range(self.num_ants):
                # Losowy punkt startowy dla każdej mrówki
                start_node = random.randint(0, self.num_nodes - 1)
                ant = Ant(start_node, self.num_nodes)
                
                # Przejście przez wszystkie miasta
                for _ in range(self.num_nodes - 1):
                    ant.move(self.distance_matrix, self.pheromone_matrix, 
                             self.alpha, self.beta, self.p_random)
                
                ant.return_to_start(self.distance_matrix)
                ants.append(ant)

            iteration_best_ant = min(ants, key=lambda x: x.total_distance)
            
            # Aktualizacja globalnie najlepszego wyniku
            if iteration_best_ant.total_distance < self.best_distance:
                self.best_distance = iteration_best_ant.total_distance
                self.best_route = list(iteration_best_ant.visited) 
            
            self.best_route_history.append(self.best_distance)

            self._update_pheromones(ants)

            if verbose and (iteration + 1) % 10 == 0:
                print(f"Iteracja {iteration + 1}/{self.num_iterations}: Najlepszy koszt = {self.best_distance:.2f}")

        execution_time = time.time() - start_time
        
        if verbose:
            print("\n--- KONIEC SYMULACJI ---")
            print(f"Najlepsza znaleziona trasa (długość): {self.best_distance:.2f}")
            print(f"Czas wykonania: {execution_time:.4f} s")
            self._plot_results()
        
        return self.best_distance, self.best_route, self.best_route_history, execution_time
    
    # Aktualizacja poziomów feromonów
    def _update_pheromones(self, ants):
        # f_ij = (1 - rho) * f_ij
        self.pheromone_matrix *= (1 - self.rho)

        for ant in ants:
            contribution = self.Q / ant.total_distance
            path = ant.visited
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                self.pheromone_matrix[u][v] += contribution
                self.pheromone_matrix[v][u] += contribution

    # generowanie wykresów
    def _plot_results(self):
        plt.figure(figsize=(12, 5))
        
        plt.subplot(1, 2, 1)
        plt.plot(self.best_route_history)
        plt.title("Postęp optymalizacji (Zbieżność)")
        plt.xlabel("Iteracja")
        plt.ylabel("Długość najlepszej trasy")
        plt.grid(True)

        plt.subplot(1, 2, 2)
        x_coords = self.coords[:, 0]
        y_coords = self.coords[:, 1]
        
        plt.scatter(x_coords, y_coords, c='red', zorder=2)
        for i, txt in enumerate(self.ids):
            plt.annotate(txt, (x_coords[i], y_coords[i]), xytext=(5, 5), textcoords='offset points')

        if self.best_route:
            route_x = [self.coords[node][0] for node in self.best_route]
            route_y = [self.coords[node][1] for node in self.best_route]
            plt.plot(route_x, route_y, c='blue', linestyle='-', linewidth=1, zorder=1)

        plt.title(f"Najlepsza trasa: {self.best_distance:.2f}")
        plt.grid(True)
        
        plt.tight_layout()
        plt.show()