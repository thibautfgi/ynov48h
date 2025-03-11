import json
import time

import pandas as pd
from mistralai import Mistral

# Initialisation du client avec votre clé API
client = Mistral(api_key="9T91Y7oBgurTbatkohTNjbvbpPfFla7R")

try:
    # Chargement du fichier CSV
    df = pd.read_csv('../csv/tweets_v2.csv')
    # Afficher les colonnes du DataFrame pour vérifier
    print("Colonnes du DataFrame :", df.columns)
except FileNotFoundError:
    print("Le fichier CSV n'a pas été trouvé.")
    exit(1)

df["satisfaction"] = None
df["sentiment"] = None
df["urgence"] = None
df["mot_clef"] = None
df["categorie"] = None

# Parcours de chaque ligne du DataFrame
for index, row in df.iterrows():
    try:
        # Utiliser la colonne 'content' pour le texte à analyser
        content = df.at[index, 'content']
        content = "Commentaire : " + content

        # Appel de l'API pour obtenir une réponse
        response = client.agents.complete(
            agent_id="ag:587f53c1:20250310:my-agent-48:0274b466",  # Remplacez par l'ID de votre agent
            messages=[{"role": "user", "content": content}],
            response_format = {
                "type": "json_object",
            }
        )

        # Extraction du texte de la réponse
        response_text = response.choices[0].message.content.strip()

        # Affichage de la réponse
        print(f"Réponse pour la ligne {index}: {response_text}")
        df.at[index, "satisfaction"] = json.loads(response_text)["satisfaction"]
        df.at[index, "sentiment"] = json.loads(response_text)["sentiment"]
        df.at[index, "urgence"] = json.loads(response_text)["urgence"]
        df.at[index, "mot_clef"] = json.loads(response_text)["mots clefs"]
        df.at[index, "categorie"] = json.loads(response_text)["catégorie"]
        time.sleep(3.5)
    except Exception as e:
        print(f"Erreur lors du traitement de la ligne {index}: {e}")

df.to_csv("../csv/tweets_v3.csv", index=False, encoding="utf-8")
print("Fichier créer")