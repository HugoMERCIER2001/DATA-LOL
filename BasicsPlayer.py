import requests
from database import *
from Initial import API
from datetime import datetime, timedelta

def Mise_a_jour_Basics_Player():
    conn = sqlite3.connect("Riot_Database.db")
    cursor = conn.cursor()
    rows = fetch_all_friends()
    current_time = datetime.now()
    print(current_time)
    for i in range(len(rows)):
        summonerId = rows[i][4]
        puuid = rows[i][0]
        realName = rows[i][3]
        cursor.execute("SELECT date FROM BasicsPlayer WHERE summonerId = ?", (summonerId,))
        result = cursor.fetchone()
        if(result):
            saved_datetime = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S.%f")
            if current_time - saved_datetime > timedelta(hours=1):
                print("voici le temps depuis dernière maj : " + f"{current_time - saved_datetime}")
                print(f"Mise à jour de la ligne pour le joueur {realName}")
                reponse = cherche_stat_basics_player(summonerId)
                if(reponse == "None") :
                    playerData = {
                    "summonerId" : summonerId, 
                    "puuid" : puuid,
                    "realName" : realName,
                    "flexRank" : 'None',
                    "flexLeaguePoint" : 0,
                    "flexNbrWin" : 0,
                    "flexNbrLoss" : 0,
                    "flexRatio" : 0,
                    "soloqRank" : 'None',
                    "soloqLeaguePoint" : 0,
                    "soloqNbrWin" : 0,
                    "soloqNbrLoss" : 0,
                    "soloqRatio" : 0,
                    "date" : current_time
                    }
                else :
                    playerData = {
                        "summonerId" : summonerId, 
                        "puuid" : puuid,
                        "realName" : realName,
                        "flexRank" : reponse['flexRank'],
                        "flexLeaguePoint" : reponse['flexLeaguePoint'],
                        "flexNbrWin" : reponse['flexNbrWins'],
                        "flexNbrLoss" : reponse['flexNbrLosses'],
                        "flexRatio" : reponse['flexNbrWins']/(reponse['flexNbrWins'] + reponse['flexNbrLosses']),
                        "soloqRank" : reponse['soloqRank'],
                        "soloqLeaguePoint" : reponse['soloqLeaguePoint'],
                        "soloqNbrWin" : reponse['soloqNbrWins'],
                        "soloqNbrLoss" : reponse['soloqNbrLosses'],
                        "soloqRatio" : reponse['soloqNbrWins']/(reponse['soloqNbrWins'] + reponse['soloqNbrLosses']),
                        "date" : current_time
                    }
                update_to_database_BasicsPlayer(playerData, summonerId)
            else :
                print(f"La dernière maj date de moin de 1h pour le joueur {realName}")
        else :
            print(f"Nouvelle ligne pour le joueur {realName}")
            reponse = cherche_stat_basics_player(summonerId)
            if(reponse == "None") :
                    playerData = {
                    "summonerId" : summonerId, 
                    "puuid" : puuid,
                    "realName" : realName,
                    "flexRank" : 'None',
                    "flexLeaguePoint" : 0,
                    "flexNbrWin" : 0,
                    "flexNbrLoss" : 0,
                    "flexRatio" : 0,
                    "soloqRank" : 'None',
                    "soloqLeaguePoint" : 0,
                    "soloqNbrWin" : 0,
                    "soloqNbrLoss" : 0,
                    "soloqRatio" : 0,
                    "date" : current_time
                    }
            else :
                playerData = {
                    "summonerId" : summonerId, 
                    "puuid" : puuid,
                    "realName" : realName,
                    "flexRank" : reponse['flexRank'],
                    "flexLeaguePoint" : reponse['flexLeaguePoint'],
                    "flexNbrWin" : reponse['flexNbrWins'],
                    "flexNbrLoss" : reponse['flexNbrLosses'],
                    "flexRatio" : reponse['flexNbrWins']/(reponse['flexNbrWins'] + reponse['flexNbrLosses']),
                    "soloqRank" : reponse['soloqRank'],
                    "soloqLeaguePoint" : reponse['soloqLeaguePoint'],
                    "soloqNbrWin" : reponse['soloqNbrWins'],
                    "soloqNbrLoss" : reponse['soloqNbrLosses'],
                    "soloqRatio" : reponse['soloqNbrWins']/(reponse['soloqNbrWins'] + reponse['soloqNbrLosses']),
                    "date" : current_time
                }
            save_to_database_BasicsPlayer(playerData)
    
def cherche_stat_basics_player(summonerId):
    # URL de base pour l'API Riot (ici pour League of Legends)
    url = f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summonerId}?api_key={API}"
    # Faire la requête GET pour obtenir des informations sur le joueur
    response = requests.get(url)
    # Vérifier si la requête a réussi (code de statut 200)
    if response.status_code == 200:
        date_header = response.headers.get('Date')
        data = response.json()  # Récupérer les données de la réponse au format JSON
        if (data == []) :
            reponse = 'None'
        else :
            if(data[0]['queueType'] == "RANKED_FLEX_SR"):
                i = 0
                j = 1
            else :
                i = 1
                j = 0
            reponse = {
                "date" : date_header,
                "summonerId" : summonerId,
                "flexRank" : f"{data[i]['tier']}" + f" {data[i]['rank']}",
                "flexLeaguePoint" : data[i]['leaguePoints'],
                "flexNbrWins" : data[i]['wins'],
                "flexNbrLosses" : data[i]['losses'],
                "soloqRank" : f"{data[j]['tier']}" + f" {data[j]['rank']}",
                "soloqLeaguePoint" : data[j]['leaguePoints'],
                "soloqNbrWins" : data[j]['wins'],
                "soloqNbrLosses" : data[j]['losses']
            }
    else:
        print(f"Erreur lors de la requête: {response.status_code}")
    return reponse

def save_to_database_BasicsPlayer(playerData): #player_data doit être une liste qui contient la clé "id", la clé "name", la clé "summonerLevel"
    conn = sqlite3.connect("Riot_Database.db")
    cursor = conn.cursor()
    
    # Insérer ou remplacer les données d'un joueur
    cursor.execute("""
        INSERT OR REPLACE INTO BasicsPlayer (puuid, summonerId, realName, flexRank, flexLeaguePoint, flexNbrWin, flexNbrLoss, flexRatio, soloqRank, soloqLeaguePoint, soloqNbrWin, soloqNbrLoss, soloqRatio, date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (playerData["puuid"], playerData["summonerId"], playerData["realName"], playerData["flexRank"], playerData["flexLeaguePoint"], playerData["flexNbrWin"], playerData["flexNbrLoss"], playerData["flexRatio"], playerData["soloqRank"], playerData["soloqLeaguePoint"], playerData["soloqNbrWin"], playerData["soloqNbrLoss"], playerData["soloqRatio"], playerData['date']))
    
    conn.commit()  # Sauvegarde les modifications
    conn.close()

def update_to_database_BasicsPlayer(playerData, summonerId):
    mettre_a_jour_ligne("Riot_Database.db", "BasicsPlayer", {"flexRank" : playerData['flexRank'], "flexLeaguePoint" : playerData['flexLeaguePoint'], "flexNbrWin" : playerData['flexNbrWin'], "flexNbrLoss" : playerData['flexNbrLoss'], "flexRatio" : playerData['flexRatio'], "soloqRank" : playerData['soloqRank'], "soloqLeaguePoint" : playerData['soloqLeaguePoint'], "soloqNbrWin" : playerData['soloqNbrWin'], "soloqNbrLoss" : playerData['soloqNbrLoss'], "soloqRatio" : playerData['soloqRatio'], "date" : playerData['date']}, f"summonerId = '{summonerId}'")

def fetch_all_BasicsPlayer():
    conn = sqlite3.connect("Riot_Database.db")
    cursor = conn.cursor()
    
    # Récupérer toutes les données de la table
    cursor.execute("SELECT * FROM BasicsPlayer")
    rows = cursor.fetchall()
    
    conn.close()
    return rows


def convert_to_timestamp(date_str):
    # Définir le format de la date à parser (en tenant compte du jour de la semaine, "Thu")
    date_format = "%a, %d %b %Y %H:%M:%S GMT"
    
    # Convertir la chaîne en objet datetime
    dt_obj = datetime.strptime(date_str, date_format)
    
    # Convertir en format TIMESTAMP (YYYY-MM-DD HH:MM:SS)
    timestamp = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
    
    return timestamp