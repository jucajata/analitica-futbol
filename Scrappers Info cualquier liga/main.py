# Imports
import os
from league_matches_scraper import league_matches_scraper
from average_stats_calculator import average_stats_calculator
from upcoming_matches_scraper import upcoming_matches_scraper


def main(pais, liga, cant_omitir):
    # Lectura de parámetros
    print("ESTOY EN EL MAIN ANTIGUO")
    link_liga = "https://www.flashscore.co/futbol/{}/{}/".format(pais, liga)

    # Lectura de versión
    version = 0

    # Especificación de la ruta con los datos
    if not os.path.exists(f'data/{pais}_{liga}'):
        os.mkdir(os.path.abspath(os.getcwd()).replace("\\", "/") + "/" + f'data/{pais}_{liga}')

    path = f'data/{pais}_{liga}/version{version}'
    if not os.path.exists(path):
        os.mkdir(os.path.abspath(os.getcwd()).replace("\\", "/") + "/" + path)

    # Ejecución del programa
    print("-------------------- Parte 1 de 3 --------------------")
    print("Recolectando estadísticas anteriores")
    print()
    league_matches_scraper(link_liga + "resultados/", path + "/resultados_anteriores.xlsx", cant_omitir)

    print("-------------------- Parte 2 de 3 --------------------")
    print("Calculando estadísticas promedio")
    print()
    average_stats_calculator(path + "/resultados_anteriores.xlsx")

    print("-------------------- Parte 3 de 3 --------------------")
    print("Obteniendo lista de próximos partidos")
    print()
    upcoming_matches_scraper(link_liga + "partidos/", path + "/proximos_partidos.xlsx")


#main("belgica", "jupiler-pro-league", 0)
#main("espana", "laliga", 0)
#main("espana", "laliga-smartbank", 0)
#main("francia", "ligue-1", 0)
#main("francia", "ligue-2", 0)
#main("inglaterra", "championship", 0)
#main("inglaterra", "premier-league", 0)
#main("italia", "serie-a", 0)
#main("italia", "serie-b", 0)
#main("paises-bajos", "eredivisie", 0)
#main("portugal", "liga-portugal", 0)
#main("turquia", "super-lig", 0)
# main("colombia", "primera-a", 0)
main("brasil", "brasileirao-serie-a", 0)
