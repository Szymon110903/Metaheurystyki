import time
import os
import numpy as np 
import ant_Algorythm as aco
import data.dataReader as dr

# funkcje pomocmnicze do menu
def wyczysc_ekran():
    os.system('cls' if os.name == 'nt' else 'clear')

def wyswietl_aktualne_parametry(parametry):
    print("--- AKTUALNE USTAWIENIA ALGORYTMU ---")
    print(f"  Plik danych (wczytywanie): {parametry['plik_danych']}")
    print(f"  Ilość mrówek:              {parametry['ilosc_mrowek']}")
    print(f"  Ilość iteracji:            {parametry['ilosc_iteracji']}")
    print(f"  Waga feromonu (alpha):     {parametry['alpha']:.2f}")
    print(f"  Waga heurystyki (beta):    {parametry['beta']:.2f}")
    print(f"  Wsp. parowania (rho):      {parametry['rho']:.2f}")
    print(f"  Prawd. losowe (p_random):  {parametry['p_random']:.2f}") # NOWE
    print(f"  Ilość feromonu (Q):        {parametry['Q']:.2f}")
    print("-" * 38)

def menu_zmiany_danych(aktualne_parametry):
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
        print(f"  7. Prawd. losowe (p_rand)  ({nowe_parametry['p_random']:.2f})") # NOWE
        print(f"  8. Ilość feromonu (Q)      ({nowe_parametry['Q']:.2f})")
        print("\n  0. POWRÓT do menu głównego")
        print("-" * 38)
        
        wybor_param = input("Wybierz opcję [0-8]: ")

        if wybor_param == '1':
                wyczysc_ekran()
                print("--- WYBÓR PLIKU DANYCH ---")
                
                katalog_projektu = os.path.dirname(os.path.abspath(__file__))
                sciezka_data = os.path.join(katalog_projektu, "data")
                
                print(f"[DEBUG] Szukam folderu 'data' pod ścieżką:")
                print(f" -> {sciezka_data}")
                
                if not os.path.exists(sciezka_data):
                    print("\n[BŁĄD KRYTYCZNY] System nie widzi tego folderu!")
                    print("Upewnij się, że folder nazywa się dokładnie 'data' (małe litery).")
                    time.sleep(4)
                    continue

                try:
                    dostepne_pliki = [f for f in os.listdir(sciezka_data) if f.endswith(".txt")]
                except Exception as e:
                    print(f"[BŁĄD] Wystąpił błąd przy odczycie folderu: {e}")
                    dostepne_pliki = []
                
                if not dostepne_pliki:
                    print("\n[INFO] Folder istnieje, ale nie ma w nim plików .txt.")
                    print("Sprawdź czy pliki nie mają podwójnych rozszerzeń (np. przyklad.txt.txt)")
                    time.sleep(4)
                    continue

                print("\nDostępne pliki do wyboru:")
                for i, nazwa_pliku in enumerate(dostepne_pliki):
                    print(f"  {i + 1}. {nazwa_pliku}")
                
                print("\n  0. Anuluj i wróć")
                
                wybor_pliku = input(f"Wybierz numer pliku [1-{len(dostepne_pliki)}]: ")
                
                if wybor_pliku == '0':
                    print("[INFO] Anulowano.")
                    time.sleep(1)
                    continue 

                try:
                    numer_pliku = int(wybor_pliku)
                    if 1 <= numer_pliku <= len(dostepne_pliki):
                        wybrany_plik = dostepne_pliki[numer_pliku - 1]
                        nowe_parametry['plik_danych'] = wybrany_plik
                        print(f"[INFO] Wybrano plik danych: {wybrany_plik}")
                        time.sleep(1)
                    else:
                        print("[BŁĄD] Nieprawidłowy numer.")
                        time.sleep(1)
                except ValueError:
                    print("[BŁĄD] To nie jest liczba.")
                time.sleep(1)

        elif wybor_param == '2':
            val = input("Nowa ilość mrówek: ")
            if val.isdigit(): nowe_parametry['ilosc_mrowek'] = int(val)

        elif wybor_param == '3':
            val = input("Nowa ilość iteracji: ")
            if val.isdigit(): nowe_parametry['ilosc_iteracji'] = int(val)

        elif wybor_param == '4':
            try: nowe_parametry['alpha'] = float(input("Nowa alpha: ").replace(',','.'))
            except: pass

        elif wybor_param == '5':
            try: nowe_parametry['beta'] = float(input("Nowa beta: ").replace(',','.'))
            except: pass

        elif wybor_param == '6':
            try: nowe_parametry['rho'] = float(input("Nowe rho (0-1): ").replace(',','.'))
            except: pass
            
        elif wybor_param == '7':
            try: nowe_parametry['p_random'] = float(input("Nowe p_random (0-1): ").replace(',','.'))
            except: pass

        elif wybor_param == '8':
            try: nowe_parametry['Q'] = float(input("Nowe Q: ").replace(',','.'))
            except: pass

        elif wybor_param == '0':
            return nowe_parametry
        
        else:
            print("Nieprawidłowa opcja.")
            time.sleep(0.5)

def uruchom_pojedynczy_program(parametry):
    print("\n[INFO] Wczytywanie danych...")
    data = dr.read_data_from_file(parametry['plik_danych'])
    if not data: return

    print(f"[INFO] Uruchamianie algorytmu dla {len(data)} miast...")
    colony = aco.AntColony(
        num_ants=parametry['ilosc_mrowek'],
        num_iterations=parametry['ilosc_iteracji'],
        Q=parametry['Q'],
        A=parametry['alpha'],
        B=parametry['beta'],
        rho=parametry['rho'],
        p_random=parametry['p_random'],
        data=data
    )
    colony.run(verbose=True)

def uruchom_eksperyment(parametry):
    print("\n[INFO] Wczytywanie danych...")
    data = dr.read_data_from_file(parametry['plik_danych'])
    if not data: return

    wyniki_koszt = []
    czasy = []
    
    ILOSC_PROB = 5
    print(f"\n[EKSPERYMENT] Rozpoczynam {ILOSC_PROB} przebiegów dla aktualnych parametrów...")

    for i in range(ILOSC_PROB):
        print(f"  -> Próba {i+1}/{ILOSC_PROB}...", end="", flush=True)
        colony = aco.AntColony(
            num_ants=parametry['ilosc_mrowek'],
            num_iterations=parametry['ilosc_iteracji'],
            Q=parametry['Q'],
            A=parametry['alpha'],
            B=parametry['beta'],
            rho=parametry['rho'],
            p_random=parametry['p_random'],
            data=data
        )
        koszt, trasa, historia, czas = colony.run(verbose=True)
        wyniki_koszt.append(koszt)
        czasy.append(czas)
        print(f" Wynik: {koszt:.2f}, Czas: {czas:.4f}s")

    srednia = np.mean(wyniki_koszt)
    mediana = np.median(wyniki_koszt)
    odchylenie = np.std(wyniki_koszt)
    najlepszy = np.min(wyniki_koszt)
    najgorszy = np.max(wyniki_koszt)

    print("\n" + "="*40)
    print(f" WYNIKI EKSPERYMENTU ({ILOSC_PROB} powtórzeń)")
    print("="*40)
    print(f" Parametry: alpha={parametry['alpha']}, beta={parametry['beta']}, rho={parametry['rho']}, p_rand={parametry['p_random']}")
    print("-" * 40)
    print(f" Średnia długość trasy:   {srednia:.2f}")
    print(f" Mediana:                 {mediana:.2f}")
    print(f" Odchylenie std:          {odchylenie:.2f}")
    print(f" Najlepszy wynik (min):   {najlepszy:.2f}")
    print(f" Najgorszy wynik (max):   {najgorszy:.2f}")
    print(f" Średni czas wykonania:   {np.mean(czasy):.4f} s")
    print("="*40)

def main():
    parametry_aco = {
        'plik_danych': 'A-n32-k5.txt', 
        'ilosc_mrowek': 50,
        'ilosc_iteracji': 100,
        'alpha': 1.0,
        'beta': 5.0,
        'rho': 0.9,
        'Q': 100.0,
        'p_random': 0.01 
    }

    while True:
        wyczysc_ekran()
        print("=" * 45)
        print("     GŁÓWNE MENU SYMULATORA ACO (Wesołe Miasteczko)")
        print("=" * 45)
        
        wyswietl_aktualne_parametry(parametry_aco)

        print("\nOpcje:")
        print("  1. Zmień ustawienia algorytmu")
        print("  2. Uruchom POJEDYNCZO (z wykresem)")
        print("  3. Uruchom EKSPERYMENT (5 powtórzeń + statystyki)")
        print("  0. Wyjdź z programu")
        print("-" * 45)
        
        wybor_glowny = input("Wybierz opcję: ")

        if wybor_glowny == '1':
            parametry_aco = menu_zmiany_danych(parametry_aco)
            
        elif wybor_glowny == '2':
            wyczysc_ekran() 
            uruchom_pojedynczy_program(parametry_aco)
            input("\nWciśnij Enter, aby wrócić...")
            
        elif wybor_glowny == '3':
            wyczysc_ekran()
            uruchom_eksperyment(parametry_aco)
            input("\nWciśnij Enter, aby wrócić...")

        elif wybor_glowny == '0':
            break 
            
        else:
            print("\n[BŁĄD] Nieprawidłowa opcja.")
            time.sleep(1)

if __name__ == "__main__":
    main()