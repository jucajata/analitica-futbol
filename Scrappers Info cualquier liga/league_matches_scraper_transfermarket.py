# Imports
import os

import pandas as pd
from utils import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time

titulos_estadisticas = (
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
                )

def transfermarket_scrapper_liga(link,datos):
    # output_file=f"./data/pruebas/data_fbref.xlsx"
    # link= 'https://www.transfermarkt.co.uk/premier-league/marktwerte/wettbewerb/GB1/pos//detailpos/0/altersklasse/alle/plus/1'
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

    # num_partidos=num_partidos+1
    for num in range(2,6):
        print("Numero: "+str(num))
        encabezados=0
        filas_tabla=0
        try:
            encabezados= browser.find_elements("xpath",'//*[@class="items"]/thead[1]/tr[1]/th')
            filas_tabla= browser.find_elements("xpath",'//*[@class="items"]/tbody[1]/tr')
        except:
            print("Auxiilio")
            break
        # html = items.text
        # soup = BeautifulSoup(html, features="html.parser")
        # statsfb_pro= str(soup).split("<div id='team_stats_extra'>")[0].split("<div>")[0].split("\n")
        
        # print(filas_tabla)
        for fila in filas_tabla:
            cols= fila.find_elements("xpath","td")
            # print(len(cols))
            # print(cols[0].get_attribute("textContent"))

            # html = cols[1]
            # soup = BeautifulSoup(html, features="html.parser")
            # print(str(soup))


            info_jugador=cols[1].find_element("xpath","table[1]/tbody[1]/tr[1]/td[2]/a")
            nombre_jugador= info_jugador.get_attribute("textContent")
            nacionalidad=cols[2].find_elements(By.TAG_NAME,"img")[0].get_attribute("title")
            edad=cols[3].get_attribute("textContent")

            club=cols[4].find_element("xpath","a[1]/img").get_attribute("title")
            valor_mas_alto=cols[5].find_element(By.TAG_NAME,"span").get_attribute("textContent")
            ultima_actu=cols[6].get_attribute("textContent")
            valor_mercado=cols[7].find_element(By.TAG_NAME,"a").get_attribute("textContent")
            datos.append([nombre_jugador,nacionalidad,edad,club,valor_mas_alto,ultima_actu,valor_mercado])
        try:
            browser.execute_script("arguments[0].click();",
                                    browser.find_element("xpath",'//a[@title="Page {}"]'.format(num)))
            time.sleep(3)
        except:
            print("Auxiilio")
            break
        # print(datos)
    print(len(datos))
    fin = time.time()
    print("El tiempo en guardar información de este partido fue:")
    print(fin-inicio)
    browser.quit() 
    return datos


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

def traer_jugadores_y_guardar_info():
    # league_matches_scraper_fbref("","")
    datos_finales=[]
    for num in range(1,15):
        datos_finales= transfermarket_scrapper_liga("https://www.transfermarkt.co.uk/laliga/marktwerte/wettbewerb/ES1/plus/1/galerie/0?pos=&detailpos={}&altersklasse=alle".format(num),datos_finales)

    encabezados= ['Jugador','Nacionalidad','Edad','Club','Histórico valor mercado máximo','Ultima actualización','Valor actual mercado']
    guardar_info_archivo("Valo Jugadores",f"./data/pruebas/data_valor_jugadores_espana.xlsx",encabezados,datos_finales)


traer_jugadores_y_guardar_info()