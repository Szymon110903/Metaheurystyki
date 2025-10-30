from asyncio import graph

class AntColony:
    def __init__(self, num_ants, num_iterations, Q, A, B, rho, data):
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.Q = Q        #stała ilośc feromonu pozostawiana przez mrówkę
        self.A = A        #waga śladu feromonu
        self.B = B        #waga informacji heurystycznej
        self.rho = rho    #współczynnik parowania feromonu
        self.data = data  #dane wejściowe


    def run(self):
        
        for iter in range(self.num_iterations):
            for ant in range(self.num_ants):
                print(f"Iteration {iter+1}, Ant {ant+1}")
            #     self.make_tour()
            # self.evaporate_pheromone()
            # self.update_pheromone()
        