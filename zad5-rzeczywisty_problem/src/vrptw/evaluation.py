from dataclasses import dataclass
from .models import Customer, Solution
from .validation import validate_solution


@dataclass(frozen=True)
class RouteStats:
    distance: float
    load: int
    late_time: float
    start_service_times: list[float]
    end_time: float

@dataclass(frozen=True)
class Score:
    vehicles: int
    penalty: float
    distance: float

    def key(self) -> tuple[int, float, float]:
        return (self.vehicles, self.penalty, self.distance)

'''
Symulacja przejazdu jednej trasy, zwraca statystyki trasy
'''
def simulate_route(
    nodes: list[Customer],
    dist: list[list[float]],
    route_stops: list[int],
) -> RouteStats:
    t = 0.0
    total_dist = 0.0
    load = 0
    late = 0.0
    start_times: list[float] = []

    prev = 0  # depot

    for cid in route_stops:
        c = nodes[cid]

        travel = dist[prev][cid]
        total_dist += travel
        t += travel

        if t < c.ready_time:
            t = c.ready_time

        if t > c.due_date:
            late += (t - c.due_date)

        start_times.append(t)

        t += c.service_time
        load += c.demand
        prev = cid

    total_dist += dist[prev][0]
    t += dist[prev][0]

    depot = nodes[0]
    if t < depot.ready_time:
        t = depot.ready_time
    if t > depot.due_date:
        late += (t - depot.due_date)

    return RouteStats(
        distance=total_dist,
        load=load,
        late_time=late,
        start_service_times=start_times,
        end_time=t,
    )

'''
Suma statystyk dla całego rozwiązania
'''
def evaluate_solution(
    nodes: list[Customer],
    dist: list[list[float]],
    capacity: int,
    max_vehicles: int,
    solution: Solution
) -> Score:
    n_customers = len(nodes) - 1
    validate_solution(solution, n_customers, max_vehicles)

    total_dist = 0.0
    total_late = 0.0
    total_overflow = 0.0

    for route in solution.routes:
        rs = simulate_route(nodes, dist, route.stops)
        total_dist += rs.distance
        total_late += rs.late_time
        if rs.load > capacity:
            total_overflow += (rs.load - capacity)

    penalty = total_late + 1000.0 * total_overflow
    return Score(vehicles=len(solution.routes), penalty=penalty, distance=total_dist) # przyklad: Score(vehicles=25, penalty=6882.222876879532, distance=2699.346467857258)
