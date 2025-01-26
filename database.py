import Initial #Import du fichier python initial.
import sqlite3

# Fonction pour initialiser la base de données
def initialize_database():
    conn = sqlite3.connect("Riot_Database.db")  # Crée ou ouvre le fichier de la base de données
    cursor = conn.cursor()
    
    # Créer une table Friends pour stocker les informations des joueurs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Friends (
            puuid TEXT PRIMARY KEY,
            gameName TEXT,
            tagLine TEXT,
            realName TEXT DEFAULT "Inconnu",
            summonerId TEXT,
            summonerLevel INT
                )
    """)
    conn.commit()  # Sauvegarde les modifications
    conn.close()

def initialise_database_game_by_players():
    conn = sqlite3.connect("Riot_Database.db")  # Crée ou ouvre le fichier de la base de données
    cursor = conn.cursor()
    
    # Créer une table Friends pour stocker les informations des joueurs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS GameByPlayers (
            realName TEXT,
            puuid TEXT,
            gameId TEXT,
            etude INT,
            type TEXT CHECK (type IN ('ranked')),
            PRIMARY KEY (puuid, gameId))
    """)
    conn.commit()  # Sauvegarde les modifications
    conn.close()

def initialise_database_basics_player():
    conn = sqlite3.connect("Riot_Database.db")  # Crée ou ouvre le fichier de la base de données
    cursor = conn.cursor()
    
    # Créer une table Friends pour stocker les informations des joueurs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS BasicsPlayer (
            puuid TEXT PRIMARY KEY,
            summonerId TEXT,
            realName TEXT DEFAULT "Inconnu",
            flexRank TEXT,
            flexLeaguePoint INT,
            flexNbrWin INT,
            flexNbrLoss INT,
            flexRatio FLOAT,
            soloqRank TEXT,
            soloqLeaguePoint INT,
            soloqNbrWin INT,
            soloqNbrLoss INT,
            soloqRatio FLOAT,
            date TIMESTAMP
                )
    """)
    conn.commit()  # Sauvegarde les modifications
    conn.close()

def initialise_database_advanced_player():
    conn = sqlite3.connect("Riot_Database.db")  # Crée ou ouvre le fichier de la base de données
    cursor = conn.cursor()
    
    # Créer une table Friends pour stocker les informations des joueurs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS AdvancedPlayer (
            puuid TEXT,
            gameId TEXT,
            realName TEXT,
            result INT,
            allies TEXT,
            ennemies TEXT,
            lane TEXT,
            championName TEXT,
            nbrKill INT,
            nbrDeath INT,
            nbrAssist INT,
            KDA FLOAT,
            CS INT,
            gold INT,
            goldPerMinute FLOAT,
            turretTaken INT,
            damageDealt INT,
            damagePerMinute FLOAT,
            damageTaken INT,
            visionScore INT,
            visionScorePerMinute FLOAT,       
            PRIMARY KEY (puuid, gameId))
    """)
    conn.commit()  # Sauvegarde les modifications
    conn.close()

# Fonction pour INSERER DES DONNEES dans la table Friend
def save_to_database(playerData): #player_data doit être une liste qui contient la clé "id", la clé "name", la clé "summonerLevel"
    conn = sqlite3.connect("riot_database.db")
    cursor = conn.cursor()

    if type(playerData) != int:

        # Insérer ou remplacer les données d'un joueur
        cursor.execute("""
            INSERT OR REPLACE INTO friends (puuid, gameName, tagLine, realName)
            VALUES (?, ?, ?, ?)
        """, (playerData["puuid"], playerData["gameName"], playerData["tagLine"], playerData["realName"]))

    conn.commit()  # Sauvegarde les modifications
    conn.close()



# Fonction pour RECUPERER TOUTES LES DONNEES
def fetch_all_friends():
    conn = sqlite3.connect("Riot_Database.db")
    cursor = conn.cursor()
    
    # Récupérer toutes les données de la table
    cursor.execute("SELECT * FROM Friends")
    rows = cursor.fetchall()
    
    conn.close()
    return rows

#Fonction pour SUPPRIMER UNE TABLE de la base de données
def supprimer_table(db_name, table_name):
    """
    Fonction pour supprimer une table d'une base de données SQLite.

    :param db_name: Le nom du fichier de la base de données SQLite.
    :param table_name: Le nom de la table à supprimer.
    """
    try:
        # Se connecter à la base de données
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Créer la requête SQL pour supprimer la table
        sql = f"DROP TABLE IF EXISTS {table_name}"

        # Exécuter la requête
        cursor.execute(sql)

        # Committer les changements et fermer la connexion
        conn.commit()

        print(f"La table '{table_name}' a été supprimée avec succès.")
    
    except sqlite3.Error as e:
        print(f"Erreur lors de la suppression de la table: {e}")
    
    finally:
        # Fermer la connexion à la base de données
        conn.close()


#Fonction pour SUPPRIMER UNE LIGNE de la table
def supprimer_ligne(db_name, table_name, condition):
    """
    Fonction pour supprimer une ligne d'une table d'une base de données SQLite.

    :param db_name: Le nom du fichier de la base de données SQLite.
    :param table_name: Le nom de la table où la ligne sera supprimée.
    :param condition: La condition qui spécifie la ligne à supprimer.
    """
    try:
        # Se connecter à la base de données
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Créer la requête SQL pour supprimer une ligne en fonction de la condition
        sql = f"DELETE FROM {table_name} WHERE {condition}"

        # Exécuter la requête
        cursor.execute(sql)

        # Committer les changements et fermer la connexion
        conn.commit()

        print(f"La ligne a été supprimée de la table '{table_name}' avec succès.")
    
    except sqlite3.Error as e:
        print(f"Erreur lors de la suppression de la ligne: {e}")
    
    finally:
        # Fermer la connexion à la base de données
        conn.close()

import sqlite3

def ajouter_colonne(db_name, table_name, colonne_name, colonne_type, valeur_par_defaut = None):
    try:
        # Se connecter à la base de donnée
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Créer la requête SQL pour ajouter une colonne
        if valeur_par_defaut is not None:
            sql = f"ALTER TABLE {table_name} ADD COLUMN {colonne_name} {colonne_type} DEFAULT {valeur_par_defaut}"
        else:
            sql = f"ALTER TABLE {table_name} ADD COLUMN {colonne_name} {colonne_type}"

        # Exécuter la requête
        cursor.execute(sql)

        # Committer les changements et fermer la connexion
        conn.commit()
        print(f"Colonne '{colonne_name}' ajoutée à la table '{table_name}' avec succès.")
    
    except sqlite3.Error as e:
        print(f"Erreur lors de l'ajout de la colonne: {e}")
    
    finally:
        # Fermer la connexion à la base de données
        conn.close()


def mettre_a_jour_ligne(db_name, table_name, valeurs, condition):
    """
    Fonction pour mettre à jour une ligne dans une table SQLite.

    :param db_name: Le nom du fichier de la base de données SQLite.
    :param table_name: Le nom de la table où mettre à jour la ligne.
    :param valeurs: Un dictionnaire contenant les colonnes à mettre à jour et leurs nouvelles valeurs.
    :param condition: La condition pour identifier la ligne à mettre à jour.
    """
    try:
        # Se connecter à la base de données
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Préparer la requête SQL pour mettre à jour la ligne
        set_clause = ', '.join([f"{colonne} = ?" for colonne in valeurs.keys()])
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"

        # Exécuter la requête
        cursor.execute(sql, tuple(valeurs.values()))

        # Committer les changements et fermer la connexion
        conn.commit()
        print(f"Ligne mise à jour dans la table '{table_name}' avec succès.")
    
    except sqlite3.Error as e:
        print(f"Erreur lors de la mise à jour de la ligne: {e}")
    
    finally:
        # Fermer la connexion à la base de données
        conn.close()

def rechercher_element(db_name, table_name, colonne_condition, valeur, colonne_cherche="*"):
    """
    Fonction pour rechercher un élément dans une table SQLite.

    :param db_name: Le nom du fichier de la base de données SQLite.
    :param table_name: Le nom de la table où rechercher.
    :param colonne: Le nom de la colonne à filtrer.
    :param valeur: La valeur que tu cherches dans la colonne spécifiée.
    """
    try:
        # Se connecter à la base de données
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Préparer la requête SQL pour rechercher l'élément
        sql = f"SELECT {colonne_cherche} FROM {table_name} WHERE {colonne_condition} = ?"

        # Exécuter la requête
        cursor.execute(sql, (valeur,))

        # Récupérer le résultat
        resultats = cursor.fetchall()

        # Afficher les résultats
        if resultats:
            print(f"Résultats trouvés : {resultats}")
            return resultats
        else:
            print("Aucun résultat trouvé.")

    except sqlite3.Error as e:
        print(f"Erreur lors de la recherche : {e}")
    
    finally:
        # Fermer la connexion à la base de données
        conn.close()

