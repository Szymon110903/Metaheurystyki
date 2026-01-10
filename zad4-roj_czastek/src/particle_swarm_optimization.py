import random
import time

class Particle:
    def __init__(self, position_x, position_y, fitness):
        self.x = position_x
        self.y = position_y
        self.vx = 0.0
        self.vy = 0.0

        self.fitness = fitness

        self.best_position = (self.x, self.y)
        self.best_value = self.fitness(self.x, self.y)

    def evaluate(self):
        value = self.fitness(self.x, self.y)
        if value < self.best_value:
            self.best_value = value
            self.best_position = (self.x, self.y)
        return value

    def move(self, gbest_position, w, c1, c2, v_max, bounds):
        # TODO: sprawdzic czy tutaj nie powinno sie losowac r1 i r2 osobno dla vx i vy (tak zeby byly 4 losowania a nie 2)
        r1 = random.random()
        r2 = random.random()

        px, py = self.best_position
        gx, gy = gbest_position

        self.vx = w * self.vx + c1 * r1 * (px - self.x) + c2 * r2 * (gx - self.x)
        self.vy = w * self.vy + c1 * r1 * (py - self.y) + c2 * r2 * (gy - self.y)

        if self.vx > v_max: self.vx = v_max
        if self.vx < -v_max: self.vx = -v_max
        if self.vy > v_max: self.vy = v_max
        if self.vy < -v_max: self.vy = -v_max

        self.x += self.vx
        self.y += self.vy

        (xmin, xmax), (ymin, ymax) = bounds

        if self.x < xmin: self.x = xmin
        if self.x > xmax: self.x = xmax
        if self.y < ymin: self.y = ymin
        if self.y > ymax: self.y = ymax


class ParticleSwarmOptimization:
    def __init__(self, fitness, bounds, n_particles=30, w=0.7, c1=1.5, c2=1.5, v_max=1.0, n_iterations=30):
        self.fitness = fitness
        self.bounds = bounds

        self.n_particles = n_particles
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.v_max = v_max
        self.n_iterations = n_iterations

        (xmin, xmax), (ymin, ymax) = bounds
        self.swarm = []

        for _ in range(self.n_particles):
            x = random.uniform(xmin, xmax)
            y = random.uniform(ymin, ymax)
            p = Particle(x, y, self.fitness)

            self.swarm.append(p)

        best = self.swarm[0]
        for p in self.swarm:
            if p.best_value < best.best_value:
                best = p

        self.gbest_position = best.best_position
        self.gbest_value = best.best_value

    def run(self):
        for _ in range(self.n_iterations):
            for p in self.swarm:
                p.move(self.gbest_position, self.w, self.c1, self.c2, self.v_max, self.bounds)
                p.evaluate()

                if p.best_value < self.gbest_value:
                    self.gbest_value = p.best_value
                    self.gbest_position = p.best_position

        return self.gbest_position, self.gbest_value
