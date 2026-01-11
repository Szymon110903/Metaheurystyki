import random
import time
import matplotlib.pyplot as plt

'''
format bounds
bounds = [
    (min_x1, max_x1),
    (min_x2, max_x2),
    ...
    (min_xN, max_xN)
]
'''


class Particle:
    def __init__(self, position, fitness, mm):
        self.position = position.copy() # kopia przekazanej listy pozycji
        dim = len(position)
        self.velocity = [0.0] * dim

        self.fitness = lambda X: mm * fitness(X)

        self.best_position = self.position.copy()
        self.best_value = self.fitness(self.position)

    def evaluate(self):
        value = self.fitness(self.position)
        if value < self.best_value:
            self.best_value = value
            self.best_position = self.position.copy()
        return value

    def move(self, gbest_position, w, c1, c2, v_max, bounds):
        dim = len(self.position)

        for i in range(dim):
            r1 = random.random()
            r2 = random.random()

            # aktualizacja predkosci
            self.velocity[i] = (
                w * self.velocity[i]
                + c1 * r1 * (self.best_position[i] - self.position[i])
                + c2 * r2 * (gbest_position[i] - self.position[i])
            )

            # przyciecie predkosci do granic
            if self.velocity[i] > v_max:
                self.velocity[i] = v_max
            elif self.velocity[i] < -v_max:
                self.velocity[i] = -v_max

            # aktualizacja pozycji
            self.position[i] += self.velocity[i]

            # bounds dla i-tego wymiaru
            min_i, max_i = bounds[i]
            if self.position[i] < min_i:
                self.position[i] = min_i
            elif self.position[i] > max_i:
                self.position[i] = max_i


class ParticleSwarmOptimization:
    def __init__(self, fitness, bounds, n_particles=30, n_iterations=30, w=0.7, c1=1.5, c2=1.5, v_max=1.0, minimization=True):
        self.fitness = fitness
        self.bounds = bounds

        self.n_particles = n_particles
        self.n_iterations = n_iterations
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.v_max = v_max

        self.mm = None
        if minimization:
            self.mm = 1
        else:
            self.mm = -1

        self.swarm = []
        dim = len(bounds)

        for _ in range(self.n_particles):
            position = []
            for i in range(dim):
                min_i, max_i = bounds[i]
                position.append(random.uniform(min_i, max_i))

            p = Particle(position, self.fitness, self.mm)
            self.swarm.append(p)

        best = self.swarm[0]
        for p in self.swarm[1:]:
            if p.best_value < best.best_value:
                best = p

        self.gbest_position = best.best_position.copy()
        self.gbest_value = best.best_value

    def iterate(self):
        improved = False
        for p in self.swarm:
            p.move(self.gbest_position, self.w, self.c1, self.c2, self.v_max, self.bounds)
            p.evaluate()

            if p.best_value < self.gbest_value:
                self.gbest_value = p.best_value
                self.gbest_position = p.best_position.copy()
                improved = True
        return improved

    def run(self, patience=10, plot=False, pause=0.01):
        no_improvement = 0

        history = []

        if plot:
            plt.ion()
            fig, ax = plt.subplots()
            line, = ax.plot([], [])
            ax.set_xlabel("iteration")
            ax.set_ylabel("best value")
            fig.show()

        for it in range(self.n_iterations):
            improved = self.iterate()

            # zapis prawdziwej wartości (odwiniętej z mm)
            best_real_value = self.mm * self.gbest_value
            history.append(best_real_value)

            if plot:
                line.set_data(range(len(history)), history)
                ax.relim()
                ax.autoscale_view()
                plt.pause(pause)

            if improved:
                no_improvement = 0
            else:
                no_improvement += 1

            if no_improvement >= patience:
                break

        if plot:
            plt.ioff()
            plt.show()

        return self.gbest_position, self.mm * self.gbest_value, history
