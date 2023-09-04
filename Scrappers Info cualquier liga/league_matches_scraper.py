# Imports
import os
import pandas as pd
from utils import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def league_matches_scraper(link, output_file, cant_omitir):
    file_exists = os.path.exists(output_file)
    previous_data = {}
    first_value = {}
    # if file_exists:
    #     previous_data = pd.read_csv(output_file.split(".")[0] + ".csv", sep=';', encoding='utf-8', na_values='-')
    #     first_value = previous_data.iloc[0]

    # Se crea un archivo nuevo
    create_file(output_file)

    # Configuracion del WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options, executable_path='driver/chromedriver.exe')
    timeout_in_seconds = 10

    # Obtiene el html con la lista de partidos
    soup = obtener_lista_partidos(browser, link)

    # Data formatting: extract matches ID
    season = ((str(soup).split("sportName soccer")[0]).split(" class=\"heading__info\">")[1]).split("</div>")[0]
    data = str(soup).split("sportName soccer")[1]
    data = data.split("notificationsDialog")[0]
    lines = data.split("id=\"")

    ids = []
    for i in lines[1:]:
        ids.append(i[4:12])

    # Matches
    total = len(ids)
    completados = 0
    terminar = False
    index = 0

    total -= cant_omitir
    # while (index < len(ids[:-cant_omitir])) and (not terminar):  # Temporada corta (ej: Colombia)
    while (index < len(ids)) and (not terminar):  # Temporada larga
        i = ids[index]

        # Match info retrieving
        try:
            time.sleep(0.25)
            browser.get("https://www.flashscore.co/partido/" + i + "/#/resumen-del-partido/estadisticas-del-partido/0")
            WebDriverWait(browser, timeout_in_seconds).until(
                ec.presence_of_element_located((By.CLASS_NAME, 'stat__worseSideOrEqualBackground')))
            html = browser.page_source
            soup = BeautifulSoup(html, features="html.parser")
        except TimeoutException:
            completados += 1
            print("Partido " + str(completados) + " de " + str(total) + ":")
            print("No se disputó")
            print()
            index += 1
            continue

        # Header
        header = str(soup).split("tournamentHeader__country")[1]
        header = header.split("Enfrentamientos H2H")[0]
        temp = header.split("</")
        lines_header = []
        for j in temp:
            if len(j) >= 6:
                lines_header.append(j)

        info_header = []
        info_header.append(lines_header[0].split(">")[-1])  # League Round
        info_header.append(lines_header[1].split(">")[-1])  # Date
        info_header.append(
            lines_header[7].split(">")[-1] + " " + lines_header[8].split(">")[-1])  # Home Team Name and Goals
        info_header.append(
            lines_header[17].split(">")[-1] + " " + lines_header[10].split(">")[-1])  # Away Team Name and Goals
        
        # print(info_header)
        # Stats
        stats = browser.find_elements(By.CLASS_NAME,"stat__row")
        # print(stats)
        lines_stats = []
        info_stats=[]
        for j in stats:
            home_value=j.find_element(By.CLASS_NAME,"stat__homeValue").get_attribute("textContent")
            away_value=j.find_element(By.CLASS_NAME,"stat__awayValue").get_attribute("textContent")
            nombre_stat_act= j.find_element(By.CLASS_NAME,"stat__categoryName").get_attribute("textContent")
            info_stats.append(nombre_stat_act)
            # print(home_value,away_value,nombre_stat_act)
            lines_stats.append(home_value)
            lines_stats.append(away_value)
            # print(j.get_attribute("textContent"))
            # if len(j) >= 6:
                # lines_stats.append(j)

        # info_stats = []
        # should_skip = True
        # first_line = 11 if lines_stats[6].__contains__("xG") else 3
        # for j in range(first_line, len(lines_stats) - 5, 5):
        #     if lines_stats[j + 1].split(">")[-1] in nom_estadisticas:
        #         info_stats.append(
        #             [lines_stats[j].split(">")[-1], lines_stats[j + 1].split(">")[-1],
        #              lines_stats[j + 2].split(">")[-1]])
        #         should_skip = False

        # if should_skip:
        #     completados += 1
        #     print("Partido " + str(completados) + " de " + str(total) + ":")
        #     print("No se disputó")
        #     print()
        #     index += 1
        #     continue

        # Escritura del archivo excel
        nom_hoja = (info_header[0].split("-"))[0] + season.split("/")[0]
        if len(season.split("/")) > 1:
            nom_hoja += season.split("/")[1]

        wb = openpyxl.load_workbook(output_file)
        existe_hoja = False

        for hoja_w in wb:
            if nom_hoja == hoja_w.title:
                existe_hoja = True

        if existe_hoja:
            hoja = wb[nom_hoja]
            wb.active = hoja

        else:
            hoja = wb.create_sheet(nom_hoja)
            wb.active = hoja

            # Crea la fila del encabezado con los títulos
            hoja.append(titulos_estadisticas)

        # File writting
        stats_gen = []
        stats_gen.append(info_header[1])
        datos_local = info_header[2]
        datos_visita = info_header[3]
        stats_gen.append(datos_local[:-2].strip())
        stats_gen.append(datos_visita[:-2].strip())
        stats_gen.append(datos_local[-2:].strip())
        stats_gen.append(datos_visita[-2:].strip())

        contador = 0
        cont_est = 0
        for j in info_stats:
            act = j
            # print(nom_estadisticas[contador], act)
            if nom_estadisticas[contador] in act:
                stats_gen.append(lines_stats[cont_est])
                stats_gen.append(lines_stats[cont_est+1])
                cont_est = cont_est + 2
                contador = contador + 1
                
            else:
                dif_index = nom_estadisticas.index(act) - contador
                contador = nom_estadisticas.index(act) + 1

                for k in range(dif_index):
                    stats_gen.append(None)
                    stats_gen.append(None)
                stats_gen.append(lines_stats[cont_est])
                stats_gen.append(lines_stats[cont_est+1])
                cont_est = cont_est + 2

        stats_gen.append(int(datos_local[-2:]) - int(datos_visita[-2:]))  # Resultado

        # if file_exists and (first_value["Date"] == stats_gen[0]) and (
        #         first_value["HomeTeam"] == stats_gen[1]) and (
        #         first_value["AwayTeam"] == stats_gen[2]):
        #     print("Datos anteriores encontrados. Actualizando archivo")
        #     print()
        #     for i in range(len(previous_data)):
        #         hoja.append(previous_data.iloc[i].tolist())
        #         wb.save(output_file)
        #     terminar = True

        if not terminar:
            hoja.append(stats_gen)
            wb.save(output_file)

            # Console printing
            completados += 1
            print("Partido " + str(completados) + " de " + str(total) + ":")
            print(datos_local[:-2] + " vs " + datos_visita[:-2])
            print(datos_local[-1:] + " a " + datos_visita[-1:])
            print(info_stats)
            print()

        index += 1

    # Elimina la hoja por defecto
    eliminar_hoja_por_defecto(output_file)

    # Cerrar el driver del navegador
    browser.quit()

    # Convierte el archivo excel en un archivo CSV
    convertir_excel_a_csv(output_file)

# "Main"
# with open("./data/linksLigas.txt") as archivo:
#    version_init = 0
#    output_file_init = f'data/data_matches_mismarcadores_half{version_init}.xlsx'
#    for linea in archivo:
#        league_matches_scraper(linea, output_file_init)
