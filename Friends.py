#Ce fichier Python a pour but de faire les requêtes permettant de charger la table friend dans ma base de donnée"
import requests
from Initial import API
from database import *


# Remplace par ta clé API Riot
api_key = API  # Remplace avec ta clé API Riot

def chercher_friend(gamerName, vraiNom, gamerTag):
    # URL de base pour l'API Riot (ici pour League of Legends)
    url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gamerName}/{gamerTag}?api_key={api_key}"
    # Faire la requête GET pour obtenir des informations sur le joueur
    response = requests.get(url)
    # Vérifier si la requête a réussi (code de statut 200)
    if response.status_code == 200:
        data = response.json()  # Récupérer les données de la réponse au format JSON
        print(f"Nom du joueur: {data['gameName']}")
        print(f"ID du joueur: {data['puuid']}")
        print(f"Tag: {data['tagLine']}")
        data = response.json()
        print(data)
        reponse = {
            "puuid": data['puuid'],
            "gameName": gamerName,
            "tagLine": gamerTag,
            "realName": vraiNom
        }
    else:
        print(f"Erreur lors de la requête: {response.status_code}")
        return response.status_code

    return reponse

def chercher_friend_lvl(vraiNom):
    puuid = rechercher_element('Riot_Database.db', 'Friends', 'realName', vraiNom, "puuid")[0][0]
    # URL de base pour l'API Riot (ici pour League of Legends)
    url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={api_key}"
    # Faire la requête GET pour obtenir des informations sur le joueur
    response = requests.get(url)
    # Vérifier si la requête a réussi (code de statut 200)
    if response.status_code == 200:
        data = response.json()  # Récupérer les données de la réponse au format JSON
        data = response.json()
        print(data)
        reponse = {
            "summonerId": data['id'],
            "summonerLevel": data['summonerLevel']
        }
    else:
        print(f"Erreur lors de la requête: {response.status_code}")
        return response.status_code
    return reponse