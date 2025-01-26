from time import sleep

import requests
from database import *
from Initial import API
from datetime import datetime, timedelta
import time

def Mise_a_jour_Advanced_Player():
    conn = sqlite3.connect("Riot_Database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT gameId, puuid, realName FROM GameByPlayers WHERE (etude = 0);")
    rows = cursor.fetchall()
    print(rows)
    nom = rows[0][2]
    i = 0
    for element in rows:
        if element[2] == nom:
            print(f"on fait la {i}ème game de {element[2]}")
            i += 1
        else :
            i = 1
            nom = element[2]
            print(f"on fait la {i}ème game de {element[2]}")
        reponse = None
        while type(reponse) != dict:
            reponse = cherche_stat_advanced_player(element[0], element[1])
            if type(reponse) != dict: time.sleep(60); print("on attend 60 secondes")

        playerData = {
            "gameId" : element[0],
            "puuid" : element[1],
            "realName" : element[2],
            "result" : reponse["result"],
            "allies" : reponse["allies"],
            "ennemies" : reponse["ennemies"],
            "lane" : reponse["lane"],
            "championName" : reponse["championName"],
            "nbrKill" : reponse["nbrKill"],
            "nbrDeath" : reponse["nbrDeath"],
            "nbrAssist" : reponse["nbrAssist"],
            "KDA" : reponse["KDA"],
            "CS" : reponse["CS"],
            "gold" : reponse["gold"],
            "goldPerMinute" : reponse["goldPerMinute"],
            "turretTaken" : reponse["turretTaken"],
            "damageDealt" : reponse["damageDealt"],
            "damagePerMinute" : reponse["damagePerMinute"],
            "damageTaken" : reponse["damageTaken"],
            "visionScore" : reponse["visionScore"],
            "visionScorePerMinute" : reponse["visionScorePerMinute"]
        }
        ajouter_ligne_AdvancedPlayer(playerData)
        etude_devient_1(element[0], element[1])
    print("Nous avons bien tout mis à jour")
        



def cherche_stat_advanced_player(gameId, puuid):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{gameId}?api_key={API}"
    # Faire la requête GET pour obtenir des informations sur le joueur
    response = requests.get(url)
    teamId = 0
    j = -1
    # Vérifier si la requête a réussi (code de statut 200)
    if response.status_code == 200:
        data = response.json()  # Récupérer les données de la réponse au format JSON
        for i in range(0, len(data["info"]["participants"])):
            if(data["info"]["participants"][i]["puuid"] == puuid):
                teamId = data["info"]["participants"][i]["teamId"]
                j = i
        allies = []
        ennemies = []
        for i in range(0, len(data["info"]["participants"])):
            if(data["info"]["participants"][i]["teamId"] == teamId):
                allies += [data["info"]["participants"][i]["riotIdGameName"]]
            else :
                ennemies += [data["info"]["participants"][i]["riotIdGameName"]]
        if(data["info"]["participants"][j]["win"] == False):
            win = 0
        else:
            win = 1
        rate_limit_count = response.headers.get("X-App-Rate-Limit-Count")
        if rate_limit_count:
            # La valeur dans "X-App-Rate-Limit-Count" sera sous la forme "1:1,1:120"
            # Séparer les différentes valeurs
            request_count = rate_limit_count.split(",")[1].split(":")[0] 
            request_count = int(request_count)
        else:
            request_count = 0
        reponse = {
            "nbrRequetesFaites" : request_count,
            "result" : win,
            "allies" : f"{allies}",
            "ennemies" : f"{ennemies}",
            "lane" : data["info"]["participants"][j]["teamPosition"],
            "championName" : data["info"]["participants"][j]["championName"], 
            "nbrKill" : data["info"]["participants"][j]["kills"],
            "nbrDeath" : data["info"]["participants"][j]["deaths"],
            "nbrAssist" : data["info"]["participants"][j]["assists"],
            "KDA" : data["info"]["participants"][j]["challenges"]["kda"],
            "CS" : data["info"]["participants"][j]["totalMinionsKilled"],
            "gold" : data["info"]["participants"][j]["goldEarned"],
            "goldPerMinute" : data["info"]["participants"][j]["challenges"]["goldPerMinute"],
            "turretTaken" : data["info"]["participants"][j]["turretTakedowns"],
            "damageDealt" : data["info"]["participants"][j]["totalDamageDealtToChampions"],
            "damagePerMinute" : data["info"]["participants"][j]["challenges"]["damagePerMinute"],
            "damageTaken" : data["info"]["participants"][j]["totalDamageTaken"],
            "visionScore" : data["info"]["participants"][j]["visionScore"],
            "visionScorePerMinute" : data["info"]["participants"][j]["challenges"]["visionScorePerMinute"]
        }

        #    print(i)
    else :
        print("Erreur dans la requête pour obtenir les matchs par puuid")
        reponse = "None"
    return reponse


def ajouter_ligne_AdvancedPlayer(playerData):
    conn = sqlite3.connect("Riot_Database.db")
    cursor = conn.cursor()
    
    # Insérer ou remplacer les données d"un joueur
    cursor.execute("""
        INSERT OR REPLACE INTO AdvancedPlayer (gameId, puuid, realName, result, allies, ennemies, lane, championName, nbrKill, nbrDeath, nbrAssist, KDA, CS, gold, goldPerMinute, turretTaken, damageDealt, damagePerMinute, damageTaken, visionScore, visionScorePerMinute)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (playerData["gameId"], playerData["puuid"], playerData["realName"], playerData["result"], playerData["allies"], playerData["ennemies"], playerData["lane"], playerData["championName"], playerData["nbrKill"], playerData["nbrDeath"], playerData["nbrAssist"], playerData["KDA"], playerData["CS"], playerData["gold"], playerData["goldPerMinute"], playerData["turretTaken"], playerData["damageDealt"], playerData["damagePerMinute"], playerData["damageTaken"], playerData["visionScore"], playerData["visionScorePerMinute"]))
    conn.commit()  # Sauvegarde les modifications
    conn.close()

def etude_devient_1(gameId, puuid):
    conn = sqlite3.connect("Riot_Database.db")
    cursor = conn.cursor()
    sql = f"UPDATE GameByPlayers SET etude = 1  WHERE (gameId = '{gameId}' AND puuid = '{puuid}')"
        # Insérer ou remplacer les données d"un joueur
    cursor.execute(sql)
    conn.commit()  # Sauvegarde les modifications
    conn.close()
