import pandas as pd

print("Extraction de données à partir du data store...")

df_calendrier = pd.read_csv("data/raw/calendrier.csv")
df_employes = pd.read_csv("data/raw/employes.csv")
df_formations = pd.read_csv("data/raw/formations.csv")
df_salaires = pd.read_csv("data/raw/salaires.csv")

print("Données enregistrées en dataframes.")