CREATE TABLE IF NOT EXISTS dim_employe (
    id_employe INTEGER PRIMARY KEY,
    nom TEXT,
    prenom TEXT,
    sexe TEXT,
    date_naissance DATE,
    date_embauche DATE,
    poste TEXT,
    service TEXT,
    type_contrat TEXT,
    statut TEXT,
    anciennete INTEGER
);

CREATE TABLE IF NOT EXISTS dim_temps (
    date DATE PRIMARY KEY,
    jour INTEGER,
    mois TEXT,
    annee INTEGER,
    trimestre TEXT,
    semaine INTEGER
);

CREATE TABLE IF NOT EXISTS fact_salaire (
    id_employe INTEGER,
    mois DATE,
    salaire_brut REAL,
    prime REAL,
    heures_sup REAL,
    absences REAL,
    PRIMARY KEY (id_employe, mois),
    FOREIGN KEY (id_employe) REFERENCES dim_employe(id_employe),
    FOREIGN KEY (mois) REFERENCES dim_temps(date)
);

CREATE TABLE IF NOT EXISTS fact_formation (
    id_employe INTEGER,
    date_formation DATE,
    theme TEXT,
    nb_heures INTEGER,
    cout REAL,
    PRIMARY KEY (id_employe, date_formation, theme),
    FOREIGN KEY (id_employe) REFERENCES dim_employe(id_employe),
    FOREIGN KEY (date_formation) REFERENCES dim_temps(date)
);
