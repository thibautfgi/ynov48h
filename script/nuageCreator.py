import pandas as pd
import re
import random
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

def get_text_dimensions(text, font):
    """Retourne les dimensions (largeur, hauteur) d'un texte avec une police donnée."""
    img = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(img)
    return draw.textbbox((0, 0), text, font=font)[2:]

def create_dic(texte, exclusion):
    """Crée un dictionnaire de fréquence des mots à partir du texte donné, en excluant certains mots."""
    mots = re.findall(r'\b\w+\b', texte.lower())  # Séparer les mots, tout en les mettant en minuscule
    mots_filtres = [mot for mot in mots if mot not in exclusion and len(mot) > 2]  # Exclure les mots trop courts
    frequence = {}
    for mot in mots_filtres:
        frequence[mot] = frequence.get(mot, 0) + 1
    return frequence

def check_collision(x, y, width, height, positions):
    """Vérifie s'il y a une collision avec les positions des mots déjà dessinés."""
    for (px, py, pw, ph) in positions:
        if not (x + width < px or x > px + pw or y + height < py or y > py + ph):
            return True
    return False

def nuage(fichier_csv, size=(800, 600), max_words=100):
    """Génère un nuage de mots à partir des tweets d'un fichier CSV, garantissant l'apparition de tous les mots."""
    try:
        df = pd.read_csv(fichier_csv, sep=",", encoding="utf-8")
        texte = " ".join(df["content"].astype(str))  # Fusionner tous les tweets en une seule chaîne de texte
    except FileNotFoundError:
        print("Erreur : Le fichier CSV est introuvable.")
        return
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return

    exclusion = [
        "le", "la", "les", "un", "une", "des", "du", "au", "aux", "ce", "cette", "ces", 
        "je", "tu", "il", "elle", "on", "nous", "vous", "ils", "elles", "me", "te", "se", "lui", "leur", "moi", "toi", "soi", "nous", "vous", "eux", 
        "à", "de", "en", "pour", "par", "avec", "sans", "sur", "sous", "dans", "entre", "chez", "contre", "vers",  
        "et", "ou", "mais", "donc", "or", "ni", "car", "que", "puis", "lorsque", "quand", "si", 
        "bien", "mal", "très", "trop", "peu", "aussi", "encore", "déjà", "autant", "ainsi", "même", "alors", 
        "être", "avoir", "faire", "aller", "pouvoir", "devoir", "vouloir", "savoir", "dire", "voir", "venir",
        "est", "plus", "ont", "non", "sont", "êtes", "mes", "avez", "vos", "suis"  
    ]

    mots = create_dic(texte, exclusion)
    max_size = min(size[0], size[1]) // 3  # Taille maximale d'un mot

    w, h = size
    cloud = Image.new("RGB", (w, h), 'white')
    d = ImageDraw.Draw(cloud)
    m = max(mots.values(), default=1)

    positions = []  # Liste pour garder une trace des positions des mots
    counter = 0  # Compteur pour les mots dessinés
    for key, value in sorted(mots.items(), key=lambda x: x[1], reverse=True):
        if counter >= max_words:  # Limiter à 100 mots
            break
        try:
            # Ajuster la taille des mots proportionnellement à leur fréquence
            fontsize = int((max_size * value / m) * 1.5)  # Agrandir davantage la taille des mots
            font = ImageFont.truetype("arial.ttf", fontsize)
            text_width, text_height = get_text_dimensions(key, font)

            # Générer une position aléatoire sans chevauchement
            x_max = w - text_width - 20
            y_max = h - text_height - 20
            placed = False

            for _ in range(100):  # Essayer jusqu'à 100 fois de trouver une position valide
                x, y = random.randint(20, x_max), random.randint(20, y_max)
                if not check_collision(x, y, text_width, text_height, positions):
                    positions.append((x, y, text_width, text_height))  # Enregistrer la position
                    placed = True
                    break

            if placed:
                # Dessiner le mot avec une couleur aléatoire
                d.text((x, y), key, font=font, fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                counter += 1
        except Exception as e:
            continue

    # Afficher le nuage de mots
    plt.figure(figsize=(10, 8))
    plt.imshow(cloud)
    plt.axis("off")
    plt.show()

# Exemple d'utilisation
nuage("/../csv/tweets_v2.csv", max_words=100)
