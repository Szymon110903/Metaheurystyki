import math

import numpy as np


# przykladowa funkcja
def booth_function(vector):
    x, y = vector[0], vector[1]
    return (x + 2*y - 7)**2 + (2*x + y - 5)**2

def example1(X):
    A = 10
    y = A*2 + sum([(x**2 - A * np.cos(2 * math.pi * x)) for x in X])
    return y