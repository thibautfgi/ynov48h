import pandas as pd
import re

# Charger le fichier CSV (remplacer par le bon chemin de fichier)
fichier_entree = "/../csv/tweets_v2.csv"
df = pd.read_csv(fichier_entree)

# Liste des comptes ENGIE à surveiller
engie_accounts = ["ENGIEpartFR", "ENGIEpartSAV", "ENGIEgroup", "ENGIEgems"]

# Fonction pour compter les mentions des comptes ENGIE dans un tweet
def compter_mentions(content):
    mentions = {account: content.lower().count('@' + account.lower()) for account in engie_accounts}
    return mentions

# Appliquer la fonction à chaque ligne pour extraire les mentions
df['mentions'] = df['content'].apply(compter_mentions)

# Convertir le dictionnaire de mentions en plusieurs colonnes (une par compte)
mentions_df = pd.json_normalize(df['mentions'])

# Ajouter les mentions dans le dataframe d'origine
df = pd.concat([df, mentions_df], axis=1)

# Calcul du nombre de mentions pour chaque compte
kpi_mentions = mentions_df.sum()

# Affichage du tableau des mentions pour chaque compte ENGIE
print(kpi_mentions)

# Afficher un tableau résumé pour chaque compte
kpi_mentions_table = pd.DataFrame(kpi_mentions).reset_index()
kpi_mentions_table.columns = ['Compte', 'Nombre de Mentions']

# Sauvegarder le tableau dans un fichier CSV
kpi_mentions_table.to_csv("/../csv/kpi_mentions_engie.csv", index=False, encoding="utf-8")

print("Le tableau des mentions a été créé et sauvegardé dans 'kpi_mentions_engie.csv'.")

