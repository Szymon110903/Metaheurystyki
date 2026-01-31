from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class Customer:
    '''
    cel: przechowywanie danych klienta/depotu
    '''

    id: int
    # TODO: x,y moze nie jako odzielne floaty, tylko (x,y)
    x: float
    y: float
    # TODO: (invariant) demand >= 0
    demand: int
    # TODO: (invariant) ready_time <= due_date
    ready_time: float
    due_date: float
    service_time: float

@dataclass(frozen=True)
class Instance:
    '''
    cel: opis "świata problemu" (dane wejściowe + stałe ograniczenia)
    '''

    name: str
    max_vehicles: int
    capacity: int
    # TODO: do wyboru czy przechowywac depot_id jedynie czy obiekt Customera
    # depot_id: int
    depot: Customer
    customers: List[Customer]  # id=1..100, wtedy id=0 to bedzie Depot
    distance_matrix: List[List[float]]

    def get_customer(self, customer_id: int) -> Customer:
        return self.customers[customer_id]

    def get_travel_time(self, point_a: Customer, point_b: Customer) -> float:
        return self.distance_matrix[point_a.id][point_b.id]


# TODO: czy rzeczywiście jest do tego potrzebna klasa?
@dataclass
class Route:
    stops: List[int] # lista ID klientów (bez Depot)

@dataclass
class Solution:
    routes: List[Route]