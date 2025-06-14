import pandas as pd

def afficher_infos(df, nom):
    print(f"Infos sur {nom}")
    print("-" * 40)
    print(df.shape)
    print(df.columns)
    print(df.dtypes)
    print("\n")

def calculer_anciennete(date_embauche, reference_annee=2025):
    return reference_annee - date_embauche.year
