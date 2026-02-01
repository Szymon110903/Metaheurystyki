import random
import copy
from typing import List, Dict, Any
from .models import Solution, Route
from .evaluation import evaluate_solution, simulate_route

class GeneticAlgorithm:
    def __init__(self, nodes, dist_matrix, capacity, max_vehicles, pop_size=100, mutation_rate=0.1):
        self.nodes = nodes
        self.dist_matrix = dist_matrix
        self.capacity = capacity
        self.max_vehicles = max_vehicles
        self.pop_size = pop_size
        self.population: List[Solution] = []
        self.mutation_rate = mutation_rate 
        # Rozbudowana historia do analizy w sprawozdaniu
        self.history: List[Dict[str, Any]] = []

    def create_initial_population(self, base_solution: Solution):
        """Inicjalizacja populacji rozwiązaniem startowym i jego wariacjami."""
        self.population = [base_solution]
        for _ in range(self.pop_size - 1):
            # Tworzymy kopie z silną mutacją na start, aby przeszukać przestrzeń
            mutated = self.mutate(copy.deepcopy(base_solution))
            self.population.append(mutated)

    def _get_best_insertion_pos(self, route: Route, customer_id: int):
        """Szuka pozycji w trasie, która generuje najmniejszą karę i dystans."""
        best_pos = 0
        best_score = (float('inf'), float('inf'), float('inf')) # (kara, przeładowanie, dystans)
        
        for i in range(len(route.stops) + 1):
            test_stops = route.stops[:i] + [customer_id] + route.stops[i:]
            stats = simulate_route(self.nodes, self.dist_matrix, test_stops)
            current_score = (stats.late_time, stats.load > self.capacity, stats.distance)
            
            if current_score < best_score:
                best_score = current_score
                best_pos = i
        return best_pos

    def _relocate_mutation(self, solution: Solution):
        """Przenosi klienta do trasy, w której najlepiej 'pasuje' czasowo."""
        if len(solution.routes) < 2: return solution
        
        source_idx = random.randrange(len(solution.routes))
        if not solution.routes[source_idx].stops: return solution
        
        cid = solution.routes[source_idx].stops.pop(random.randrange(len(solution.routes[source_idx].stops)))
        
        target_idx = random.choice([i for i in range(len(solution.routes)) if i != source_idx])
        target_route = solution.routes[target_idx]
        
        pos = self._get_best_insertion_pos(target_route, cid)
        target_route.stops.insert(pos, cid)
        return solution

    def _2opt_mutation(self, solution: Solution):
        """Lokalna optymalizacja dystansu wewnątrz jednej trasy."""
        if not solution.routes: return solution
        route = random.choice(solution.routes)
        if len(route.stops) < 4: return solution
        
        i, j = sorted(random.sample(range(len(route.stops)), 2))
        route.stops[i:j] = reversed(route.stops[i:j])
        return solution

    def mutate(self, solution: Solution) -> Solution:
        """Wybór operatora mutacji."""
        op = random.random()
        if op < 0.5:
            return self._relocate_mutation(solution)
        else:
            return self._2opt_mutation(solution)

    def run(self, generations=1000):
        best_overall = None
        best_overall_key = (True, float('inf'), float('inf'), float('inf'))
        
        print(f"{'Gen':<5} | {'Veh':<4} | {'Best Pen':<10} | {'Best Dist':<10} | {'Avg Pen':<10}")
        print("-" * 65)

        for gen in range(generations):
            evaluated_pop = []
            for s in self.population:
                s.routes = [r for r in s.routes if r.stops]
                
                sc = evaluate_solution(self.nodes, self.dist_matrix, self.capacity, self.max_vehicles, s)
                sort_key = (sc.penalty > 0,sc.vehicles, sc.penalty, sc.distance)
                evaluated_pop.append((sort_key, sc, s))
            
            evaluated_pop.sort(key=lambda x: x[0])
            
            best_sc = evaluated_pop[0][1]
            best_sol = evaluated_pop[0][2]
            current_key = evaluated_pop[0][0]
            avg_pen = sum(x[1].penalty for x in evaluated_pop) / len(evaluated_pop)
            
            if best_overall is None or current_key < best_overall_key:
                best_overall = copy.deepcopy(best_sol)
                best_overall_key = current_key

            self.history.append({
                'gen': gen,
                'best_dist': best_sc.distance,
                'best_penalty': best_sc.penalty,
                'avg_penalty': avg_pen,
                'vehicles': best_sc.vehicles
            })

            if gen % 100 == 0 or gen == generations - 1:
                print(f"{gen:<5} | {best_sc.vehicles:<4} | {best_sc.penalty:<10.2f} | {best_sc.distance:<10.2f} | {avg_pen:<10.2f}")

            next_gen = [x[2] for x in evaluated_pop[:int(self.pop_size * 0.2)]]
            
            while len(next_gen) < self.pop_size:
                parent = random.choice(next_gen[:10])
                child = copy.deepcopy(parent)

                if random.random() < self.mutation_rate:
                    child = self.mutate(child)
                child = self.mutate(copy.deepcopy(parent))
                
                child.routes = [r for r in child.routes if r.stops]
                next_gen.append(child)

            self.population = next_gen

        return best_overall