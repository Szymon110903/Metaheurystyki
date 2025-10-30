import time
import os
import data.dataReader as dr
import ant_Algorythm as aco

# (Funkcje pomocnicze menu)

def wyczysc_ekran():
    """Wyczyść ekran terminala dla czytelności."""
    os.system('cls' if os.name == 'nt' else 'clear')

def wyswietl_aktualne_parametry(parametry):
    """Wyświetla aktualne wartości wszystkich ustawień."""
    print("--- AKTUALNE USTAWIENIA ALGORYTMU ---")

    
    print(f"  Plik danych (wczytywanie): {parametry['plik_danych']}")
    print(f"  Ilość mrówek:              {parametry['ilosc_mrowek']}")
    print(f"  Ilość iteracji:            {parametry['ilosc_iteracji']}")
    print(f"  Waga feromonu (alpha):     {parametry['alpha']:.2f}")
    print(f"  Waga heurystyki (beta):    {parametry['beta']:.2f}")
    print(f"  Wsp. parowania (rho):      {parametry['rho']:.2f}  (musi być 0 < rho < 1)")
    print(f"  Ilość feromonu (Q):        {parametry['Q']:.2f}")
    print("-" * 38)

def menu_zmiany_danych(aktualne_parametry):
    """Pod-menu do zmiany parametrów (bez zmian logiki)"""
    nowe_parametry = aktualne_parametry.copy()

    while True:
        wyczysc_ekran()
        print("--- ZMIANA PARAMETRÓW ALGORYTMU ---")
        
        print("\nKtóry parametr chcesz zmienić?")
        print(f"  1. Plik wczytywania danych ({nowe_parametry['plik_danych']})")
        print(f"  2. Ilość mrówek            ({nowe_parametry['ilosc_mrowek']})")
        print(f"  3. Ilość iteracji          ({nowe_parametry['ilosc_iteracji']})")
        print(f"  4. Waga feromonu (alpha)   ({nowe_parametry['alpha']:.2f})")
        print(f"  5. Waga heurystyki (beta)  ({nowe_parametry['beta']:.2f})")
        print(f"  6. Wsp. parowania (rho)    ({nowe_parametry['rho']:.2f})")
        print(f"  7. Ilość feromonu (Q)      ({nowe_parametry['Q']:.2f})")
        print("\n  8. POWRÓT do menu głównego")
        print("-" * 38)
        
        wybor_param = input("Wybierz opcję [1-8]: ")

        if wybor_param == '1':
            wyczysc_ekran()
            print("--- WYBÓR PLIKU DANYCH ---")
            
            dostepne_pliki = ["A-n32-k5.txt", "A-n80-k5.txt"] # Poprawka literówki
            
            print("\nDostępne pliki do wyboru:")
            for i, nazwa_pliku in enumerate(dostepne_pliki):
                print(f"  {i + 1}. {nazwa_pliku}")
            
            print("\n  0. Anuluj i wróć")
            print("-" * 30)
            
            while True: 
                wybor_pliku = input(f"Wybierz numer pliku [1-{len(dostepne_pliki)}] (lub 0): ")
                
                if wybor_pliku == '0':
                    print("[INFO] Anulowano zmianę.")
                    break 
                    
                try:
                    numer_pliku = int(wybor_pliku)
                    if 1 <= numer_pliku <= len(dostepne_pliki):
                        wybrany_plik = dostepne_pliki[numer_pliku - 1]
                        nowe_parametry['plik_danych'] = wybrany_plik
                        print(f"[INFO] Wybrano plik danych: {wybrany_plik}")
                        break
                    else:
                        print(f"[BŁĄD] Nieprawidłowy numer. Wprowadź liczbę od 1 do {len(dostepne_pliki)}.")
                except ValueError:
                    print("[BŁĄD] To nie jest liczba. Spróbuj ponownie.")
            
            time.sleep(1.5)

        elif wybor_param == '2':
            stara_wartosc = nowe_parametry['ilosc_mrowek']
            print(f"Aktualna wartość: {stara_wartosc}")
            while True:
                nowa_wartosc_str = input("Podaj nową ilość mrówek (Enter, aby anulować): ")
                if not nowa_wartosc_str:
                    print("[INFO] Anulowano zmianę.")
                    break
                try:
                    nowa_wartosc_int = int(nowa_wartosc_str)
                    if nowa_wartosc_int > 0:
                        nowe_parametry['ilosc_mrowek'] = nowa_wartosc_int
                        print(f"[INFO] Zmieniono ilość mrówek na: {nowa_wartosc_int}")
                        break
                    else:
                        print("[BŁĄD] Ilość mrówek musi być liczbą dodatnią (większą od 0).")
                except ValueError:
                    print("[BŁĄD] To nie jest poprawna liczba całkowita.")
            time.sleep(1)

        elif wybor_param == '3':
            stara_wartosc = nowe_parametry['ilosc_iteracji']
            print(f"Aktualna wartość: {stara_wartosc}")
            while True:
                nowa_wartosc_str = input("Podaj nową ilość iteracji (Enter, aby anulować): ")
                if not nowa_wartosc_str:
                    print("[INFO] Anulowano zmianę.")
                    break
                try:
                    nowa_wartosc_int = int(nowa_wartosc_str)
                    if nowa_wartosc_int > 0:
                        nowe_parametry['ilosc_iteracji'] = nowa_wartosc_int
                        print(f"[INFO] Zmieniono ilość iteracji na: {nowa_wartosc_int}")
                        break
                    else:
                        print("[BŁĄD] Ilość iteracji musi być liczbą dodatnią (większą od 0).")
                except ValueError:
                    print("[BŁĄD] To nie jest poprawna liczba całkowita.")
            time.sleep(1)

        elif wybor_param == '4':
            stara_wartosc = nowe_parametry['alpha']
            print(f"Aktualna wartość: {stara_wartosc}")
            while True:
                nowa_wartosc_str = input("Podaj nową wagę feromonu (alpha) (Enter, aby anulować): ").replace(',', '.')
                if not nowa_wartosc_str:
                    print("[INFO] Anulowano zmianę.")
                    break
                try:
                    nowa_wartosc_float = float(nowa_wartosc_str)
                    if nowa_wartosc_float >= 0:
                        nowe_parametry['alpha'] = nowa_wartosc_float
                        print(f"[INFO] Zmieniono 'alpha' na: {nowa_wartosc_float:.2f}")
                        break
                    else:
                        print("[BŁĄD] Waga nie może być ujemna (musi być >= 0).")
                except ValueError:
                    print("[BŁĄD] To nie jest poprawna liczba (np. 1.0 lub 0.5).")
            time.sleep(1)
            
        elif wybor_param == '5':
            stara_wartosc = nowe_parametry['beta']
            print(f"Aktualna wartość: {stara_wartosc}")
            while True:
                nowa_wartosc_str = input("Podaj nową wagę heurystyki (beta) (Enter, aby anulować): ").replace(',', '.')
                if not nowa_wartosc_str:
                    print("[INFO] Anulowano zmianę.")
                    break
                try:
                    nowa_wartosc_float = float(nowa_wartosc_str)
                    if nowa_wartosc_float >= 0:
                        nowe_parametry['beta'] = nowa_wartosc_float
                        print(f"[INFO] Zmieniono 'beta' na: {nowa_wartosc_float:.2f}")
                        break
                    else:
                        print("[BŁĄD] Waga nie może być ujemna (musi być >= 0).")
                except ValueError:
                    print("[BŁĄD] To nie jest poprawna liczba (np. 1.0 lub 2.5).")
            time.sleep(1)

        elif wybor_param == '6':
            stara_wartosc = nowe_parametry['rho']
            print(f"Aktualna wartość: {stara_wartosc}")
            while True:
                nowa_wartosc_str = input("Podaj nowy wsp. parowania (rho) (Enter, aby anulować): ").replace(',', '.')
                if not nowa_wartosc_str:
                    print("[INFO] Anulowano zmianę.")
                    break
                try:
                    nowa_wartosc_float = float(nowa_wartosc_str)
                    if 0 < nowa_wartosc_float < 1:
                        nowe_parametry['rho'] = nowa_wartosc_float
                        print(f"[INFO] Zmieniono 'rho' na: {nowa_wartosc_float:.2f}")
                        break
                    else:
                        print("[BŁĄD] Współczynnik musi być liczbą Pomiędzy 0 a 1 (np. 0.1 lub 0.5).")
                except ValueError:
                    print("[BŁĄD] To nie jest poprawna liczba (np. 0.5).")
            time.sleep(1)

        elif wybor_param == '7':
            stara_wartosc = nowe_parametry['Q']
            print(f"Aktualna wartość: {stara_wartosc}")
            while True:
                nowa_wartosc_str = input("Podaj nową ilość feromonu (Q) (Enter, aby anulować): ").replace(',', '.')
                if not nowa_wartosc_str:
                    print("[INFO] Anulowano zmianę.")
                    break
                try:
                    nowa_wartosc_float = float(nowa_wartosc_str)
                    if nowa_wartosc_float > 0:
                        nowe_parametry['Q'] = nowa_wartosc_float
                        print(f"[INFO] Zmieniono 'Q' na: {nowa_wartosc_float:.2f}")
                        break
                    else:
                        print("[BŁĄD] Ilość feromonu musi być dodatnia (większa od 0).")
                except ValueError:
                    print("[BŁĄD] To nie jest poprawna liczba (np. 100 lub 50.5).")
            time.sleep(1)

        elif wybor_param == '8':
            print("Zapisywanie zmian i powrót do menu głównego...")
            return nowe_parametry
        
        else:
            print("[BŁĄD] Nieprawidłowa opcja. Wybierz 1-8.")
            time.sleep(1)

def uruchom_program(parametry):
    data = dr.read_data_from_file(parametry['plik_danych'])
    aco.AntColony(
        num_ants=parametry['ilosc_mrowek'],
        num_iterations=parametry['ilosc_iteracji'],
        Q=parametry['Q'],
        A=parametry['alpha'],
        B=parametry['beta'],
        rho=parametry['rho'],
        data=data
    ).run()



def main():
    parametry_aco = {
        'plik_danych': 'A-n32-k5.txt', 
        'ilosc_mrowek': 50,
        'ilosc_iteracji': 100,
        'alpha': 1.0,
        'beta': 2.0,
        'rho': 0.5,
        'Q': 100.0
    }

    while True:
        wyczysc_ekran()
        print("=" * 38)
        print("    GŁÓWNE MENU SYMULATORA ACO")
        print("=" * 38)
        
        wyswietl_aktualne_parametry(parametry_aco)

        print("\nOpcje:")
        print("  1. Zmień ustawienia algorytmu")
        print("  2. Uruchom algorytm (na aktualnych danych)")
        print("  3. Wyjdź z programu")
        print("-" * 38)
        
        wybor_glowny = input("Wybierz opcję [1-3]: ")

        if wybor_glowny == '1':
            parametry_aco = menu_zmiany_danych(parametry_aco)
            
        elif wybor_glowny == '2':
            # === POPRAWKA ===
            # Najpierw czyścimy menu
            wyczysc_ekran() 
            print("--- URUCHAMIANIE PROGRAMU ---")
            
            uruchom_program(parametry_aco)
            
            input("\nWciśnij Enter, aby wrócić do menu głównego...")
            
        elif wybor_glowny == '3':
            print("Zamykanie programu. Do widzenia!")
            break 
            
        else:
            print("\n[BŁĄD] Nieprawidłowa opcja. Wybierz 1, 2 lub 3.")
            time.sleep(1.5)

if __name__ == "__main__":
    main()