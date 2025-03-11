## Equipe 8 - Projet 48h

Bienvenue dans ce projet 48H ynov, édition mars 2025 !

Voici la liste des membres de l'équipe :

- HAMEDI Elisa
- FIGUEIRA Thibaut
- TSUI Jia-Bao
- LI Oscar
- SAIDI Abdelhamid

## Lancement du projet

Assurer vous de posseder sur votre ordinateur les modules suivants :

- pythons
- matplotlib
- pandas
- mistalai
- streamlit
- numpy

Positionner vous dans le fichier "Script".

```bash
cd script/
```

Run le fichier main.py pour nettoyer et préparer les datas, elle seront visualisable dans le fichier csv "tweets_v2.csv".

```bash
py main.py
```

Run le fichier nuageCreator.py, pour faire apparaitre un nuage de mots.

```bash
py nuageCreator.py
```

Run le fichier kpi_dataCSV.py avec streamlit pour visualiser les graphs sur les données de nettoyer de notre csv.

```bash
streamlit run kpi_dataCSV.py
```

Run le fichier agent.py pour faire tourner l'agents mystralAI, *attention ce processus peut être long*.

```bash
py agent.py
```

Run le fichier kpi_nombreTweets.py avec streamlit pour visualiser le nombre de tweets envoyé en direction des comptes ENGI.

```bash
streamlit run kpi_nombreTweets.py
```

Run le fichier kpi_dataAgent.py avec streamlit pour visualiser les graphs sur les données de notre agent mistral.

```bash
streamlit run kpi_dataAgent.py
```


## Configuration de l'agent Mistral AI

Voici la configuration de notre agent Mistral

###### format d'entrée

Je vais te donner des tweets, pour chaque tweets donner, chaque tweets sera composer de cette manière :

id_utilisateur,pseudo_user,description_user,content,image,date_time,timezone,contains_délai,contains_panne,contains_urgence,contains_scandale,contains_pas,contains_jamais,contains_rien,contains_problème,contains_erreur,contains_impossible,contains_tarifs,contains_aucune

###### format de sortie

{
"satisfaction" : int,
"sentiment" : string,
"urgence" : boolean,
"mots clefs" : [string],
"catégorie" : [string]
}


###### Satisfaction

Je veux que tu analyse le sentiment de satisfaction humain que dégage le tweets.

Tu donnera a chaque tweets une note de ressentis "satisfactions", allant de : -10= très insatisfait en passant par 0=avis neutre et allant jusqu'à 10=grandement satisfait. 

cette note de satisfaction dépendra de plusieurs facteur :
- si l'user a envoye plusieur tweets dans un espace de temps réduis, et si le contenue de ces tweets son negatif, il deviendrons encore plus negatif car le client est mécontend et envoie plusieur tweets de meme si le client envoie des tweets positifs.
- si le client utilise beaucoup de mots a booleans de notre csv, plus de booleans son en true, plus on considera que notre client emploie des mots enerver et est donc insatisfait.
- ta propre apréciation, en plus des prises en comptes précedentes, je veux que tu evalue toi meme la situation et rajoute dans la note finale ton evalution de la situation pour ensuite donner une note allant donc de -10 a 10.
-les émoticônes peuvent montrer aussi le sentiment du client, interprète les.

Prend bien tous ces facteurs en comptes pour cree la note final

###### Sentiment
Pour une note de satisfaction egale ou proche de zero soit -2; -1; 0; 1; 2; tu donnera un sentiment "neutre.
Pour une note de satisfaction négative inferieur strictement a -2, tu donnera un sentiment "negatif".
Pour une note de satisfaction positive supérieur strictement a 2, tu donnera un sentiment "positif".

###### Urgence

Pour le boolean urgence, je veux que tu le coche uniquement dans certaine condition, soit si le client qui ecris a un probleme qui ne peut attendre, soit par exemple
-chauffage en hivert
-Attente deja trop longue

###### mots clefs

A chaque tweets tu regardera le "content" et tu associera un theme globale du message en 12 mots maximal.


###### catégorie


De ce theme globale fomer de mots clefs, tu associera des "etiquettes" c'est a dire une categories pour resume le contenue du tweets, voici des exemples de categories : 

- Problèmes de facturation (par exemple  erreurs de montant, prélèvements injustifiés.)
- Pannes et urgences (par exemple absence de gaz, d’électricité, problème d’eau chaude. )
- Service client injoignable (par exemple absence de réponse, relances infructueuses.)
- Problèmes avec l’application (par exemple bugs, indisponibilité du service. )

tu pourra ajouter d'autre mots clef a la liste si tu trouve des themes pertinents qui ressortent souvent, tu peux appliquer plusieurs etiquettes a un tweets. 

Fait en sorte que les etiquettes soit communs entre plusieurs tweets, reunis les catégories.

Par exemple delais et retard son la meme choses, reunis les sous le mots "retard"

Quand il y a un problème avec le service client, précise le type, téléphonique, internet, agent en ajoutant probleme ou succès soit Problème service client téléphonique par exemple.

l'étiquette "besoin d'aide" quand le client demande assistance.


##### Exemples 1


>Entrer

1,0Poliak,elPoliak,@ENGIEpartFR alors comme ça on veut pas rembourser ses client et on leur impute des délais et des contraintes effarantes alors que c’est vous qui êtes en tord ? Ça commence à faire beaucoup la non ?,[],2024-02-23 11:38:19,+01:00,True,False,False,False,True,False,False,False,False,False,False,False

>Sortie

{
"satisfaction" : -6,
"sentiment" : négatif,
"urgence" : false,
"mots clefs" : [ENGIE refuse remboursement clients; délais; contraintes],
"catégorie" : [Problème de facturation, Retard]
}

##### Exemples 2

>Entrer

3,9semL,9sl,Vraiment des incapables @ENGIEgroup qui me font prendre une demi journée de taff pour que leur technicien ne soit jamais arrivé ! Quand je les appels ils me raccrochent au nez ??? Mais on est où là ??? @ENGIEgroup boycott,[],2024-08-29 17:09:06,+02:00,False,False,False,False,False,True,False,False,False,False,False,False

>Sortie

{
"satisfaction" : -7,
"sentiment" : négatif,
"urgence" : false,
"mots clefs" : [ENGIE service incompetent, technicien absent, boycott],
"catégorie" : [Retard, Service client téléphonique mauvais, problème rendez-vous],
}

##### Exemples 3

>Entrer

4,ANDIAAAL,ANDIAL,"Bonjour @ENGIEpartFR, ça fait plus de 10 min que j’attends au téléphone pour modifier la date de rdv avec le technicien, votre site étant en maintenance DEPUIS UNE SEMAINE ! 😡\n\nOn peut modifier ça en DM ? Merci ! #Engie @ENGIEgroup",[],2024-06-27 11:18:08,+02:00,False,False,False,False,False,False,False,False,False,False,False,False

>Sortie

{
"satisfaction" : -8,
"sentiment" : négatif,
"urgence" : false,
"mots clefs" : [ENGIE attente, site maintenance, frustration, technicien],
"catégorie" : [Retard, Service client internet mauvais, problème rendez-vous]
}