import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime

# Charger les données depuis le fichier CSV
df = pd.read_csv("new_filtered_tweets_engie.csv")

# Convertir la colonne 'date_time' en datetime
df['date_time'] = pd.to_datetime(df['date_time'], format='%Y-%m-%d %H:%M:%S')

# Ajouter des colonnes pour le jour, la semaine, le mois et le jour de la semaine
df["day"] = df["date_time"].dt.date
df["week"] = df["date_time"].dt.isocalendar().week
df["month"] = df["date_time"].dt.to_period('M')
df["day_of_week"] = df["date_time"].dt.day_name()

# Traduire les jours de la semaine en français
day_mapping = {
    "Monday": "Lundi",
    "Tuesday": "Mardi",
    "Wednesday": "Mercredi",
    "Thursday": "Jeudi",
    "Friday": "Vendredi",
    "Saturday": "Samedi",
    "Sunday": "Dimanche"
}

df["day_of_week_fr"] = df["day_of_week"].map(day_mapping)

# Filtrer les données pour les fuseaux horaires +01:00 et +02:00
df_tz_plus1 = df[df['timezone'] == '+01:00']
df_tz_plus2 = df[df['timezone'] == '+02:00']

total_tweets = len(df.index)

# Calcul des KPI
# 1. Nombre de tweets par jour de la semaine
tweets_per_day_of_week = df.groupby("day_of_week_fr").size().reindex([
    "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"
])

# 2. Nombre de tweets par mois
tweets_per_month = df.groupby("month").size()

# 3. Nombre de tweets par fuseau horaire
tweets_per_tz_plus1 = df_tz_plus1.groupby("day_of_week_fr").size().reindex([
    "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"
])

tweets_per_tz_plus2 = df_tz_plus2.groupby("day_of_week_fr").size().reindex([
    "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"
])

# Calcul du pourcentage de tweets pour chaque fuseau horaire par jour
percentage_tz_plus1 = (tweets_per_tz_plus1 / total_tweets) * 100
percentage_tz_plus2 = (tweets_per_tz_plus2 / total_tweets) * 100

# Création des graphiques
def plot_kpi():
    # Plot Nombre de tweets par jour de la semaine
    st.subheader("Nombre de tweets par jour de la semaine")
    fig, ax = plt.subplots(figsize=(10, 6))
    tweets_per_day_of_week.plot(ax=ax, kind="bar", color="blue", title="Nombre de tweets par jour de la semaine")
    ax.set_ylabel('Nombre de tweets')
    st.pyplot(fig)

    # Plot Nombre de tweets par mois
    st.subheader("Nombre de tweets par mois")
    fig, ax = plt.subplots(figsize=(10, 6))
    tweets_per_month.plot(ax=ax, kind="bar", color="red", title="Nombre de tweets par mois")
    ax.set_ylabel('Nombre de tweets')
    st.pyplot(fig)

    # Plot Pourcentage de tweets par fuseau horaire par jour
    st.subheader("Pourcentage de tweets par fuseau horaire par jour")
    fig, ax = plt.subplots(figsize=(10, 6))
    percentage_tz_plus1.plot(ax=ax, kind="bar", color="green", position=0, width=0.4, label='Timezone +01:00')
    percentage_tz_plus2.plot(ax=ax, kind="bar", color="orange", position=1, width=0.4, label='Timezone +02:00')
    for i in ax.patches:
        ax.text(i.get_x() + i.get_width() / 2, i.get_height(), str(round(i.get_height(), 2)) + '%',
                ha='center', va='bottom')
    ax.set_ylabel('Pourcentage de tweets')
    ax.set_title("Pourcentage de tweets par jour et fuseau horaire")
    ax.legend()
    st.pyplot(fig)

# Affichage des résultats dans Streamlit
plot_kpi()