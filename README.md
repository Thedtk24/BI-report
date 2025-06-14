# Projet RH Dashboard – Reporting annuel

Ce projet est une application Dash interactive permettant de visualiser, filtrer et analyser les données sociales d'une entreprise dans le cadre du reporting annuel à l'État. Il facilite la consultation de KPIs et la production de statistiques à partir de données RH massives (salaires, formations, emplois).

---

## Fonctionnalités principales

* **Filtres dynamiques** par service, sexe et année
* **Graphiques interactifs** :
  * Répartition des contrats et parité homme/femme
  * Masse salariale par service et évolution mensuelle
  * Coûts et durées des formations par service
  * KPIs synthétiques : effectif actif, masse salariale, coûts & heures de formation

---

## Structure du projet

```
project-root/
├── data/                  # Données sources CSV
├── etl/
│   ├── extract.py         # Extraction & nettoyage des données
│   ├── transform.py       # Transformation des données (formatage, enrichissement)
│   └── load.py            # Chargement vers base SQLite
├── warehouse/
│   ├── reporting.db       # Base de données SQLite
│   └── schema.sql         # Schéma SQL de la base (dimensions & faits)
├── dashboard/
│   └── app.py             # Application Dash (vizualisation)
└── README.md              # Documentation du projet
```

---

## Installation & lancement

1. **Cloner le dépôt**

```bash
git clone https://github.com/votre-utilisateur/rh-dashboard.git
cd rh-dashboard
```

2. **Créer un environnement virtuel**

```bash
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
```

3. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

4. **Exécuter le pipeline ETL**

```bash
python etl/extract.py
python etl/transform.py
python etl/load.py
```

5. **Lancer le dashboard**

```bash
python dashboard/app.py
```

---

## Aperçu

* Graphiques clairs & responsifs (Plotly)
* Interface utilisateur fluide avec Dash
* Organisation en cartes KPI et visualisations filtrables

---

## Technologies utilisées

* **Python**
* **Pandas** pour la manipulation des données
* **SQLite** pour le stockage en Data Warehouse local
* **Dash + Plotly** pour le dashboard interactif

---

## Améliorations futures

* Ajout d'une fonctionnalité d'export CSV ou PDF
* Intégration d'un mode sombre
* Mise en ligne (Render, Streamlit Cloud, etc.)
* Authentification utilisateur (SSO / JWT)

---

## Contributeur

* Thed Arthur – Software Engineer
