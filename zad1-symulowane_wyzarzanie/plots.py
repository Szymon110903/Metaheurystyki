import matplotlib.pyplot as plt
import numpy as np
from adjustText import adjust_text
import math

def plot_results(func, x_min, x_max, history_points, title="Przebieg algorytmu Symulowanego Wyżarzania"):
    """
    Rysuje wykres funkcji celu oraz historię znajdowania najlepszych punktów.
    Gwarantuje, że linia funkcji przechodzi DOKŁADNIE przez punkty z historii.
    
    :param func: Funkcja celu
    :param x_min: Dolna granica dziedziny
    :param x_max: Górna granica dziedziny
    :param history_points: Lista krotek (indeks, x, f(x)) zwrócona przez sa.solve()
    :param title: Tytuł wykresu
    """
    
    x_hist = [p[1] for p in history_points]
    y_hist = [p[2] for p in history_points]
    indices = [p[0] for p in history_points]


    x_values_base = np.linspace(x_min, x_max, 2000)
    
    all_x_base_points = list(x_values_base)
    densify_range = (x_max - x_min) * 0.001
    densify_points_count = 50 

    for x_point_hist in x_hist:
        lower_bound = max(x_min, x_point_hist - densify_range)
        upper_bound = min(x_max, x_point_hist + densify_range)
        if lower_bound != upper_bound:
            all_x_base_points.extend(np.linspace(lower_bound, upper_bound, densify_points_count))

    x_base_unique = np.unique(all_x_base_points)
    
    vect_func = np.vectorize(func)
    y_base_values = vect_func(x_base_unique)
    

    plot_points_dict = {}
    
    for x, y in zip(x_base_unique, y_base_values):
        plot_points_dict[x] = y
        
    for x, y in zip(x_hist, y_hist):
        plot_points_dict[x] = y
        
    sorted_plot_points = sorted(plot_points_dict.items())
    
    x_values_line = [p[0] for p in sorted_plot_points]
    y_values_line = [p[1] for p in sorted_plot_points]
    

    
    plt.figure(figsize=(12, 7))
    ax = plt.gca() 
    
    ax.plot(x_values_line, y_values_line, label="Funkcja celu f(x)", color='blue', zorder=1)
    
    ax.scatter(x_hist, y_hist, color='red', s=50, zorder=2, label="Kolejne najlepsze maksima (f_best)")
    
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
    
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.grid(True)
    plt.show()