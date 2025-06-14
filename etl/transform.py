import pandas as pd
from extract import *
from datetime import datetime

# Nettoyage table employes

df_employes["date_naissance"] = pd.to_datetime(df_employes["date_naissance"])
df_employes["date_embauche"] = pd.to_datetime(df_employes["date_embauche"])

# Est ce qu'il y a des cases sans valeurs ?
if df_employes.isnull().values.any():
    print("Valeurs manquantes")
    print(df_employes[df_employes.isnull().any(axis=1)])

else:
    print("Pas de valeurs manquantes")

# Est ce qu'il y a des doublons ?
if df_employes['id_employe'].duplicated().any():
    print("Il y a des doublons sur la colonne 'id'.")
    df_employes = df_employes.drop_duplicates(subset='id', keep='first')

else:
    print("Pas de doublons sur la colonne 'id'.")

annee_actuelle = datetime.now().year
df_employes['anciennete'] = annee_actuelle - df_employes['date_embauche'].dt.year

# Nettoyage table salaire

df_salaires["mois"] = pd.to_datetime(df_salaires["mois"], format="%Y-%m")
df_salaires["prime"] = df_salaires["prime"].astype(float)  
df_salaires["salaire_brut"] = df_salaires["salaire_brut"].astype(float)  

# Nettoyage table formation

df_formations["date_formation"] = pd.to_datetime(df_formations["date_formation"])
df_formations["cout"] = df_formations["cout"].astype(float)

# Nettoyage table calendrier

df_calendrier["date"] = pd.to_datetime(df_calendrier["date"])

cal = df_calendrier
empl = df_employes
form = df_formations
sal = df_salaires
