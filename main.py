from database import *
from Initial import *
from Friends import *
from BasicsPlayer import *
from GameByPlayers import *
import requests
from datetime import datetime, timedelta
import pandas as pd

#supprimer_table('Riot_Database.db', 'Friends')

#initialize_database() #On  initialise la table Friends (si elle est pas déjà utilisée).

#Hugo = chercher_friend("COYOTE2K", "Hugo", "EUW")
#save_to_database(Hugo)
#Adrien = chercher_friend("DovakynLOL", "Adrien", "EUW")
#save_to_database(Adrien)
#Kelian = chercher_friend("NayZer69", "Kelian", "EUW")
#save_to_database(Kelian)
#Yannis = chercher_friend("yannizer", "Yannis", "EUW")
#save_to_database(Yannis)
#Ryan = chercher_friend("ryanelfa", "Ryan", "EUW")
#save_to_database(Ryan)
#VH = chercher_friend("Omalleyy", "VH", "EUW")
#save_to_database(VH)
#Bodino = chercher_friend("Insidiouv", "Bodino", "EUW")
#save_to_database(Bodino)
#PL = chercher_friend("plo10104", "PL", "EUW")
#save_to_database(PL)
#JO = chercher_friend("JoJoMaster4", "JO", "EUW")
#save_to_database(JO)

# Exemple d'utilisation
#Hugo2 = chercher_friend_lvl("Hugo")
#mettre_a_jour_ligne('Riot_Database.db', 'Friends', {'summonerId': Hugo2['summonerId'], 'summonerLevel': Hugo2['summonerLevel']}, "realName = 'Hugo'")
#Adrien2 = chercher_friend_lvl("Adrien")
#mettre_a_jour_ligne('Riot_Database.db', 'Friends', {'summonerId': Adrien2['summonerId'], 'summonerLevel': Adrien2['summonerLevel']}, "realName = 'Adrien'")
#Kelian2 = chercher_friend_lvl("Kelian")
#mettre_a_jour_ligne('Riot_Database.db', 'Friends', {'summonerId': Kelian2['summonerId'], 'summonerLevel': Kelian2['summonerLevel']}, "realName = 'Kelian'")
#Yannis2 = chercher_friend_lvl("Yannis")
#mettre_a_jour_ligne('Riot_Database.db', 'Friends', {'summonerId': Yannis2['summonerId'], 'summonerLevel': Yannis2['summonerLevel']}, "realName = 'Yannis'")
#Ryan2 = chercher_friend_lvl("Ryan")
#mettre_a_jour_ligne('Riot_Database.db', 'Friends', {'summonerId': Ryan2['summonerId'], 'summonerLevel':Ryan2['summonerLevel']}, "realName = 'Ryan'")
#VH2 = chercher_friend_lvl("VH")
#mettre_a_jour_ligne('Riot_Database.db', 'Friends', {'summonerId': VH2['summonerId'], 'summonerLevel': VH2['summonerLevel']}, "realName = 'VH'")
#Bodino2 = chercher_friend_lvl("Bodino")
#mettre_a_jour_ligne('Riot_Database.db', 'Friends', {'summonerId': Bodino2['summonerId'], 'summonerLevel': Bodino2['summonerLevel']}, "realName = 'Bodino'")
#PL2 = chercher_friend_lvl("PL")
#mettre_a_jour_ligne('Riot_Database.db', 'Friends', {'summonerId': PL2['summonerId'], 'summonerLevel': PL2['summonerLevel']}, "realName = 'PL'")
#initialise_database_basics_player()
#JO2 = chercher_friend_lvl("JO")
#mettre_a_jour_ligne('Riot_Database.db', 'Friends', {'summonerId': JO2['summonerId'], 'summonerLevel': JO2['summonerLevel']}, "realName = 'JO'")
#Mise_a_jour_Basics_Player()
#Mise_a_jour_Game_By_Player()
print(len(fetch_all_game_by_players()))
conn = sqlite3.connect("riot_database.db")
cursor = conn.cursor()
 
# Insérer ou remplacer les données d'un joueur
query = "SELECT realName, AVG(CS), AVG(damagePerMinute) FROM AdvancedPlayer GROUP BY realName ORDER BY AVG(damagePerMinute) DESC;"

# Charger les données dans un DataFrame Pandas
df = pd.read_sql_query(query, conn)

# Afficher le DataFrame (table)
print(df)


query = "SELECT Friends.realName, soloqRank,soloqRatio, summonerLevel FROM BasicsPlayer JOIN Friends ON BasicsPlayer.realName = Friends.realName;"

# Charger les données dans un DataFrame Pandas
df = pd.read_sql_query(query, conn)

# Afficher le DataFrame (table)
print(df)

query = "SELECT AVG(CASE WHEN gold != 0 THEN damagePerMinute / goldPerMinute ELSE 0 END) AS damagepergold, realName FROM AdvancedPlayer GROUP BY realName ORDER BY damagepergold DESC;"
rows = cursor.execute(query)
# Charger les données dans un DataFrame Pandas
df2 = pd.read_sql_query(query, conn)

# Afficher le DataFrame (table)
print(df2)

# Charger les données dans un DataFrame Pandas



    
conn.commit()  # Sauvegarde les modifications
conn.close()