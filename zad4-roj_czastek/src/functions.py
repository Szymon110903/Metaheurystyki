def booth_function(vector):
    x, y = vector[0], vector[1]
    return (x + 2*y - 7)**2 + (2*x + y - 5)**2

def himmelblaus_function(vector):
    x, y = vector[0], vector[1]
    return (x**2 + y - 11)**2 + (x + y**2 - 7)**2