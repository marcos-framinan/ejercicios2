import csv
from collections import defaultdict
fichero = "la-liga-2025-UTC.csv"
def cargar_Resultados(ruta_csv: str) -> list:
    partidos = []
    print("Carga el fichero:", ruta_csv)

    with open(ruta_csv, newline='', encoding="utf-8") as f:
        lector = csv.DictReader(f)
        i = 0
        for fila in lector:
            i += 1
            partidos.append(fila)

    print("Partidos cargados:", i)
    return partidos


# ---------------------------------------------------------
# (2) Procesar estadísticas de los equipos
# ---------------------------------------------------------
def procesar_estadisticas(partidos):
    equipos = defaultdict(lambda: {
        "GF": 0, "GC": 0,
        "Puntos": 0,
        "DG": 0,
        "FairPlay": 0,
        "Directos": defaultdict(lambda: {"GF": 0, "GC": 0})
    })

    for p in partidos:

        # --- COLUMNAS ADAPTADAS A TU CSV ---
        home = p["Home Team"]
        away = p["Away Team"]

        resultado = p["Result"].strip()     # Ej: "2 - 1"
        if "-" not in resultado or resultado.strip() == "" or resultado.count("-") != 1:
            print("Resultado no válido encontrado:", resultado)
            continue  # saltamos este partido

        gh, ga = map(int, resultado.split('-'))

        # ---- Goles ----
        equipos[home]["GF"] += gh
        equipos[home]["GC"] += ga
        equipos[away]["GF"] += ga
        equipos[away]["GC"] += gh

        equipos[home]["DG"] = equipos[home]["GF"] - equipos[home]["GC"]
        equipos[away]["DG"] = equipos[away]["GF"] - equipos[away]["GC"]

        # ---- Puntos ----
        if gh > ga:
            equipos[home]["Puntos"] += 3
        elif ga > gh:
            equipos[away]["Puntos"] += 3
        else:
            equipos[home]["Puntos"] += 1
            equipos[away]["Puntos"] += 1

        # ⚠️ SIN TARJETAS → Fair Play queda en 0

        # ---- Enfrentamientos directos ----
        equipos[home]["Directos"][away]["GF"] += gh
        equipos[home]["Directos"][away]["GC"] += ga

        equipos[away]["Directos"][home]["GF"] += ga
        equipos[away]["Directos"][home]["GC"] += gh

    return equipos



# ---------------------------------------------------------
# (3) Criterios de desempate EXACTOS DEL ENUNCIADO
# ---------------------------------------------------------
def comparar(e1, e2, equipos):
    # 1. Enfrentamientos directos (DG)
    if e2 in equipos[e1]["Directos"]:
        dg1 = equipos[e1]["Directos"][e2]["GF"] - equipos[e1]["Directos"][e2]["GC"]
        dg2 = equipos[e2]["Directos"][e1]["GF"] - equipos[e2]["Directos"][e1]["GC"]
        if dg1 != dg2:
            return dg2 - dg1  # mayor primero

    # 2. Diferencia de goles general
    if equipos[e1]["DG"] != equipos[e2]["DG"]:
        return equipos[e2]["DG"] - equipos[e1]["DG"]

    # 3. Más goles marcados
    if equipos[e1]["GF"] != equipos[e2]["GF"]:
        return equipos[e2]["GF"] - equipos[e1]["GF"]

    # 4. Fair Play (menos puntos es mejor)
    return equipos[e1]["FairPlay"] - equipos[e2]["FairPlay"]


# ---------------------------------------------------------
# (4) Mostrar clasificación
# ---------------------------------------------------------
def mostrar_clasificacion(equipos):
    from functools import cmp_to_key

    lista = list(equipos.keys())

    # Primero ordenar por puntos
    lista.sort(key=lambda e: -equipos[e]["Puntos"])

    # Luego aplicar criterios avanzados
    lista.sort(key=cmp_to_key(lambda a, b: comparar(a, b, equipos)))

    print("\n=== CLASIFICACIÓN FINAL ===")
    for pos, equipo in enumerate(lista, 1):
        e = equipos[equipo]
        print(f"{pos}. {equipo} - {e['Puntos']} pts | DG: {e['DG']} | GF: {e['GF']} | FP: {e['FairPlay']}")


# ---------------------------------------------------------
# (5) Mostrar goles (apartado a)
# ---------------------------------------------------------
def imprimir_goles(equipos):
    print("\n=== GOLES A FAVOR POR EQUIPO ===")
    for k, v in equipos.items():
        print(f"{k}: {v['GF']} goles")


# ---------------------------------------------------------
# (6) MAIN
# ---------------------------------------------------------
def main():
    partidos = cargar_Resultados(fichero)
    equipos = procesar_estadisticas(partidos)

    imprimir_goles(equipos)
    mostrar_clasificacion(equipos)


if __name__ == "__main__":
    main()
