# Imports
import os
import numpy as np
import pandas as pd
from utils import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def league_matches_scraper(link, cant_omitir):
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
    dataFrame_partidos= pd.DataFrame(columns=titulos_estadisticas)
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
            lines_stats.append(home_value)
            lines_stats.append(away_value)

        # DataFrame writting
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

        if not terminar:

            dataframe_act= pd.DataFrame(columns=list(titulos_estadisticas),data=[stats_gen])
            dataFrame_partidos= pd.concat([dataFrame_partidos,dataframe_act])
            
            # Console printing
            completados += 1
            print("Partido " + str(completados) + " de " + str(total) + ":")
            print(datos_local[:-2] + " vs " + datos_visita[:-2])
            print(datos_local[-1:] + " a " + datos_visita[-1:])
            # print(info_stats)
            print()

        index += 1

    # Cerrar el driver del navegador
    browser.quit()
    return dataFrame_partidos
