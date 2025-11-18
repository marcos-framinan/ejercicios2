def doble_factorial(n):
    "Calcula el doble factorial de n."
    if n < 0:
        raise ValueError("El número no puede ser negativo.")
    if n == 0 or n == 1:
        return 1
    
    sol = 1
    for i in range(n, 0, -2):
        sol *= i
    return sol