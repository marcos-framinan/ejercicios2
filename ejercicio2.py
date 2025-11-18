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
try:
    numero = int(input("Introduce un número entero: "))
    sol = doble_factorial(numero)
    print(f"El doble factorial de {numero} es: {sol}")

except ValueError as e:
    print(f"Error: {e}")

except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")