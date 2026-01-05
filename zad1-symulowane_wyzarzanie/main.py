from algorythmSA import SimulatedAnnealing
from functions import funkcja_przykład3, funkcja_przykład4
from plots import *

parametry_algorytmu = {
    "T0": 1000,  # Temperatura początkowa
    "A": 0.7,      # Współczynnik chłodzenia
    "M": 1200,     # Liczba iteracji w T
    "k": 0.1,      # Współczynnik 'k'
}


def get_float_input(prompt, min_val=None, max_val=None):
    while True:
        try:
            val_str = input(prompt)
            val = float(val_str)
            if min_val is not None and val <= min_val:
                print(f"BŁĄD: Wartość musi być większa od {min_val}.")
                continue
            if max_val is not None and val >= max_val:
                 print(f"BŁĄD: Wartość musi być mniejsza od {max_val}.")
                 continue
            return val
        except ValueError:
            print("BŁĄD: Proszę podać poprawną liczbę.")

def get_int_input(prompt, min_val=1):
    """Bezpiecznie pobiera liczbę całkowitą od użytkownika."""
    while True:
        try:
            val_str = input(prompt)
            val = int(val_str)
            if min_val is not None and val < min_val:
                print(f"BŁĄD: Wartość musi być liczbą całkowitą, co najmniej {min_val}.")
                continue
            return val
        except ValueError:
            print("BŁĄD: Proszę podać poprawną liczbę całkowitą.")


def show_and_change_parameters():
    """Wyświetla pod-menu do zmiany parametrów."""
    global parametry_algorytmu
    
    while True:
        print("\n--- Zarządzanie Parametrami ---")
        print(f"Aktualne wartości:")
        print(f"  1. Temperatura początkowa (T0): {parametry_algorytmu['T0']}")
        print(f"  2. Współczynnik chłodzenia (A):  {parametry_algorytmu['A']}  (musi być < 1.0 i > 0.0)")
        print(f"  3. Liczba iteracji (M):         {parametry_algorytmu['M']}  (musi być >= 1)")
        print(f"  4. Współczynnik (k):            {parametry_algorytmu['k']}  (musi być > 0.0)")
        print("  5. Powrót do menu głównego")
        
        choice = input("Wybierz parametr do zmiany (1-5): ")
        
        if choice == '1':
            parametry_algorytmu['T0'] = get_float_input(
                f"Podaj nową wartość T0 (obecnie {parametry_algorytmu['T0']}): ", min_val=0.0
            )
        elif choice == '2':
            parametry_algorytmu['A'] = get_float_input(
                f"Podaj nową wartość A (obecnie {parametry_algorytmu['A']}): ", min_val=0.0, max_val=1.0
            )
        elif choice == '3':
            parametry_algorytmu['M'] = get_int_input(
                f"Podaj nową wartość M (obecnie {parametry_algorytmu['M']}): ", min_val=1
            )
        elif choice == '4':
            parametry_algorytmu['k'] = get_float_input(
                f"Podaj nową wartość k (obecnie {parametry_algorytmu['k']}): ", min_val=0.0
            )
        elif choice == '5':
            print("Zapisano parametry, powrót do menu głównego.")
            break
        else:
            print("Niepoprawna opcja, wybierz numer od 1 do 5.")

def run_experiment(experiment_name, objective_function, x_min, x_max):
    global parametry_algorytmu
    
    print("\n" + "="*60)
    print(f" Rozpoczynam eksperyment: {experiment_name}")
    print(f" Użyte parametry: T0={parametry_algorytmu['T0']}, A={parametry_algorytmu['A']}, M={parametry_algorytmu['M']}, k={parametry_algorytmu['k']}")
    print("="*60)
    
    sa = SimulatedAnnealing(
        T0=parametry_algorytmu['T0'],
        A=parametry_algorytmu['A'],
        M=parametry_algorytmu['M'],
        k=parametry_algorytmu['k']
    )
    best_x, best_f = sa.solve(objective_function, x_min, x_max)
    
    print_experiment_summary(sa, best_x, best_f, experiment_name)
    plot_results(
        objective_function,
        x_min,
        x_max,
        history_points = sa.best_solutions_history,
    )

def print_experiment_summary(solver_instance, best_x, best_f, experiment_name):
    print(f"--- Podsumowanie eksperymentu: {experiment_name} ---")
    print(f"Całkowita liczba iteracji: {solver_instance.total_iterations}")
    print(f"Liczba zaakceptowanych korekcji rozwiązań: {solver_instance.licznik_korekcji}")
    print(f"Czas wykonania: {solver_instance.execution_time:.6f} s")
    print(f"Najlepsze rozwiązanie znaleziono w iteracji: {solver_instance.best_solution_iteration}")
    print(f"\nNajlepsze znalezione rozwiązanie: x = {best_x:.20f}")
    print(f"Wartość funkcji: f(x) = {best_f:.20f}\n")
    
    print("--- Historia najlepszych rozwiązań (kolejne korekcje) ---")
    print(f"{'Indeks':<10} | {'x':<25} | {'f(x)':<25}")
    print("-" * 62)
    for entry in solver_instance.best_solutions_history:
        indeks, x, y = entry
        print(f"{indeks:<10} | {x:<25.20f} | {y:<25.20f}")
    print("\n")


def main_menu():
    """Wyświetla główne menu tekstowe i obsługuje wybór użytkownika."""
    while True:
        print("\n" + "---" * 20)
        print(" GŁÓWNE MENU - ALGORYTM SYMULOWANEGO WYŻARZANIA (SA)")
        print("---" * 20)
        print(f"Aktualne parametry: T0={parametry_algorytmu['T0']}, A={parametry_algorytmu['A']}, M={parametry_algorytmu['M']}, k={parametry_algorytmu['k']}")
        print("\nOpcje:")
        print("  1. Zmień parametry algorytmu")
        print("  2. Uruchom eksperyment (Funkcja z Rozdziału 3)")
        print("  3. Uruchom eksperyment (Funkcja z Rozdziału 4)")
        print("  4. Wyjście")
        
        choice = input("\nWybierz opcję (1-4): ")
        
        if choice == '1':
            show_and_change_parameters()
            
        elif choice == '2':
            run_experiment(
                experiment_name="Funkcja z Rozdziału 3 (Przykład 1)",
                objective_function=funkcja_przykład3,
                x_min=-150,
                x_max=150
            )
            
        elif choice == '3':
            run_experiment(
                experiment_name="Funkcja z Rozdziału 4",
                objective_function=funkcja_przykład4,
                x_min=-1,  
                x_max=2    
            )
            
        elif choice == '4':
            print("Zakończono program.")
            break
            
        else:
            print("Niepoprawna opcja. Proszę wybrać numer od 1 do 4.")

if __name__ == "__main__":
    main_menu()