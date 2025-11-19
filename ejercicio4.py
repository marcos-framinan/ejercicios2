import csv
from collections import defaultdict

archivo_csv = "la-liga-2025-UTC.csv"


def cargar_partidos(ruta_archivo: str) -> list:
    lista_partidos = []
    print("Carga el fichero:", ruta_archivo)

    with open(ruta_archivo, newline='', encoding="utf-8") as fichero_csv:
        lector_csv = csv.DictReader(fichero_csv)
        contador = 0

        for registro in lector_csv:
            contador += 1
            lista_partidos.append(registro)

    print("Partidos cargados:", contador)
    return lista_partidos


def generar_estadisticas(lista_partidos):
    datos_equipos = defaultdict(lambda: {
        "GolesAFavor": 0,
        "GolesEnContra": 0,
        "Puntos": 0,
        "DifGoles": 0,
        "FairPlay": 0,
        "DueloDirecto": defaultdict(lambda: {"GF": 0, "GC": 0})
    })

    for partido in lista_partidos:

        local = partido["Home Team"]
        visitante = partido["Away Team"]

        marcador = partido["Result"].strip()
        if "-" not in marcador or marcador.strip() == "" or marcador.count("-") != 1:
            print("Marcador inválido encontrado:", marcador)
            continue

        goles_local, goles_visit = map(int, marcador.split('-'))

        datos_equipos[local]["GolesAFavor"] += goles_local
        datos_equipos[local]["GolesEnContra"] += goles_visit

        datos_equipos[visitante]["GolesAFavor"] += goles_visit
        datos_equipos[visitante]["GolesEnContra"] += goles_local

        datos_equipos[local]["DifGoles"] = datos_equipos[local]["GolesAFavor"] - datos_equipos[local]["GolesEnContra"]
        datos_equipos[visitante]["DifGoles"] = datos_equipos[visitante]["GolesAFavor"] - datos_equipos[visitante]["GolesEnContra"]

        if goles_local > goles_visit:
            datos_equipos[local]["Puntos"] += 3
        elif goles_visit > goles_local:
            datos_equipos[visitante]["Puntos"] += 3
        else:
            datos_equipos[local]["Puntos"] += 1
            datos_equipos[visitante]["Puntos"] += 1

        datos_equipos[local]["DueloDirecto"][visitante]["GF"] += goles_local
        datos_equipos[local]["DueloDirecto"][visitante]["GC"] += goles_visit

        datos_equipos[visitante]["DueloDirecto"][local]["GF"] += goles_visit
        datos_equipos[visitante]["DueloDirecto"][local]["GC"] += goles_local

    return datos_equipos


def criterio_desempate(eq1, eq2, datos_equipos):
    if eq2 in datos_equipos[eq1]["DueloDirecto"]:
        d1 = datos_equipos[eq1]["DueloDirecto"][eq2]["GF"] - datos_equipos[eq1]["DueloDirecto"][eq2]["GC"]
        d2 = datos_equipos[eq2]["DueloDirecto"][eq1]["GF"] - datos_equipos[eq2]["DueloDirecto"][eq1]["GC"]

        if d1 != d2:
            return d2 - d1

    if datos_equipos[eq1]["DifGoles"] != datos_equipos[eq2]["DifGoles"]:
        return datos_equipos[eq2]["DifGoles"] - datos_equipos[eq1]["DifGoles"]

    if datos_equipos[eq1]["GolesAFavor"] != datos_equipos[eq2]["GolesAFavor"]:
        return datos_equipos[eq2]["GolesAFavor"] - datos_equipos[eq1]["GolesAFavor"]

    return datos_equipos[eq1]["FairPlay"] - datos_equipos[eq2]["FairPlay"]


def mostrar_tabla(datos_equipos):
    from functools import cmp_to_key

    equipos_lista = list(datos_equipos.keys())

    equipos_lista.sort(key=lambda eq: -datos_equipos[eq]["Puntos"])
    equipos_lista.sort(key=cmp_to_key(lambda a, b: criterio_desempate(a, b, datos_equipos)))

    print("\n=== CLASIFICACIÓN FINAL ===")
    for posicion, nombre in enumerate(equipos_lista, 1):
        est = datos_equipos[nombre]
        print(f"{posicion}. {nombre} - {est['Puntos']} pts | DG: {est['DifGoles']} | GF: {est['GolesAFavor']} | FP: {est['FairPlay']}")


def listar_goles(datos_equipos):
    print("\n=== GOLES A FAVOR POR EQUIPO ===")
    for equipo, info in datos_equipos.items():
        print(f"{equipo}: {info['GolesAFavor']} goles")


def main():
    lista_partidos = cargar_partidos(archivo_csv)
    datos_equipos = generar_estadisticas(lista_partidos)

    listar_goles(datos_equipos)
    mostrar_tabla(datos_equipos)


if __name__ == "__main__":
    main()