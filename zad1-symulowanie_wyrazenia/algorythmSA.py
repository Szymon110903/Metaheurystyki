import random
import math
import time


class SimulatedAnnealing:
    def __init__(self, T0, A, M, k):
        self.T0 = T0 # temperatura początkowa
        self.A = A # współczynnik/sposób chłodzenia
        self.M = M # liczba iteracji
        self.k = k # współczynnik k, stała Boltzmanna
        self.licznik_korekcji = 0
        self.start_time = None
        self.execution_time = 0
        self.best_solutions_history = [] 
        self.best_solution_iteration = 0
        self.total_iterations = 0  # Track total number of iterations

    def solve(self, objective_function, x_min, x_max):
        """
        x_min: Dolna granica dziedziny
        x_max: Górna granica dziedziny
        """
        self.start_time = time.time()
        T = self.T0
        # zaczęcie od losowego punktu startowego 
        x_current = random.uniform(x_min, x_max)
        f_current = objective_function(x_current)
        # najlepsze rozwiązanie globalne do tej pory
        x_best = x_current
        f_best = f_current
        
        global_iteration_count = 0
        self.best_solution_iteration = 0
        self.best_solutions_history.append((self.licznik_korekcji, x_best, f_best)) 
        
        # Warunek stopu - np. minimalna temperatura
        T_min = 0.0001 

        while T > T_min:
            
            # (Iteracje w stałej T)
            for _ in range(self.M):
                
                # --- Inkrementacja globalnej iteracji ---
                global_iteration_count += 1
                
                # Generowanie sąsiada (nowego punktu)
                step_size = (x_max - x_min) * (T / self.T0) * 0.1 
                x_new = x_current + random.uniform(-step_size, step_size)
                x_new = max(min(x_new, x_max), x_min)
                
                f_new = objective_function(x_new)
                
                # Różnica wartości funkcji celu
                delta_f = f_new - f_current

                # decyzja o akceptacji nowego punktu                   
                if delta_f > 0:
                    # Jeśli nowy punkt jest wyższy to go akceptujemy
                    x_current = x_new
                    f_current = f_new
                    # Aktualizacja najlepszego rozwiązania globalnego                 
                    if f_new > f_best:
                        x_best = x_new
                        f_best = f_new
                        self.licznik_korekcji += 1
                        # --- Zapisywanie numeru iteracji ---
                        self.best_solution_iteration = global_iteration_count
                        self.best_solutions_history.append((self.licznik_korekcji, x_best, f_best))
                else:
                    # Jeśli nowy punkt jest gorszy, akceptujemy go z pewnym prawdopodobieństwem               
                    if self.k * T <= 0:
                        prob = 0
                    else:
                        prob = math.exp(delta_f / (self.k * T))
                    if random.random() < prob:
                        x_current = x_new
                        f_current = f_new
                        
            # Po wykonaniu M iteracji w stałej temperaturze, schładzamy system
            T = T * self.A  
        self.execution_time = time.time() - self.start_time
        self.total_iterations = global_iteration_count 
        return x_best, f_best
    

