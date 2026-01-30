from __future__ import annotations
from typing import List
from .models import Customer, Route, Solution
from .evaluation import simulate_route

def can_append_feasible(
    nodes: List[Customer],
    dist: List[List[float]],
    capacity: int,
    route: Route,
    customer_id: int
) -> bool:
    """
    True jeśli po dopisaniu customer_id na koniec route:
    - load <= capacity
    - late_time == 0 (wliczając okno depo na powrocie)
    """
    new_stops = route.stops + [customer_id]
    stats = simulate_route(nodes, dist, capacity, new_stops)

    if stats.load > capacity:
        return False
    if stats.late_time > 0:
        return False
    return True


def build_initial_solution_ready_time(
    nodes: List[Customer],
    dist: List[List[float]],
    capacity: int,
    max_vehicles: int
) -> Solution:
    """
    Buduje rozwiązanie startowe:
    - klienci sortowani po ready_time
    - do trasy dokładamy pierwszego wykonalnego kandydata (late_time == 0, load <= capacity)
    - jeśli nie da się nic dołożyć -> nowa trasa
    """
    n = len(nodes) - 1
    remaining = list(range(1, n + 1))
    remaining.sort(key=lambda cid: nodes[cid].ready_time)

    routes: List[Route] = []

    while remaining:
        if len(routes) >= max_vehicles:
            raise ValueError(
                f"Nie udało się zbudować wykonalnego rozwiązania w limicie {max_vehicles} pojazdów "
                f"(pozostało klientów: {len(remaining)})."
            )

        current = Route(stops=[])

        # próbujemy dokładać dopóki znajdziemy wykonalnego klienta
        improved = True
        while improved and remaining:
            improved = False
            for cid in list(remaining):  # iterujemy po kopii, bo będziemy usuwać

                if can_append_feasible(nodes, dist, capacity, current, cid):
                    current.stops.append(cid)
                    remaining.remove(cid)
                    improved = True
                    break  # bierzemy pierwszego wykonalnego i wracamy na początek pętli

        if not current.stops:
            # jeżeli nie udało się dodać nikogo do pustej trasy,
            # to znaczy, że sam pojedynczy klient jest niewykonalny (z oknem depo),
            # co w Solomonie raczej nie powinno się zdarzyć.
            cid = remaining[0]
            raise ValueError(f"Klient {cid} nie może być obsłużony w pojedynczej trasie (late_time>0).")

        routes.append(current)

    return Solution(routes=routes)