from __future__ import annotations
from pathlib import Path
from typing import List, Optional, Tuple, Dict
from .models import Customer


def load_solomon(path: str | Path) -> Tuple[str, int, int, Customer, List[Customer]]:
    path = Path(path)
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()

    # capacity i max_vehicles
    max_vehicles: Optional[int] = None
    capacity: Optional[int] = None
    for i, line in enumerate(lines):
        if "CAPACITY" in line.upper():
            for j in range(i + 1, min(i + 8, len(lines))):
                parts = lines[j].split()
                if len(parts) >= 2 and parts[0].lstrip("-").isdigit() and parts[1].lstrip("-").isdigit():
                    max_vehicles = int(parts[0])
                    capacity = int(parts[1])
                    break
        if capacity is not None:
            break

    if max_vehicles is None or capacity is None:
        raise ValueError(f"Nie znaleziono NUMBER/CAPACITY w pliku: {path}")

    # start sekcji klientów
    start_idx: Optional[int] = None
    for i, line in enumerate(lines):
        u = line.upper()
        if "CUST" in u and "NO" in u:
            start_idx = i + 1
            break
    if start_idx is None:
        for i, line in enumerate(lines):
            parts = line.split()
            if len(parts) >= 7 and parts[0].lstrip("-").isdigit():
                start_idx = i
                break
    if start_idx is None:
        raise ValueError(f"Nie znaleziono sekcji klientów w pliku: {path}")

    records: List[Customer] = []
    for line in lines[start_idx:]:
        parts = line.split()
        if len(parts) < 7:
            continue
        try:
            cid = int(parts[0])
            x = float(parts[1])
            y = float(parts[2])
            demand = int(parts[3])
            ready = float(parts[4])
            due = float(parts[5])
            service = float(parts[6])
        except ValueError:
            continue
        records.append(Customer(
            id=cid,
            x=x,
            y=y,
            demand=demand,
            ready_time=ready,
            due_date=due,
            service_time=service))

    depot_candidates = [c for c in records if c.id == 0]
    if not depot_candidates:
        raise ValueError("Brak depo (id=0) w danych.")
    depot = depot_candidates[0]

    customers = [c for c in records if c.id != 0]
    customers.sort(key=lambda c: c.id)

    return path.stem, max_vehicles, capacity, depot, customers
