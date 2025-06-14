import sqlite3
from transform import *

conn = sqlite3.connect("warehouse/reporting.db")
cursor = conn.cursor()

with open("warehouse/schema.sql", "r") as f:
    sql_script = f.read()

cursor.executescript(sql_script)
conn.commit()

empl.to_sql("dim_employe", conn, if_exists="append", index=False)
conn.commit()

sal.to_sql("fact_salaire", conn, if_exists="append", index=False)
conn.commit()

form.to_sql("fact_formation", conn, if_exists="append", index=False)
conn.commit()

cal.to_sql("dim_temps", conn, if_exists="append", index=False)
conn.commit()

conn.close()