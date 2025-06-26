import sqlite3
import pandas as pd
from transform import *

conn = sqlite3.connect("warehouse/reporting.db")
cursor = conn.cursor()

with open("warehouse/schema.sql", "r") as f:
    sql_script = f.read()
cursor.executescript(sql_script)
conn.commit()

existing_ids = pd.read_sql("SELECT id_employe FROM dim_employe", conn)
empl_filtered = empl[~empl["id_employe"].isin(existing_ids["id_employe"])]

if not empl_filtered.empty:
    empl_filtered.to_sql("dim_employe", conn, if_exists="append", index=False)
    print(f"{len(empl_filtered)} lignes insérées dans dim_employe.")
else:
    print("Aucune nouvelle ligne à insérer dans dim_employe.")

existing_sals = pd.read_sql("SELECT id_employe, mois FROM fact_salaire", conn)
existing_sals["mois"] = pd.to_datetime(existing_sals["mois"])

merged_sal = sal.merge(existing_sals, on=["id_employe", "mois"], how="left", indicator=True)
sal_filtered = merged_sal[merged_sal["_merge"] == "left_only"].drop(columns=["_merge"])

if not sal_filtered.empty:
    sal_filtered.to_sql("fact_salaire", conn, if_exists="append", index=False)
    print(f"{len(sal_filtered)} lignes insérées dans fact_salaire.")
else:
    print("Aucune nouvelle ligne à insérer dans fact_salaire.")

existing_forms = pd.read_sql("SELECT id_employe, date_formation FROM fact_formation", conn)
existing_forms["date_formation"] = pd.to_datetime(existing_forms["date_formation"])

merged_form = form.merge(existing_forms, on=["id_employe", "date_formation"], how="left", indicator=True)
form_filtered = merged_form[merged_form["_merge"] == "left_only"].drop(columns=["_merge"])

if not form_filtered.empty:
    form_filtered.to_sql("fact_formation", conn, if_exists="append", index=False)
    print(f"{len(form_filtered)} lignes insérées dans fact_formation.")
else:
    print("Aucune nouvelle ligne à insérer dans fact_formation.")

existing_dates = pd.read_sql("SELECT date FROM dim_temps", conn)
existing_dates["date"] = pd.to_datetime(existing_dates["date"])

merged_cal = cal.merge(existing_dates, on="date", how="left", indicator=True)
cal_filtered = merged_cal[merged_cal["_merge"] == "left_only"].drop(columns=["_merge"])

if not cal_filtered.empty:
    cal_filtered.to_sql("dim_temps", conn, if_exists="append", index=False)
    print(f"{len(cal_filtered)} lignes insérées dans dim_temps.")
else:
    print("Aucune nouvelle ligne à insérer dans dim_temps.")

conn.commit()
conn.close()
print("Chargement terminé avec succès.")
