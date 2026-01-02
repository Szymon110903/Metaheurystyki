import math

#  pierwszy przykład z rozdziału 3 
def funkcja_przykład3(x):
    if not (-150 <= x <= 150):
        return 0 
    if -105 <= x <= -95:
        return -2 * abs(x + 100) + 10
    elif 95 <= x <= 105:
        return -2.2 * abs(x - 100) + 11
    else:
        # Obszar x in (-95, 95) oraz poza (-105, 105)
        return 0

def funkcja_przykład4(x):
    if not (-1 <= x <= 2):
        return 0
    return x*math.sin(10*math.pi*x) + 1