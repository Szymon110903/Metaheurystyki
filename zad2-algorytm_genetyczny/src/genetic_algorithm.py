import random
import time
from typing import Literal


# reprezentacja osobnika: [1, 0, 0, 1, 1, 0, ...] - 26 genów 1-bierzemy przedmiot 0-nie bierzemy
# osobnik - chromosom
# chromosome = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

class GeneticAlgorithm:
    SELECTION_METHODS = ("roulette", "tournament", "ranking")
    CROSSOVER_METHODS = ("one_point", "two_point", "uniform")
    MUTATION_METHODS = ("bit_flip", )

    def __init__(
        self,
        weights,
        values,
        capacity: int,
        population_size: int = 100,
        generations: int = 500,
        crossover_prob: float = 0.8,
        mutation_prob: float = 0.05,
        selection_method: Literal['roulette', 'tournament', 'ranking'] = 'roulette',
        crossover_method: Literal['one_point', 'two_point', 'uniform'] = 'one_point',
        mutation_method: Literal['bit_flip'] = 'bit_flip'
    ):
        if not isinstance(weights, list):
            raise TypeError(f"weights must be a list, got {type(weights)}")

        if not isinstance(values, list):
            raise TypeError(f"values must be a list, got {type(values)}")

        if not isinstance(capacity, int):
            raise TypeError(f"capacity must be an integer, got {type(capacity)}")

        if not isinstance(population_size, int):
            raise TypeError(f"population_size must be an integer, got {type(population_size)}")

        if not isinstance(generations, int):
            raise TypeError(f"generations must be an integer, got {type(generations)}")

        if not (0 <= crossover_prob <= 1):
            raise ValueError(f"crossover_prob must be in range [0,1], got {crossover_prob}")

        if not (0 <= mutation_prob <= 1):
            raise ValueError(f"mutation_prob must be in range [0,1], got {mutation_prob}")

        if selection_method not in self.SELECTION_METHODS:
            raise ValueError(f"selection_method must be one of {self.SELECTION_METHODS}")

        if crossover_method not in self.CROSSOVER_METHODS:
            raise ValueError(f"crossover_method must be one of {self.CROSSOVER_METHODS}")

        if mutation_method not in self.MUTATION_METHODS:
            raise ValueError(f"mutation_method must be one of {self.MUTATION_METHODS}")

        # dane problemu
        self.weights = weights # wagi przedmiotow [w1, w2, w3, ...] (kg)
        self.values = values # ceny przedmiotow [c1, c2, c3, ...] (zl)
        self.capacity = capacity # udzwig plecaka = 6 404 180 kg



        # parametry GA
        self.N = population_size
        self.T = generations
        self.Pc = crossover_prob
        self.Pm = mutation_prob
        self.selection_method = selection_method
        self.crossover_method = crossover_method
        self.mutation_method = mutation_method
        self.elitism_rate = 0.05 # elita o wielkosci 5% populacji jest zawsze przenoszona do nastepnej iteracji

        #populacja
        self.population = []
        self.fitness = []
        self.chromosome_size = len(weights)

        # zmienne do zapisu statystyk
        self.start_time = None
        self.execution_time = 0
        self.best_solutions_history = []
        self.worst_solutions_history = []
        self.avg_solutions_history = []
        self.best_index = 0
        self.worst_index = 0
        self.best_solution_iteration = 0

    '''metoda tworzaca poczatkowa populacje'''
    def initialize(self):
        self.population = []
        # od 0 do population_size-1
        for _ in range(self.N):
            subject = []

            for gene in range(self.chromosome_size): # od 0 do 25
                subject.append(random.randint(0, 1))

            self.population.append(subject)

    '''metoda wyliczajca fitnes dla podanego osobnika (chromosomu)'''
    def fitness_function(self, subject):
        total_weight = 0
        total_value = 0

        for i, gene in enumerate(subject):
            if gene == 1:
                total_weight += self.weights[i]
                total_value += self.values[i]

        if total_weight > self.capacity:
            return 0
        else:
            return total_value # co powinna zwracac ta funkcja wage czy wartosc plecaka? w prezentacji jest ze wage

    '''wylicza fitnes dla wszystkich osobników w populacji'''
    def evaluate(self):
        self.fitness = []

        for subject in self.population:
            calc_fitness = self.fitness_function(subject)
            self.fitness.append(calc_fitness)

        best_fitness = max(self.fitness)
        worst_fitness = min(self.fitness)
        avg_fitness = sum(self.fitness) / len(self.fitness)

        self.best_solutions_history.append(best_fitness)
        self.worst_solutions_history.append(worst_fitness)
        self.avg_solutions_history.append(avg_fitness)

        self.best_index = self.fitness.index(best_fitness) # to dziala na zasadzie znajdowania indeksu z taka sama wartoscia jak podana. co jesli jest kilka indeksow z taka wartoscia
        self.worst_index = self.fitness.index(worst_fitness)


    def _selection_roulette(self):
        total_fitness = sum(self.fitness)
        pick = random.uniform(0, total_fitness)

        if total_fitness == 0:
            return random.randint(0, self.N - 1)

        for i, fitness_value in enumerate(self.fitness):
            pick -= fitness_value
            if pick <= 0:
                return i

        return self.N - 1 # na wypadek gdyby pick teoretycznie byl <= 0 ale z uwagi dokladnosc float python by tak tego nie odczytal

    def _selection_tournament(self):
        k = 3 # zastanowic sie czy zeby zostawic to na sztywno czy zeby uzytkownik to podawal
        drawn_indices = random.sample(range(self.N), k) # lista wylosowanych indeksow osobnikow z calej populacji

        best = drawn_indices[0]
        for idx in drawn_indices:
            if self.fitness[best] < self.fitness[idx]:
                best = idx

        return best

    def _selection_ranking(self):
        ranks = [0] * self.N

        pairs = [(self.fitness[i], i) for i in range(self.N)]
        # sortujemy po fitness
        pairs.sort(key=lambda x: x[0]) # posortowane rosnaco wiec od najgorszych do najlepszych
        ranking = [index for (fitness_value, index) in pairs]

        for rank_position, subjects_index in enumerate(ranking):
            ranks[subjects_index] = rank_position + 1

        sum_ranks = sum(ranks)
        pick = random.uniform(0, sum_ranks)
        for i, r in enumerate(ranks):
            pick -= r
            if pick <= 0:
                return i

        return self.N - 1

    '''
    glowna metoda selekcji ktora wywoluje konkretne metody selekcji w zaleznosci od tego jaki parametr zostal 
    podany w konstruktorze
    '''
    def selection(self):
        if self.selection_method == 'roulette':
            return self._selection_roulette()
        elif self.selection_method == 'tournament':
            return self._selection_tournament()
        elif self.selection_method == 'ranking':
            return self._selection_ranking()


    def _crossover_one_point(self, parent1, parent2):
        crossing_point = random.randint(1, self.chromosome_size - 1)

        child1 = parent1[:crossing_point] + parent2[crossing_point:]
        child2 = parent2[:crossing_point] + parent1[crossing_point:]

        return child1, child2

    def _crossover_two_point(self, parent1, parent2):
        # range(1,x) daje liczby od 1 do x-1, a my chcemy miec jako ten punkt przeciecia poza indeksami 0 i ostatnim dlatego chromosome_size - 1
        points = random.sample(range(1, self.chromosome_size - 1), 2) # sample zapewnia ze bedziemy miec dwie rozne liczby
        points = sorted(points) # sortujemy zeby zawsze A < B, inaczej ponizsze laczenia czesci list bylyby bledne
        point_a = points[0]
        point_b = points[1]

        child1 = parent1[:point_a] + parent2[point_a:point_b] + parent1[point_b:]
        child2 = parent2[:point_a] + parent1[point_a:point_b] + parent2[point_b:]

        return child1, child2

    def _crossover_uniform(self, parent1, parent2):
        child1 = []
        child2 = []

        for idx in range(0, self.chromosome_size):
            if random.random() < 0.5:
                child1.append(parent1[idx])
                child2.append(parent2[idx])
            else:
                child1.append(parent2[idx])
                child2.append(parent1[idx])

        return child1, child2

    '''glowna metoda krzyzowania wywolujaca konkretne metody krzyzowania'''
    def crossover(self, parent1, parent2):
        if self.crossover_method == 'one_point':
            return self._crossover_one_point(parent1, parent2)
        elif self.crossover_method == 'two_point':
            return self._crossover_two_point(parent1, parent2)
        elif self.crossover_method == 'uniform':
            return self._crossover_uniform(parent1, parent2)

    '''
    metoda mutacji 
    - na razie jest to jedyna metoda mutacji w kodzie
    - nie zmienia jednego losowego genu, tylko przechodzac po kazdym genie losuje porownujac do Pm czy zmieniac gen 
    '''
    def mutation(self, chromosome):
        for idx in range(0, self.chromosome_size):
            if random.random() < self.Pm:
                chromosome[idx] = 1 - chromosome[idx]


    '''
    metoda tworzaca nowa populacje
    - przenosi za kazdym razem do nowej populacji jakis procent z obecnej populacji (elite) na podstawie "elitsm_rate".
    
    '''
    def replacement(self):
        elitism_amount = max(1, int(self.elitism_rate * self.N))
        sorted_indices = sorted(range(0, self.N), key=lambda i: self.fitness[i], reverse=True)
        elite_indices = sorted_indices[:elitism_amount]
        new_population = [self.population[i].copy() for i in elite_indices]

        # w tym przypadku rodzice moga sie powtarzac - sa oni wybierani losowo na podstawie metody selekcji
        while len(new_population) < self.N:
            parent1_idx = self.selection()
            parent2_idx = self.selection()
            # pytanie jak tutaj chcemy zeby bylo: 1)rodzic moze sam ze soba crossowac 2)tylko rozni rodzice moga
            # while parent1_idx == parent2_idx:
            #     parent2_idx = self.selection() # ta petla tez jest bledna bo w selekcji ruletkowej jest szansa ze bedzie zwracany ciagle ten sam osobnik i wtedy nieskonczona petla

            parent1 = self.population[parent1_idx]
            parent2 = self.population[parent2_idx]

            # crossover lub kopia rodzicow ktorzy i tak beda pozniej mutowani
            if random.random() < self.Pc:
                child1, child2 = self.crossover(parent1, parent2)
            else:
                child1 = parent1.copy() # czy taka kopia wystarczy? czy trzeba deepcopy
                child2 = parent2.copy()

            # mutacja dzieci
            self.mutation(child1)
            self.mutation(child2)

            # dodawanie dzieci do populacji
            if len(new_population) < self.N:
                new_population.append(child1)
            if len(new_population) < self.N:
                new_population.append(child2)

        self.population = new_population


    '''metoda kontrolujaca przebieg algorytmu - ja wywoluje uzytkownik. zwraca slownik ze statystykami'''
    def run(self):
        self.start_time = time.time()

        self.initialize()

        # czyszczenie zmiennch przechowujacych statystyki przed ruszeniem z petla
        self.best_solutions_history = []
        self.avg_solutions_history = []
        self.worst_solutions_history = []

        for iteration in range(1, self.T + 1):
            self.evaluate()
            self.replacement()

        self.evaluate()

        self.execution_time = time.time() - self.start_time

        return {
            'best_value': self.fitness[self.best_index],
            'best_individual': self.population[self.best_index],
            'worst_individual': self.population[self.worst_index],
            'worst_value': self.fitness[self.worst_index],
            'best_history': self.best_solutions_history,
            'avg_solutions_history': self.avg_solutions_history,
            'worst_history': self.worst_solutions_history,
            'execution_time': self.execution_time,
            'iterations': self.T
        }