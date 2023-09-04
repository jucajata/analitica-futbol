# Imports
import datetime
from league_matches_scraper_dataframes import * 
from league_matches_scraper_fbref_dataframes import *

def unir_datos_fbref(diccionario_dfs_fbref):
    stats_summary =diccionario_dfs_fbref['stats_summary'].copy()
    stats_summary['Jugador'] = stats_summary['Jugador'].apply(quitar_espacios)
    fecha = stats_summary['Fecha'].apply(parse_fecha_espanol)
    stats_summary['Fecha'] = fecha
    jugadores_por_partido= stats_summary[['Fecha','Jugador']].groupby(['Fecha',"Jugador"]).sum().reset_index()
    nombres_hoja_partidos=["stats_summary","stats_keeper","stats_passing","stats_passing_types","stats_defense","stats_possession","stats_misc"]
    for hoja in nombres_hoja_partidos:
        if hoja== "stats_summary":
            diccionario_dfs_fbref[hoja] = diccionario_dfs_fbref[hoja].rename({"Gls.": "Goles Anotados S","Ass":"Asistencias S","TP":"Tiros Penales Ejecutado Ss"
                                            ,"TPint":"Tiros Penales Intentados S","Dis":"Total disparos S","DaP":"Disparos a puerta S",
                                        "TA":"Tarjetas Amarillas S","TR":"Tarjetas Rojas S","Tkl":"Barridas S","Int":"Intercepciones S",
                                        "Cmp":"Pases Completados S","Int.":"Pases Intentados S","% Cmp":"% de pase completo","PrgP":"Pases Progresivos S",
                                            "PrgC":"Acarreos progresivos S","Att":"Regates intentados S","Succ":"Regates exitosos S","Bloqueos":"Bloqueos S","Toques":"Toques S"},axis="columns")
        elif hoja== "stats_keeper":
            diccionario_dfs_fbref[hoja] = diccionario_dfs_fbref[hoja].rename({"DaPC": "Disparos a puerta en contra GK","GC":"Goles en contra GK","Cmp":"Pases completados (Iniciado) GK"
                                            ,"Int.":"Pases intentados (Iniciado) GK","% Cmp":"% Pases completados (Iniciado) GK","Int..1":"Pases intentados GK",
                                        "TI":"Tiros Intentados GK","%deLanzamientos":"Porcentaje de de pases que fueron realizados GK","Long. prom.":"Promedio de longitud del pase GK",
                                            "Int..2":"Saques de meta GK","%deLanzamientos.1":"Porcentaje de saques de meta realizados GK","Long. prom..1":"Longitud promedio de los saques de meta GK",
                                        "Opp":"Pases superados GK","Stp":"Cruces detenidos GK","% de Stp":"% de cruces detenidos GK","Núm. de OPA":"Número de acciones defensivas fuera del área penal GK",
                                            "DistProm.":"Distancia promedio de las acciones defensivoas GK"},axis="columns")
        elif hoja== "stats_passing":
            diccionario_dfs_fbref[hoja] = diccionario_dfs_fbref[hoja].rename({"Cmp": "Pases completados P","Int.":"Pases intentados P","% Cmp":"Porcentaje de pases completo P",
                                        "Dist. tot.":"Distancia total de pase P","Dist. prg.":"Distancia de paso progresiva P","Cmp.1":"Pases completados (Cortos) P",
                                        "Int..1":"Pases intentados (Cortos) P","% Cmp.1":"Porcentaje de pases completo (Cortos) P","Cmp.2":"Pases completados (Medios) P",
                                        "Int..2":"Pases intentados (Medios) P","% Cmp.2":"Porcentaje de pases completos (Medios) P","Cmp.3":"Pases completados (Largos) P",
                                        "Int..3":"Pases intentados (Largos) P","% Cmp.3":"Porcentaje de pases completos (Largos) P","Ass":"Asistencias P",
                                        "PC":"Pases Clave","1/3":"Pases en el último tercio de la cancha P","PPA":"Pases al área de penalización P","CrAP":"Cruce en el área de penalización P",
                                        "PrgP":"Pases progresivos P"},axis="columns")
        elif hoja== "stats_passing_types":
            diccionario_dfs_fbref[hoja] = diccionario_dfs_fbref[hoja].rename({"Int.":"Pases intentados PT","Balón vivo":"Pases de balón vivo PT","Balón Muerto":"Pases de balón muerto PT",
                                        "FK":"Pases de tiros libres PT","PL":"Pases Largos PT","Camb.":"Pases de cambio de frente PT","Pcz":"Pases cruzados PT",
                                        "Lanz.":"Lanzamientos realizados PT","SE":"Saques de esquina PT","Dentro":"Saques de esquina hacia adentro PT","Fuera":"Saques de esquina hacia fuera PT",
                                        "Rect.":"Saques de esquina rectos","Cmp":"Pases completados PT","PA":"Pases fuera de juego PT","Bloqueos":"Pases bloqueados PT"},axis="columns")
        elif hoja== "stats_defense":
            diccionario_dfs_fbref[hoja] = diccionario_dfs_fbref[hoja].rename({"Tkl":"Barridas D","TklG":"Barridas exitosas D","3.º def.":"Barridas en la defensa D","3.º cent.":"Barridas en el centro D","3.º ataq.":"Barridas en el ataque D",
                                        "Tkl.1":"Número de regateadores barridos D","Att":"Regateos desafiados D","Tkl%":"Porcentaje de regateadores barridos D","Pérdida":"Desafíos perdidos D",
                                        "Bloqueos":"Bloqueos D","Dis":"Disparos bloqueados D","Pases":"Pases bloqueados D","Int":"Intercepciones D",
                                        "Tkl+Int":"Número de jugadores barridos más número de intercepciones  D","Desp.":"Despeje D","Err":"Errores defensivos D"},axis="columns")
        elif hoja== "stats_possession":
            diccionario_dfs_fbref[hoja] = diccionario_dfs_fbref[hoja].rename({"Toques":"Toques PO","Def. pen.":"Toques en el área propia PO","3.º def.":"Toques en la defensa PO","3.º cent.":"Toques en el mediocampo PO",
                                        "3.º ataq.":"Toques en el ataque PO","Ataq. pen.":"Toques en el área penal de ataque PO","Balón vivo":"Toques (Pelota activa) PO",
                                        "Att":"Robos intentados PO","Succ":"Robos exitosos PO","Exitosa%":"% de robos exitosos PO","Tkld":"Número de barridas en un mismo intento de barrida PO",
                                        "Tkld%":"Porcentaje de tiempo barrido por un defensa durante un intento de enfrentamiento PO","Transportes":"Número de controles de balón PO","Dist. tot.":"Distancia totoal de traslados PO",
                                        "Dist. prg.":"Distancia de traslado progresivo PO","PrgC":"Acarreos progresivos PO","1/3":"Traslados en el último tercio PO",
                                        "TAP":"Traslados en el área penal PO","Errores de control":"Errores de control PO","Des":"Pérdidas de balon PO","Rec":"Pases recibidos PO",
                                        "PrgR":"Pases progresivos recibidos PO"},axis="columns")
        elif hoja== "stats_misc":
            diccionario_dfs_fbref[hoja] = diccionario_dfs_fbref[hoja].rename({"TA":"Tarjetas amarillas M","TR":"Tarjetas rojas M","2a amarilla":"2a amarilla M","Fls":"Faltas cometidas M","FR":"Faltas recibidas M","PA":"Posicion adelantada M",
                                        "Pcz":"Pases cruzados M","Int":"Intercepciones M","TklG":"Barridas ganadas M","Penal ejecutado":"Penal ejecutado M", 
                                        "Penal concedido":"Penal concedido M","GC":"Goles en contra M","Recup.":"Recuperación de pelotas M","Ganados":"Duelos Aéreos ganados M", "Perdidos":"Duelos Aéreos perdidos M",
                                        "% de ganados":"Porcentaje de duelos aéreos ganados M"},axis="columns")
    for hoja in nombres_hoja_partidos:
        # print(hoja)
        hoja_actual= diccionario_dfs_fbref[hoja].copy()
        fecha = hoja_actual['Fecha'].apply(parse_fecha_espanol)
        dia_semana = hoja_actual['Fecha'].apply(parse_dia_semana)
        hoja_actual['Fecha'] = fecha
        hoja_actual['dia_semana'] = dia_semana
        hoja_actual['Jugador'] = hoja_actual['Jugador'].apply(quitar_espacios)
        hoja_actual['Equipo'] = hoja_actual['Equipo'].apply(quitar_espacios)
        hoja_actual=hoja_actual.fillna(0).copy()
        # hoja_actual.drop(inplace=True,columns=["Unnamed: 0"])
        if not(hoja =="stats_summary") and  not(hoja =="stats_keeper"):
            hoja_actual.drop(inplace=True,columns=["Equipo","núm.","País","Posc","Edad","Mín","dia_semana"])
        elif hoja =="stats_keeper":
            hoja_actual.drop(inplace=True,columns=["Equipo","País","Edad","Mín","dia_semana"])
            
        jugadores_por_partido=jugadores_por_partido.merge(hoja_actual,on=["Fecha",'Jugador'],how="left").copy()

    return jugadores_por_partido,diccionario_dfs_fbref['stats_shots']
def devolver_dia_semana(dia_semana):

    if dia_semana == "Lunes":
        return 1
    elif dia_semana == "Martes":
        return 2
    elif dia_semana == "Miércoles":
        return 3
    elif dia_semana == "Jueves":
        return 4
    elif dia_semana == "Viernes":
        return 5
    elif dia_semana == "Sábado":
        return 6
    elif dia_semana == "Domingo":
        return 7
    return
def quitar_espacios(entrada):
    return entrada.strip()

def devolver_mes_anio(mes):
    if mes == "Enero":
        return 1
    elif mes == "Febrero":
        return 2
    elif mes == "Marzo":
        return 3
    elif mes == "Abril":
        return 4
    elif mes == "Mayo":
        return 5
    elif mes == "Junio":
        return 6
    elif mes == "Julio":
        return 7
    elif mes == "Agosto":
        return 8
    elif mes == "Septiembre":
        return 9
    elif mes == "Octubre":
        return 10
    elif mes == "Noviembre":
        return 11
    elif mes == "Diciembre":
        return 12
    return

def parse_fecha_espanol(fecha):


    # Borar coma
    datos = fecha.replace(",", "").split()
   
    # Mes
    mes = devolver_mes_anio(datos[1])
    # Número del dia en el año
    num_dia = int(datos[2])
    # Año
    anio = int(datos[3])

    fecha_dt = datetime.datetime(anio, mes, num_dia).date()

    return fecha_dt

def parse_dia_semana(fecha):

    # Borar coma
    datos = fecha.replace(",", "").split()

    # Obtener el día de la semana en número
    dia_semana = devolver_dia_semana(datos[0])

    return int(dia_semana)

def main_dataframes(pais, liga, cant_omitir, link_fbref):
    # Lectura de parámetros
    print("ESTOY EN EL MAIN NUEVO")
    link_liga = "https://www.flashscore.co/futbol/{}/{}/".format(pais, liga)

    # Ejecución del programa
    print("-------------------- Parte 1 de 3 --------------------")
    print("Recolectando estadísticas anteriores")
    print()
    #Dataframe flashcore
    flashcore_info=league_matches_scraper(link_liga + "resultados/", cant_omitir)

    print(flashcore_info)

    print("-------------------- Parte 2 de 3 --------------------")
    print("Recolectando estadísticas fbref")
    print()
    #Colección de Dataframes
    fbref_info=recorrer_toda_una_liga(link_fbref)

    ## Unir datos todo en una misma tabla
    dataframe_final, dataframe_shots= unir_datos_fbref(fbref_info)
    print(dataframe_final)
    print(dataframe_shots)


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
main_dataframes("brasil", "brasileirao-serie-a", 0,"https://fbref.com/es/comps/24/horario/Resultados-y-partidos-en-Serie-A")
