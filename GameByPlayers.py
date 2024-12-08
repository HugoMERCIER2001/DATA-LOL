import requests
from database import *
from Initial import API
from datetime import datetime, timedelta
from BasicsPlayer import *

def Mise_a_jour_Game_By_Player():
    conn = sqlite3.connect("Riot_Database.db")
    cursor = conn.cursor()
    rows = fetch_all_BasicsPlayer()
    for i in range(len(rows)):
        puuid = rows[i][0]
        realName = rows[i][2]
        print(realName)
        nbrwinflex = rows[i][5]
        nbrlossflex = rows[i][6]
        nbrwinsoloq = rows[i][10]
        nbrlosssoloq = rows[i][11]
        count = nbrwinflex + nbrlossflex + nbrlosssoloq + nbrwinsoloq
        reponse_ranked = cherche_game_by_player(puuid, count, "ranked")
        for gameId in reponse_ranked:
            ajouter_game_table(gameId, puuid, realName)
    print("mise à jour faite")


def cherche_game_by_player(puuid, count, type):
    if (count >= 100):
        count = 100
    print(puuid, count, type)
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type={type}&count={count}&api_key={API}"
    # Faire la requête GET pour obtenir des informations sur le joueur
    response = requests.get(url)
    # Vérifier si la requête a réussi (code de statut 200)
    if response.status_code == 200:
        data = response.json()  # Récupérer les données de la réponse au format JSON
    else :
        print("Erreur dans la requête pour obtenir les matchs par puuid")
    return data


def ajouter_game_table(gameId, puuid, realName):
        # Connexion à la base de données
    conn = sqlite3.connect("Riot_Database.db")  # Remplacez par votre chemin de base de données
    cursor = conn.cursor()

    # Vérifier si la ligne existe déjà dans la table
    cursor.execute("SELECT * FROM GameByPlayers WHERE gameId = ? AND puuid = ?", (gameId, puuid))
    result = cursor.fetchone()

    if result:
        print("La ligne existe déjà dans la table.")
    else:
        # Si la ligne n'existe pas, insérer une nouvelle ligne
        cursor.execute("INSERT INTO GameByPlayers (gameId, puuid, realName, etude, type) VALUES (?, ?, ?, ?, ?)",
                       (gameId, puuid, realName, 0, 'ranked'))
        conn.commit()
        print("Nouvelle ligne ajoutée à la table.")

    # Fermer la connexion
    conn.close()

def fetch_all_game_by_players():
    conn = sqlite3.connect("Riot_Database.db")
    cursor = conn.cursor()
    
    # Récupérer toutes les données de la table
    cursor.execute("SELECT * FROM GameByPlayers")
    rows = cursor.fetchall()
    
    conn.close()
    return rows