import math
from typing import List
from .models import Customer

def euclidean(a: Customer, b: Customer) -> float:
    return math.hypot(a.x - b.x, a.y - b.y)

def build_distance_matrix(customers: List[Customer]) -> List[List[float]]:
    '''
    customers[0] = Depot, customers[1..N] = klienci
    '''
    nodes = customers
    n = len(customers)
    dist = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dist[i][j] = euclidean(nodes[i], nodes[j])
    return dist
