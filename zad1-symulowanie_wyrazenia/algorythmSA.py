import random
import math
from functions import funkcja_przykład3, funkcja_przykład4

class SimulatedAnnealing:
    def __init__(self, T0, A, M, k):
        self.T0 = T0 # temperatura początkowa
        self.A = A # współczynnik/sposób chłodzenia
        self.M = M # liczba iteracji
        self.k = k # współczynnik k, stała Boltzmanna
        self.licznik_korekcji = 0


    def solve(self, objective_function, x_min, x_max):
            """
            x_min: Dolna granica dziedziny
            x_max: Górna granica dziedziny
            """
            
            T = self.T0
            # zaczęcie od losowego punktu startowego 
            x_current = random.uniform(x_min, x_max)
            f_current = objective_function(x_current)
            # najlepsze rozwiązanie globalne do tej pory
            x_best = x_current
            f_best = f_current
            
            # Warunek stopu - np. minimalna temperatura
            T_min = 0.0001 

            while T > T_min:
                
                # (Iteracje w stałej T)
                for _ in range(self.M):
                    
                    # Generowanie sąsiada (nowego punktu) - strategia perturbacji,
                    # wygerowanie losowego kroku w obrębie dziedziny
                    # krok zależy od aktualnej temperatury
                    step_size = (x_max - x_min) * (T / self.T0) * 0.1 
                    x_new = x_current + random.uniform(-step_size, step_size)
                    # sprawdzenie czy krok nie wychodzi poza dziedzinę                    
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
                    else:
                        # Jeśli nowy punkt jest gorszy, akceptujemy go z pewnym prawdopodobieństwem                         
                        # prawdopodobieństwo akceptacji gorszego rozwiązania
                        if self.k * T <= 0:
                            prob = 0
                        else:
                            prob = math.exp(delta_f / (self.k * T))
                        # żeby uciec z lokalnego maksimum                        
                        if random.random() < prob:
                            x_current = x_new
                            f_current = f_new
                            
                # Po wykonaniu M iteracji w stałej temperaturze, schładzamy system
                T = T * self.A  
                
            return x_best, f_best
    

if __name__ == "__main__":
    # Parametry algorytmu
    T0 = 1000    # początkowa temperatura
    A = 0.9      # współczynnik chłodzenia
    M = 1000      # liczba iteracji na poziomie temperatury
    k = 1        # stała Boltzmanna

    sa = SimulatedAnnealing(T0, A, M, k)

    # Definicja dziedziny problemu
    x_min = -1
    x_max = 2

    # Uruchomienie algorytmu dla przykładowej funkcji
    best_x, best_f = sa.solve(funkcja_przykład4, x_min, x_max)
    print(f"Liczba zaakceptowanych korekcji rozwiązań: {sa.licznik_korekcji}")
    print(f"Najlepsze znalezione rozwiązanie: x = {best_x}, f(x) = {best_f}")