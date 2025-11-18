iteraciones = 10000
sol = 0.0
for k in range(iteraciones):
    termino = ((-1) ** k) / (2 * k + 1)
    sol += termino

pi_aprox = 4 * sol

print(f"Aproximación de π con {iteraciones} iteraciones: {pi_aprox}")
