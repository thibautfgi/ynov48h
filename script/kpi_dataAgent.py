import pandas as pd
import matplotlib.pyplot as plt
import ast

# Chargement du fichier CSV
df = pd.read_csv('../csv/tweets_v3.csv')

# Sélection des 30 premières lignes
df_30 = df.head(30)

# Convertir les chaînes de listes en listes réelles pour la colonne 'categorie'
df_30['categorie'] = df_30['categorie'].apply(ast.literal_eval)

# Exploser les catégories pour avoir une ligne par catégorie
df_exploded = df_30.explode('categorie')

# Grouper par catégorie et calculer la satisfaction moyenne
satisfaction_by_category = df_exploded.groupby('categorie')['satisfaction'].mean()

# Génération du graphique de satisfaction client en fonction des catégories
plt.figure(figsize=(12, 8))
satisfaction_by_category.plot(kind='bar', color='skyblue')
plt.title('Satisfaction Client par Catégorie (30 premières lignes)')
plt.xlabel('Catégorie')
plt.ylabel('Satisfaction Moyenne')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
