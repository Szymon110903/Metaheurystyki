import matplotlib.pyplot as plt
import numpy as np
from adjustText import adjust_text
import math

def plot_results(func, x_min, x_max, history_points, title="Przebieg algorytmu Symulowanego Wyżarzania"):
    """
    Rysuje wykres funkcji celu oraz historię znajdowania najlepszych punktów.
    :param func: Funkcja celu (ta sama, co optymalizowana)
    :param x_min: Dolna granica dziedziny
    :param x_max: Górna granica dziedziny
    :param history_points: Lista krotek (indeks, x, f(x)) zwrócona przez sa.solve()
    :param title: Tytuł wykresu (opcjonalny)
    """
    
    # 1. Przygotuj dane z historii (potrzebujemy x_hist najpierw)
    x_hist = [p[1] for p in history_points]
    y_hist = [p[2] for p in history_points]
    indices = [p[0] for p in history_points]

    # 2. Przygotuj dane do wykresu funkcji
    # Generujemy bazowe punkty
    x_linspace = np.linspace(x_min, x_max, 1000000)
    
    # --- KLUCZOWA ZMIANA ---
    # Łączymy punkty bazowe z punktami znalezionymi przez algorytm,
    # aby mieć pewność, że wykres przejdzie przez wszystkie znalezione maksima.
    combined_x = np.concatenate((x_linspace, x_hist))
    
    # Sortujemy i usuwamy duplikaty, aby linia była ciągła
    x_values = np.unique(combined_x)
    # --- KONIEC ZMIANY ---

    # Obliczamy y dla *nowego*, pełnego zestawu punktów x
    vect_func = np.vectorize(func)
    y_values = vect_func(x_values)
    
    # 3. Rysuj wykres
    plt.figure(figsize=(12, 7))
    ax = plt.gca() 
    
    # Wykres funkcji celu
    # Teraz ta linia gwarantowanie przejdzie przez wszystkie punkty z historii
    ax.plot(x_values, y_values, label="Funkcja celu f(x)", color='blue', zorder=1)
    
    # Punkty z historii (rysowane na wierzchu)
    ax.scatter(x_hist, y_hist, color='red', s=50, zorder=2, label="Kolejne najlepsze maksima (f_best)")
    
    # 4. Dodawanie adnotacji (etykiet) za pomocą adjustText
    texts = []
    for i, x, y in zip(indices, x_hist, y_hist):
        texts.append(ax.text(x, y, str(i), 
                             color='black', 
                             fontsize=9,
                             ha='center', 
                             va='center'))
    
    adjust_text(texts, 
                ax=ax,
                force_points=(0.2, 0.5),
                force_text=(0.2, 0.5),
                arrowprops=dict(arrowstyle='-', color='gray', lw=0.5, alpha=0.7))
    
    # 5. Ustawienia końcowe wykresu
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.grid(True)
    plt.show()