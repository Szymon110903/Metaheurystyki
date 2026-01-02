
import math
import random
import time

class AntColony:
    def __init__(self, num_ants, num_iterations, Q, A, B, rho, data):
        self.num_ants = num_ants
        self.p_random = 0.0 # prawdopodobienstwo wyboru losowej atrakcji. do przetestowania kilka poziomow {0.0, 0.01, 0.05, 0.1}
        self.num_iterations = num_iterations
        self.Q = Q        #stała ilośc feromonu pozostawiana przez mrówkę
        self.A = A        #waga śladu feromonu
        self.B = B        #waga informacji heurystycznej
        self.rho = rho    #współczynnik parowania feromonu
        self.data = data  #dane wejściowe

        self.coordinates = [(item[1], item[2]) for item in data]
        self.num_attractions = len(self.coordinates)
        "inicjalizacja macierzy "
        self.pheromone_matrix = [[0.0 for _ in range(self.num_attractions)] for _ in range(self.num_attractions)]
        self.distance_matrix = self._init_distance_matrix(self.coordinates)
        self.heuristic_matrix = self._init_heuristic_matrix(self.distance_matrix)


    """ Macierz długości między atrakcjami """
    # Tworzona jest najpierw kwadratowa siatka o wielkości indeks X indeks atrakcji
    # Uzupełniania jest potem odległościami euklidesowymi między atrakcjami
    # Macierz obrazuje odległości między każdą parą atrakcji gdzie wiersze i kolumny odpowiadają indeksom atrakcji 
    def _init_distance_matrix(self, coordinates):
        matrix = [[0.0 for _ in range(len(coordinates))] for _ in range(len(coordinates))]
        for i in range(len(coordinates)):
            for j in range(len(coordinates)):
                    matrix[i][j] = self.euclidean_distance(coordinates[i], coordinates[j])
                    matrix[j][i] = matrix[i][j]
        return matrix

    def euclidean_distance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

    """ Macierz informacji heurystycznej """
    # Informacja heurystyczna jest odwrotnością odległości między atrakcjami 1/distance
    # Im mniejsza odległość między atrakcjami, tym większa wartość informacji heurystycznej
    # Macierz jest kwadratowa o wielkości indeks X indeks atrakcji
    # pokazuje atrakcyjność przejścia między każdą parą atrakcji
    # potrzebna do podejmowania decyzji przez mrówki podczas wyboru trasy

    def _init_heuristic_matrix(self, distance_matrix):
        heuristic = [[0.0 for _ in range(len(distance_matrix))] for _ in range(len(distance_matrix))]
        for i in range(len(distance_matrix)):
            for j in range(len(distance_matrix)):
                if distance_matrix[i][j] != 0:
                    heuristic[i][j] = 1 / (distance_matrix[i][j] + 1e-10)  # dodanie epsilona unika dzielenia przez zero
        return heuristic
    
    """ Wybór następnej atrakcji przez mrówkę """
    # Wybór opiera się na prawdopodobieństwie zależnym od ilości feromonu i informacji heurystycznej
    # w liczniku znajduje się iloczyn feromonu i informacji heurystycznej podniesionych do odpowiednich wag A i B
    # w mianowniku suma tych wartości dla wszystkich nieodwiedzonych atrakcji
    
    def select_next_attraction(self, current_attraction, visited):
        unvisited = [j for j in range(self.num_attractions) if j not in visited]
        if random.random() < self.p_random:
            return random.choice(unvisited)

        probabilities = [] 
        total = 0.0        # suma prawdopodobieństw - mianownik
        for attraction in range(self.num_attractions):
            if attraction not in visited:
                prob = (self.pheromone_matrix[current_attraction][attraction] ** self.A) * (self.heuristic_matrix[current_attraction][attraction] ** self.B)
                probabilities.append((attraction, prob))
                total += prob

        # obsługa przypadku gdy suma prawdopodobieństw wynosi 0
        if total == 0:
            return random.choice([j for j in range(self.num_attractions) if j not in visited])

        # Wyliczenie prawdopodobieństw wyboru każdej z nieodwiedzonych atrakcji
        # na zasadzie koła ruletki
        # każda atrakcja kandydująca ma przypisany przedział na kole ruletki proporcjonalny do swojego prawdopodobieństwa
        candidates, weights = zip(*[ (j, prob) for j, prob in probabilities if prob > 0])
        selected = random.choices(candidates, weights=weights, k=1)[0]
        return selected

    """ Parowanie feromonu """
    def evaporate_pheromone(self):
        for i in range(self.num_attractions):
            for j in range(self.num_attractions):
                if i != j:
                    self.pheromone_matrix[i][j] *= (1.0 - self.rho)

    """ Aktualizacja feromonu """
    def update_pheromone(self, all_paths, all_distances):
        for path, length in zip(all_paths, all_distances):
            if length <= 0:
                continue
            deposit = self.Q / length
            for k in range(len(path) - 1):
                i, j = path[k], path[k + 1]
                self.pheromone_matrix[i][j] += deposit
                self.pheromone_matrix[j][i] += deposit

    def run(self):
        # print(self.distance_matrix(self.coordinates))
        # print(self.heuristic_matrix(self.distance_matrix(self.coordinates)))
        for coordx, coordy in self.coordinates:
            print(coordx, coordy)
        for iter in range(self.num_iterations):
            all_paths = []
            all_distances = []
            for ant in range(self.num_ants):
                visited = []
                distance_traveled = 0
                # pierwsza pozycja mrówki to pierwsza atrakcja
                current_attraction = 0
                visited.append(current_attraction)
                while len(visited) < self.num_attractions:
                    next_attraction = self.select_next_attraction(current_attraction, visited)
                    visited.append(next_attraction)
                    distance_traveled += self.distance_matrix[current_attraction][next_attraction]
                    current_attraction = next_attraction
                # zapisanie trasy i odległości przejścia przez mrówkę do listy wszystkich tras i odległości
                # żeby potem zaktualizować feromon
                all_paths.append(visited) 
                all_distances.append(distance_traveled)

            # aktualizacja feromonu po przejściu wszystkich mrówek - raz na iteracje
            self.evaporate_pheromone()
            self.update_pheromone(all_paths, all_distances)