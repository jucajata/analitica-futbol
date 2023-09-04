# Imports
from utils import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def upcoming_matches_scraper(link, output_file):
    # Crea un nuevo archivo en excel
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
        if i[12] != "<":
            ids.append(i[4:12])

    # Averages files reading
    home_averages = {}
    with open(output_file.split("proximos_partidos")[0] + "home_averages.csv", encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if len(row) > 0:
                home_averages[row[0]] = row[1:]

    away_averages = {}
    with open(output_file.split("proximos_partidos")[0] + "away_averages.csv", encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if len(row) > 0:
                away_averages[row[0]] = row[1:]

    # Matches
    total = len(ids)
    completados = 0
    for i in ids:
        # Match info retrieving
        soup = ""
        try:
            time.sleep(0.25)
            browser.get("https://www.flashscore.co/partido/" + i + "/#/resumen-del-partido")
            WebDriverWait(browser, timeout_in_seconds).until(
                ec.presence_of_element_located((By.CLASS_NAME, 'participant__participantName')))
            html = browser.page_source
            soup = BeautifulSoup(html, features="html.parser")
        except TimeoutException:
            print("I give up...")

        # Header
        if len(str(soup).split("tournamentHeader__country")) < 2:
            continue
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
            lines_header[7].split(">")[-1])  # Home Team Name
        info_header.append(
            lines_header[15].split(">")[-1])  # Away Team Name
        


        # Stats (averages)
        home_stats = home_averages[info_header[-2]]
        # print(info_header)
        away_stats = away_averages[info_header[-1]]
        info_stats = []
        # print(nom_estadisticas)
        # for j in range(len(nom_estadisticas)):
        #     if j != 0:
        #         info_stats.append([home_stats[j+1], nom_estadisticas[j], away_stats[j+1]])
        #     else:
        #         info_stats.append([home_stats[j+1] + "%", nom_estadisticas[j], away_stats[j+1] + "%"])

        # Escritura del archivo excel
        if len(season.split("/")) > 1:
            nom_hoja = (info_header[0].split("-"))[0] + season.split("/")[0] + season.split("/")[1]
        else:
            nom_hoja = (info_header[0].split("-"))[0] + season.split("/")[0]

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
        stats_gen.append(datos_local)
        stats_gen.append(datos_visita)

        stats_gen.append(float(home_stats[0]))
        stats_gen.append(float(away_stats[0]))

        contador = 0
        for j in info_stats:
            act = j
            if act[1] == nom_estadisticas[contador]:
                stats_gen.append(act[0])
                stats_gen.append(act[2])
                contador = contador + 1
            else:
                dif_index = nom_estadisticas.index(act[1]) - contador
                contador = nom_estadisticas.index(act[1]) + 1

                for k in range(dif_index):
                    stats_gen.append(None)
                    stats_gen.append(None)
                stats_gen.append(act[0])
                stats_gen.append(act[2])

        hoja.append(stats_gen)
        wb.save(output_file)

        # Console printing
        completados += 1
        print("Partido " + str(completados) + " de " + str(total) + ":")
        print(info_header[-2] + " vs " + info_header[-1])
        # print(info_stats)
        print()

    # Elimina la hoja por defecto
    eliminar_hoja_por_defecto(output_file)

    # Cerrar el driver del navegador
    browser.quit()

    # Convierte el archivo excel en un archivo CSV
    convertir_excel_a_csv(output_file)


# "Main"
# with open("./data/linksLigas.txt") as archivo:
#    version_init = 3
#    output_file_init = f'data/data_matches_mismarcadores_half{version_init}.xlsx'
#    for linea in archivo:
#        upcoming_matches_scraper(str(linea).split("resultados")[0] + "partidos/", version_init, output_file_init)
