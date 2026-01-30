from collections import Counter
from .models import Solution

def validate_solution(solution: Solution, n_customers: int, max_vehicles: int) -> None:
    if len(solution.routes) == 0:
        raise ValueError("Solution ma 0 tras.")

    if len(solution.routes) > max_vehicles:
        raise ValueError(f"Za dużo tras: {len(solution.routes)} > max_vehicles={max_vehicles}")

    all_ids: list[int] = []
    for r_idx, route in enumerate(solution.routes):
        if len(route.stops) == 0:
            raise ValueError(f"Pusta trasa na indeksie {r_idx}")
        for cid in route.stops:
            if cid == 0:
                raise ValueError("Depot (0) nie może występować w Route.stops")
            if cid < 1 or cid > n_customers:
                raise ValueError(f"Niepoprawny ID klienta {cid} (dozwolone 1..{n_customers})")
        all_ids.extend(route.stops)

    counts = Counter(all_ids)

    dupes = [cid for cid, c in counts.items() if c > 1]
    if dupes:
        raise ValueError(f"Duplikaty klientów w rozwiązaniu: {dupes[:10]}")

    missing = [cid for cid in range(1, n_customers + 1) if cid not in counts]
    if missing:
        raise ValueError(f"Brakujących klientów: {missing[:10]}")
