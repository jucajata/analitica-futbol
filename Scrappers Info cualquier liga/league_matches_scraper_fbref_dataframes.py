# Imports
import os

import pandas as pd
from utils import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time

titulos_estadisticas = [
                    'HomeTeam',
                    'AwayTeam',
                    'HG',  # Home Goals
                    'AG',  # Away Goals
                    'HP',  # Home Possession
                    'AP',  # Away Possession
                    'HTS',  # Home Total Shots
                    'ATS',  # Away Total Shots
                    'HBS',  # Home Blocked Shots
                    'ABS',  # Away Blocked Shots
                    'HC',  # Home Corner Kicks
                    'AC',  # Away Corner Kicks
                    'HOFF',  # Home Offsides
                    'AOFF',  # Away Offsides
                    'HTP',  # Home Total Passes
                    'ATP',  # Away Total Passes
                    'HKP',  # Home Key Passes
                    'AKP',  # Away Key Passes
                    'HAP',  # Home Accurate Passes
                    'AAP',  # Away Accurate Passes
                    'HAC',  # Home Accurate Crosses
                    'AAC',  # Away Accurate Crosses
                    'HALB',  # Home Accurate Long Balls
                    'AALB',  # Away Accurate Long Balls
                    'HT',  # Home Tackles
                    'AT',  # Away Tackles
                    'HT',  # Home Interceptions
                    'AT',  # Away Interceptions
                    'HT',  # Home Clearances
                    'AT',  # Away Clearances
                    'HGS',  # Home Goalkeeper Saves
                    'AGS',  # Away Goalkeeper Saves
                    'Resultado'
]

def league_matches_scraper_fbref(link,datosheader,datospp,num_partidos):
    # output_file=f"./data/pruebas/data_fbref.xlsx"
    # link= 'https://fbref.com/es/partidos/e62f6e78/Crystal-Palace-Arsenal-Agosto-5-2022-Premier-League'
    inicio = time.time()
    # file_exists = os.path.exists(output_file)
    # if not file_exists:
    #     # Se crea un archivo nuevo
    #     create_file(output_file)

    # Configuracion del WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--disable-notifications")
    options.add_argument("--log-level=3")
    browser = webdriver.Chrome(options=options, executable_path='driver/chromedriver.exe')

    try:
        browser.get(link)
    except TimeoutException:
        print("I give up...")

    num_partidos=num_partidos+1
    statsfb= browser.find_element("xpath",'//*[@id="team_stats_extra"]')
    fecha= (browser.find_element("xpath",'//h1[1]').text).split("–")[-1]
    html = statsfb.text
    soup = BeautifulSoup(html, features="html.parser")
    statsfb_pro= str(soup).split("<div id='team_stats_extra'>")[0].split("<div>")[0].split("\n")
    # print(statsfb_pro)
    home= statsfb_pro[0]
    away= statsfb_pro[1]
    statsHome= []
    statsAway = []
    statsMatch = [fecha,home,away]
    for i in range(2,len(statsfb_pro),3):
        statsHome.append(statsfb_pro[i])
        statsMatch.append(statsfb_pro[i])
        statsAway.append(statsfb_pro[i+2])
        statsMatch.append(statsfb_pro[i+2])
    
    statsXG= browser.find_elements("xpath",'//*[@class="score_xg"]')
    haxg=[]
    for i in statsXG:
        html = i.text
        soup = BeautifulSoup(html, features="html.parser")
        haxg.append(str(soup))
    statsHome.append(haxg[0])
    statsMatch.append(haxg[0])
    statsAway.append(haxg[1])
    statsMatch.append(haxg[1])

    # print(statsHome)
    # print(statsAway)
    columnas=['Fecha','HomeTeam','AwayTeam','HF','AF','HC','AC','HPCru','APCru','HTo','ATo','HDerribo','ADerribo','HInter','AInter','HDAG','ADAG','HDespeje','ADespeje'
              ,'HOFF','AOFF','HGK','AGK','HSB','ASB','HPelotazos','APelotazos','HxG','AxG']
    # df_stats_partido=pd.DataFrame(statsMatch, columns=columnas)
    nom_hoja="match_stats"
    datosheader[nom_hoja]=columnas
    datospp[nom_hoja].append(statsMatch)
    # guardar_info_archivo(nom_hoja,output_file,columnas,statsMatch)

    tiempo_guarda_st_partido = time.time() - inicio

    print("Tiempo para guardar la hoja de estadisticas " +str(tiempo_guarda_st_partido))

    # Sacar información de tablas
    tablasPagina= browser.find_elements("xpath",'//div[@class="table_container is_setup"]')
    print("Longitud tablas Pagina:" + str(len(tablasPagina)))
    tablasPagina_nuevo=[]
    #Prueba
    # cont=0
    # for j in tablasPagina:
    #     html = j.text
    #     soup = BeautifulSoup(html, features="html.parser")
    #     print(cont)
    #     print(str(soup))
    #     cont=cont+1
    tablasPagina_nuevo.append(tablasPagina[0])
    tablasPagina_nuevo.append(tablasPagina[1])

    # Sacar información de tablas
    tablasPagina= browser.find_elements("xpath",'//div[@class="table_container tabbed current is_setup"]')
    # print(tablasPagina)
    #Prueba
    for j in tablasPagina:
        tablasPagina_nuevo.append(j)
        # html = j.text
        # soup = BeautifulSoup(html, features="html.parser")
        # print(str(soup))

    for tabla in tablasPagina_nuevo:
        print(tabla.get_attribute("id"))

    tablas_adicionales= ['passing','passing_types','defense','possession','misc']
    id_local=tablasPagina_nuevo[0].get_attribute("id").split("_")[-1]
    id_visitante=tablasPagina_nuevo[1].get_attribute("id").split("_")[-1]
    count=0
    for x in tablasPagina_nuevo:
        headersTable = []
        primeras_etiquetas_columnas={}
        segundas_etiquetas_columnas=['Fecha','Equipo']
        info_filas=[]
        for y in range(1,3):
            headersTable = browser.find_elements("xpath",'//div[@id="{}"][1]/table[1]/thead[1]/tr[{}]/th'.format(x.get_attribute("id"),y))
            for i in headersTable:
                if y == 1:
                    primeras_etiquetas_columnas[i.text]= i.get_attribute("colspan")
                else:
                    segundas_etiquetas_columnas.append(i.text)
        headersTable = browser.find_elements("xpath",'//div[@id="{}"][1]/table[1]/tbody[1]/tr'.format(x.get_attribute("id")))

        id_act=x.get_attribute("id")
        nom_hoja=""
        if ("keeper" in id_act) or ("shots" in id_act):
            nom_hoja= "stats_"+ id_act.split('_')[1]
        else:
            nom_hoja= "stats_"+ id_act.split('_')[-1]
        print("El nombre de la tabla va a ser: "+str(nom_hoja))    
        for y in range(1,len(headersTable)+1):            
            name_player = browser.find_elements("xpath",'//div[@id="{}"][1]/table[1]/tbody[1]/tr[{}]/th'.format(x.get_attribute("id"),y))
            # print(len(name_player))
            tablebody = browser.find_elements("xpath",'//div[@id="{}"][1]/table[1]/tbody[1]/tr[{}]/td'.format(x.get_attribute("id"),y))
            fila=[fecha]
            if id_local in x.get_attribute("id"):
                        fila.append(home)
            elif id_visitante in x.get_attribute("id"):
                        fila.append(away)
            if len(name_player) > 0:
                fila.append(name_player[0].text)
            if len(tablebody) > 0:
                for i in tablebody:
                    fila.append(i.text)
                info_filas.append(fila)
                datospp[nom_hoja].append(fila)
        # print("Tabla "+str(x))
        # print(primeras_etiquetas_columnas)
        # print(segundas_etiquetas_columnas)
        # print(info_filas)
        # df_stats_jugadores=pd.DataFrame(info_filas, columns=segundas_etiquetas_columnas)

        datosheader[nom_hoja]=segundas_etiquetas_columnas
        # guardar_info_archivo(nom_hoja,output_file,segundas_etiquetas_columnas,info_filas)
        count=count+1
    cont=2
    for nom in tablas_adicionales:
        try:
            browser.execute_script("arguments[0].click();",
                                    browser.find_element("xpath",'//div[@data-controls="#switcher_player_stats_{}"]/div[{}]/a[1]'.format(id_local,cont)))
            browser.execute_script("arguments[0].click();",
                                    browser.find_element("xpath",'//div[@data-controls="#switcher_player_stats_{}"]/div[{}]/a[1]'.format(id_visitante,cont)))
        except TimeoutException:
            print("I give up...")

        tablasDinamicas=[browser.find_element("xpath",'//div[@id="div_stats_{}_{}"]'.format(id_local,nom)),
                         browser.find_element("xpath",'//div[@id="div_stats_{}_{}"]'.format(id_visitante,nom))]
        for x in tablasDinamicas:
                inicio_for = time.time() 
                nom_hoja= "stats_"+nom
                headersTable = []
                primeras_etiquetas_columnas={}
                segundas_etiquetas_columnas=["Fecha","Equipo"]
                info_filas=[]
                for y in range(1,3):
                    headersTable = browser.find_elements("xpath",'//div[@id="{}"][1]/table[1]/thead[1]/tr[{}]/th'.format(x.get_attribute("id"),y))
                    for i in headersTable:
                        if y == 1:
                            primeras_etiquetas_columnas[i.text]= i.get_attribute("colspan")
                        else:
                            segundas_etiquetas_columnas.append(i.text)
                headersTable = browser.find_elements("xpath",'//div[@id="{}"][1]/table[1]/tbody[1]/tr'.format(x.get_attribute("id")))

                for y in range(1,len(headersTable)+1):            
                    name_player = browser.find_elements("xpath",'//div[@id="{}"][1]/table[1]/tbody[1]/tr[{}]/th'.format(x.get_attribute("id"),y))
                    # print(len(name_player))
                    tablebody = browser.find_elements("xpath",'//div[@id="{}"][1]/table[1]/tbody[1]/tr[{}]/td'.format(x.get_attribute("id"),y))
                    fila=[fecha]
                    if id_local in x.get_attribute("id"):
                        fila.append(home)
                    elif id_visitante in x.get_attribute("id"):
                        fila.append(away)
                    if len(name_player) > 0:
                        fila.append(name_player[0].text)
                    if len(tablebody) > 0:
                        for i in tablebody:
                            fila.append(i.text)
                        info_filas.append(fila)
                        datospp[nom_hoja].append(fila)
                # print("Tabla "+str(x))
                # print(primeras_etiquetas_columnas)
                # print(segundas_etiquetas_columnas)
                # print(info_filas)
                # df_stats_jugadores=pd.DataFrame(info_filas, columns=segundas_etiquetas_columnas)
            

                tiempo_guarda_st_partido = time.time() - inicio_for

                print("Tiempo para generar los datos de la tabla "+ str(nom_hoja)+" "+str(tiempo_guarda_st_partido))
                datosheader[nom_hoja]=segundas_etiquetas_columnas
                # guardar_info_archivo(nom_hoja,output_file,segundas_etiquetas_columnas,info_filas)
        cont=cont+1
    fin = time.time()
    print("El tiempo en guardar información de este partido fue:")
    print(fin-inicio)
    browser.quit() 
    return (datosheader,datospp,num_partidos)


def guardar_info_archivo(nom_hoja,output_file,titulos_estadisticas,datos):
    # wb = openpyxl.load_workbook(output_file)
    inicio= time.time()
    file_exists = os.path.exists(output_file)
    if not file_exists:
        # Se crea un archivo nuevo
        create_file(output_file)

    # Escritura del archivo excel
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

    for j in datos:
        hoja.append(j)
        wb.save(output_file)
    tiempo_guarda_st_partido = time.time() - inicio

    print("Tiempo para guardar en el excel " +str(tiempo_guarda_st_partido))
    wb.close()


def recorrer_toda_una_liga(link_partidos):

    # Configuracion del WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--disable-notifications")
    options.add_argument("--log-level=3")
    browser = webdriver.Chrome(options=options, executable_path='driver/chromedriver.exe')
    timeout_in_seconds = 10

    try:
        browser.get(link_partidos)
        # browser.execute_script("arguments[0].click();",
        #                         browser.find_element("xpath",'//*[@id="__next"]/div[1]/main[1]/div[1]/div[2]/div[1]/div['
        #                                                         '5]/div[1]/div[1]/div[1]/div[2]'))
    except TimeoutException:
        print("I give up...")

    # prueba= browser.find_element("xpath",'//div[@class="table_container tabbed current is_setup"][1]/table[1]/tbody[1]/tr[@data-row="20"]/td[@data-stat="score"]/a')
    # print(prueba.get_attribute("href"))

    # partidos = browser.find_elements("xpath",'//div[@class="table_container tabbed current is_setup"]/table[1]/tbody[1]/tr')
    # print(len(partidos))
    # lista_links_partidos=[]
    # for partido in partidos:
    #     try:
    #         link_partido= partido.find_element("xpath",'//tr[@data-row="{}"]/td[@data-stat="score"][1]'.format(partido.get_attribute("data-row")))
    #         if (len(link_partido.text) > 0) and (not link_partido.text=="Marcador"):
    #             link_partido_txt= link_partido.find_element("xpath",'//a'.format(partido.get_attribute("data-row")))
    #             lista_links_partidos.append(link_partido_txt.get_attribute("href"))
    #     except:
    #         print("No encontro a la fila"+str(partido.get_attribute("data-row")))
    html = browser.page_source
    soup = BeautifulSoup(html, features="html.parser")
    # print(str(soup).split('<tr data-row="')[5:10])
    lista_links_partidos=[]
    # print(str(soup.find_all(attrs={"data-stat": "match_report"})))
    for link_mod in soup.find_all(attrs={"data-stat": "match_report"}):
        for link_mod_ch in link_mod.find_all("a"):
            if "stathead/matchup/teams" in link_mod_ch.get("href") or link_mod_ch.get("href") == "None":
                continue
            else:
                lista_links_partidos.append("https://fbref.com/"+str(link_mod_ch.get("href")))

    datos_header_partidos={}
    nombres_hoja_partidos=["match_stats","stats_keeper","stats_summary","stats_shots","stats_passing","stats_passing_types","stats_defense","stats_possession","stats_misc"]
    datos_por_partido={}
    for nombre in nombres_hoja_partidos:
        nuevo_array=[]
        datos_por_partido[nombre]=nuevo_array
    num_partidos = 0
    # print(len(lista_links_partidos))
    # print(lista_links_partidos)

    for link in lista_links_partidos[:1]:
        # print(link)
        try:
            retorno=league_matches_scraper_fbref(link,datos_header_partidos,datos_por_partido,num_partidos)
            datos_header_partidos,datos_por_partido,num_partidos = retorno[0],retorno[1],retorno[2] 
            print("Número de partidos scrappeados: "+str(num_partidos))
        except:
            print("No se pudo scrappear correctamente el partido: "+link)
    # print(datos_header_partidos)
    # print(datos_por_partido)
    arreglo_de_dfs={}
    for nombre in nombres_hoja_partidos:
        print(nombre)
        if nombre=="stats_shots":
            datos_header_partidos[nombre] = datos_header_partidos[nombre][:1]+datos_header_partidos[nombre][2:]
            arreglo_de_dfs[nombre]= pd.DataFrame(columns=datos_header_partidos[nombre],data=datos_por_partido[nombre])
        else:
            arreglo_de_dfs[nombre]= pd.DataFrame(columns=datos_header_partidos[nombre],data=datos_por_partido[nombre])
    
    
    
    browser.quit()
    return arreglo_de_dfs


# league_matches_scraper_fbref("","")
# recorrer_toda_una_liga("https://fbref.com/es/comps/11/horario/Resultados-y-partidos-en-Serie-A")