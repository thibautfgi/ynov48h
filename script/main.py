import datetime
import pandas as pd
import numpy as np
import re  # Importation de la bibliothèque pour les expressions régulières

pd.options.display.max_rows = 9999  # Afficher plus de lignes

fichier_entree = "../csv/tweets.csv"  # Remplace par ton fichier
fichier_sortie = "../csv/tweets_v2.csv"

# Liste noire des utilisateurs à supprimer (ajouter les pseudos ici)
blacklist = ["ENGIEpartFR", "ENGIEpartSAV", "ENGIEgroup", "ENGIEgems", "ENGIEnewsroom"]

# Lire le fichier CSV avec précaution
try:
    df = pd.read_csv(fichier_entree, sep=";", encoding="utf-8")
except FileNotFoundError:
    print("Erreur : Le fichier 'tweets.csv' est introuvable.")
except pd.errors.ParserError:
    print("Erreur : Problème de format dans le fichier CSV.")
except Exception as e:
    print(f"Erreur inattendue : {e}")

# Trier les tweets par utilisateur
df = df.sort_values(by=["screen_name"])
identifiant = "screen_name"

# Suppression de la colonne "id"
df = df.drop(columns=["id"])

utilisateurs_ids = {}

# Supprimer les utilisateurs présents dans la blacklist
df = df[~df['screen_name'].isin(blacklist)]

# Fonction pour générer un ID unique par utilisateur
def generer_id_utilisateur(valeur):
    if valeur not in utilisateurs_ids:
        utilisateurs_ids[valeur] = len(utilisateurs_ids) + 1  # ID unique basé sur l'ordre
    return utilisateurs_ids[valeur]

# Appliquer la génération d'ID unique à la colonne "screen_name"
df["id_utilisateur"] = df[identifiant].apply(generer_id_utilisateur)

# Fonction pour extraire les liens d'image
def extraire_images(text):
    # Utilisation de l'expression régulière pour trouver tous les liens https://
    return re.findall(r'https://[^\s]+', str(text))

# Appliquer la fonction d'extraction des images à la colonne "full_text"
df["image"] = df["full_text"].apply(extraire_images)

# Traiter la colonne "created_at" pour en extraire la date, l'heure et le fuseau horaire
split_timezone = df['created_at'].to_string().split('\n')

# Suppression de la colonne "created_at"
df = df.drop(columns=["created_at"])

# Initialisation des nouvelles colonnes
df['date_time'] = None
df['timezone'] = None

for i in range(len(split_timezone)):
    # Découper la date, l'heure et le fuseau horaire
    split_timezone[i] = split_timezone[i].split("+")

    # Extraire la date et l'heure
    split_date_hour = split_timezone[i][0].split(" ")

    # Assigner la date, l'heure et le fuseau horaire
    df.at[i, 'date_time'] = split_date_hour[len(split_date_hour) - 3] + " " + split_date_hour[len(split_date_hour) - 2]
    df.at[i, 'timezone'] = "+" + split_timezone[i][1]

# Renommer les colonnes selon les nouveaux noms
df = df.rename(columns={
    "screen_name": "pseudo_user",
    "name": "description_user",
    "full_text": "content"
})

# Réorganiser les colonnes pour que "id_utilisateur" soit en première position
colonnes = ["id_utilisateur"] + [col for col in df.columns if col != "id_utilisateur"]
df = df[colonnes]

df.dropna(inplace=True)

df['id_utilisateur'] = df['id_utilisateur'].astype(int)
df['date_time'] = pd.to_datetime(df['date_time'])

# Liste des mots-clés critiques
keywords = [
    "délai", "panne", "urgence", "scandale",
    "pas", "jamais", "rien", "problème",
    "erreur", "impossible", "tarifs", "aucune"
]

# Ajouter une colonne booléenne pour chaque mot-clé
for keyword in keywords:
    df[f'contains_{keyword}'] = df['content'].apply(lambda x: keyword in x.lower())

# Sauvegarder le fichier avec les colonnes réorganisées et les nouveaux noms
df.to_csv(fichier_sortie, index=False, encoding="utf-8")

print("Le nouveau fichier 'tweets_v2.csv' a été créé avec succès !")
