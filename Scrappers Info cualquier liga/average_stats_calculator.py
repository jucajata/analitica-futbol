import csv
import pandas as pd

# Creacion de diccionarios con totales
estadisticas = ['G', 'P', 'TS', 'SI', 'SO', 'BS', 'FK', 'C', 'OFF', 'TI',
                'GS', 'F', 'RC', 'YC', 'TP', 'PC', 'T', 'A', 'DA']


def average_stats_calculator(db_location):
    data = pd.read_csv(db_location.split(".")[0] + ".csv", sep=',', encoding='utf-8', na_values='-')
    dict_home = {}
    dict_away = {}

    for i in range(len(data)):
        partido = data.loc[i]

        # Local
        name_home_team = data["HomeTeam"][i]
        if name_home_team not in dict_home:
            dict_home[name_home_team] = []

        stats = []
        for j in range(len(estadisticas)):
            stats.append(partido["H" + estadisticas[j]])
        dict_home[name_home_team].append(stats)

        # Visitante
        name_away_team = data["AwayTeam"][i]
        if name_away_team not in dict_away:
            dict_away[name_away_team] = []

        stats = []
        for j in range(len(estadisticas)):
            stats.append(partido["A" + estadisticas[j]])
        dict_away[name_away_team].append(stats)

    # Calculo de promedios por equipo
    # Local
    print("Home:")
    home_averages = {}
    for i in dict_home.keys():
        totals = [0 for _ in range(19)]
        nan_count = [0 for _ in range(19)]
        for j in dict_home[i]:
            for k in range(len(j)):
                if not pd.isna(j[k]):
                    totals[k] += j[k] if k != 1 else int(j[k][:-1])
                elif k != 12 and k != 13:
                    nan_count[k] += 1

        result = []
        print(i, totals)
        for j in range(len(totals)):
            if (len(dict_home[i]) - nan_count[j]) != 0:
                result.append(totals[j] / (len(dict_home[i]) - nan_count[j]))
            else:
                result.append(0)

        home_averages[i] = result

    print(home_averages)
    print()

    # Visitante
    print("Away:")
    away_averages = {}
    for i in dict_away.keys():
        totals = [0 for _ in range(19)]
        nan_count = [0 for _ in range(19)]
        for j in dict_away[i]:
            for k in range(len(j)):
                if not pd.isna(j[k]):
                    totals[k] += j[k] if k != 1 else int(j[k][:-1])
                elif k != 12 and k != 13:
                    nan_count[k] += 1

        result = []
        print(i, totals)
        for j in range(len(totals)):
            if (len(dict_away[i]) - nan_count[j]) != 0:
                result.append(totals[j] / (len(dict_away[i]) - nan_count[j]))
            else:
                result.append(0)

        away_averages[i] = result

    print(away_averages)
    print()

    with open(db_location.split("resultados_anteriores")[0] + "home_averages.csv", 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        for i in home_averages.keys():
            output = home_averages[i]
            output.insert(0, i)
            writer.writerow(output)

    with open(db_location.split("resultados_anteriores")[0] + "away_averages.csv", 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        for i in away_averages.keys():
            output = away_averages[i]
            output.insert(0, i)
            writer.writerow(output)
