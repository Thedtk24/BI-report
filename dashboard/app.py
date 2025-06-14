import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import sqlite3

# Connexion à la base
conn = sqlite3.connect("warehouse/reporting.db")
df_employes = pd.read_sql_query("SELECT * FROM dim_employe", conn)
df_salaires = pd.read_sql_query("SELECT * FROM fact_salaire", conn)
df_formations = pd.read_sql_query("SELECT * FROM fact_formation", conn)

# Formatage
df_employes["date_naissance"] = pd.to_datetime(df_employes["date_naissance"])
df_employes["date_embauche"] = pd.to_datetime(df_employes["date_embauche"])
df_salaires["mois"] = pd.to_datetime(df_salaires["mois"])
df_formations["date_formation"] = pd.to_datetime(df_formations["date_formation"])

# Données enrichies
df_actifs = df_employes[df_employes["statut"] == "Actif"]
df_salaire_detail = pd.merge(df_salaires, df_employes, on="id_employe")
df_formations_detail = pd.merge(df_formations, df_employes, on="id_employe")

# Années disponibles
annees = sorted(set(df_salaires["mois"].dt.year.unique()).union(df_formations["date_formation"].dt.year.unique()))

# App
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard RH - Reporting annuel"),

    dcc.Dropdown(
        id="filtre-service",
        options=[{"label": s, "value": s} for s in sorted(df_employes["service"].unique())],
        value=None,
        placeholder="Filtrer par service",
        clearable=True
    ),

    dcc.Dropdown(
        id="filtre-sexe",
        options=[
            {"label": "Homme", "value": "M"},
            {"label": "Femme", "value": "F"}
        ],
        value=None,
        placeholder="Filtrer par sexe",
        clearable=True
    ),

    dcc.Dropdown(
        id="filtre-annee",
        options=[{"label": str(a), "value": a} for a in annees],
        value=None,
        placeholder="Filtrer par année",
        clearable=True
    ),

    html.Div(id="kpi-summary", style={
        "display": "flex",
        "gap": "40px",
        "marginBottom": "20px",
        "justifyContent": "space-around",
        "padding": "10px",
        "backgroundColor": "#f9f9f9"
    }),

    html.Div([
        dcc.Graph(id="graph-contrats", style={"width": "48%"}),
        dcc.Graph(id="graph-parite", style={"width": "48%"})
    ], style={
        "display": "flex",
        "justifyContent": "space-between",
        "gap": "4%"
    }),

    dcc.Graph(id="graph-salaire"),
    dcc.Graph(id="graph-evolution-salaire"),
    dcc.Graph(id="graph-heures"),
    dcc.Graph(id="graph-cout"),
    dcc.Graph(id="graph-evolution-cout"),
    dcc.Graph(id="graph-evolution-heures")
])

@app.callback(
    Output("graph-contrats", "figure"),
    Input("filtre-service", "value"),
    Input("filtre-sexe", "value")
)
def maj_graph_contrats(service, sexe):
    df = df_actifs.copy()
    if service:
        df = df[df["service"] == service]
    if sexe:
        df = df[df["sexe"] == sexe]

    contrats = df["type_contrat"].value_counts().reset_index()
    contrats.columns = ["type_contrat", "nombre"]
    return px.pie(contrats, names="type_contrat", values="nombre", title="Répartition contrats")

@app.callback(
    Output("graph-parite", "figure"),
    Input("filtre-service", "value"),
    Input("filtre-annee", "value")
)
def maj_graph_parite(service, annee):
    df = df_actifs.copy()
    if service:
        df = df[df["service"] == service]
    if annee:
        df = df[df["date_embauche"].dt.year <= annee]

    repartition = df["sexe"].value_counts().reset_index()
    repartition.columns = ["sexe", "nombre"]
    repartition["sexe"] = repartition["sexe"].replace({"M": "Homme", "F": "Femme"})

    return px.pie(repartition, names="sexe", values="nombre", title="Répartition H/F des employés")

@app.callback(
    Output("graph-salaire", "figure"),
    Input("filtre-service", "value"),
    Input("filtre-sexe", "value"),
    Input("filtre-annee", "value")
)
def maj_graph_salaire(service, sexe, annee):
    df = df_salaire_detail.copy()
    if service:
        df = df[df["service"] == service]
    if sexe:
        df = df[df["sexe"] == sexe]
    if annee:
        df = df[df["mois"].dt.year == annee]
    df["total_salaire"] = df["salaire_brut"] + df["prime"]
    agg = df.groupby("service")["total_salaire"].sum().reset_index()
    return px.bar(agg, x="service", y="total_salaire", title="Masse salariale par service")

@app.callback(
    Output("graph-evolution-salaire", "figure"),
    Input("filtre-service", "value"),
    Input("filtre-sexe", "value"),
    Input("filtre-annee", "value")
)
def maj_evolution_salaire(service, sexe, annee):
    df = df_salaire_detail.copy()
    if service:
        df = df[df["service"] == service]
    if sexe:
        df = df[df["sexe"] == sexe]
    if annee:
        df = df[df["mois"].dt.year == annee]
    df["total_salaire"] = df["salaire_brut"] + df["prime"]
    agg = df.groupby("mois")["total_salaire"].sum().reset_index()
    fig = px.line(agg, x="mois", y="total_salaire", markers=True, title="Évolution mensuelle de la masse salariale")
    fig.update_layout(xaxis_tickformat="%b %Y")
    return fig

@app.callback(
    Output("graph-heures", "figure"),
    Output("graph-cout", "figure"),
    Input("filtre-service", "value"),
    Input("filtre-sexe", "value"),
    Input("filtre-annee", "value")
)
def maj_graph_formations(service, sexe, annee):
    df = df_formations_detail.copy()
    if service:
        df = df[df["service"] == service]
    if sexe:
        df = df[df["sexe"] == sexe]
    if annee:
        df = df[df["date_formation"].dt.year == annee]
    agg = df.groupby("service").agg({"nb_heures": "sum", "cout": "sum"}).reset_index()
    fig1 = px.bar(agg, x="service", y="nb_heures", title="Heures de formation")
    fig2 = px.bar(agg, x="service", y="cout", title="Coûts des formations")
    return fig1, fig2

@app.callback(
    Output("graph-evolution-cout", "figure"),
    Output("graph-evolution-heures", "figure"),
    Input("filtre-service", "value"),
    Input("filtre-sexe", "value"),
    Input("filtre-annee", "value")
)
def maj_evolution_formations(service, sexe, annee):
    df = df_formations_detail.copy()
    if service:
        df = df[df["service"] == service]
    if sexe:
        df = df[df["sexe"] == sexe]
    if annee:
        df = df[df["date_formation"].dt.year == annee]
    df["mois"] = df["date_formation"].dt.to_period("M").dt.to_timestamp()
    agg = df.groupby("mois").agg({"cout": "sum", "nb_heures": "sum"}).reset_index()
    fig_cout = px.line(agg, x="mois", y="cout", markers=True, title="Évolution mensuelle du coût des formations")
    fig_heures = px.line(agg, x="mois", y="nb_heures", markers=True, title="Évolution mensuelle des heures de formation")
    fig_cout.update_layout(xaxis_tickformat="%b %Y")
    fig_heures.update_layout(xaxis_tickformat="%b %Y")
    return fig_cout, fig_heures

@app.callback(
    Output("kpi-summary", "children"),
    Input("filtre-service", "value"),
    Input("filtre-sexe", "value"),
    Input("filtre-annee", "value")
)
def maj_kpis(service, sexe, annee):
    df_e = df_actifs.copy()
    if service:
        df_e = df_e[df_e["service"] == service]
    if sexe:
        df_e = df_e[df_e["sexe"] == sexe]
    nb_employes = len(df_e)

    df_s = df_salaire_detail.copy()
    if service:
        df_s = df_s[df_s["service"] == service]
    if sexe:
        df_s = df_s[df_s["sexe"] == sexe]
    if annee:
        df_s = df_s[df_s["mois"].dt.year == annee]
    df_s["total_salaire"] = df_s["salaire_brut"] + df_s["prime"]
    total_salaire = round(df_s["total_salaire"].sum(), 2)

    df_f = df_formations_detail.copy()
    if service:
        df_f = df_f[df_f["service"] == service]
    if sexe:
        df_f = df_f[df_f["sexe"] == sexe]
    if annee:
        df_f = df_f[df_f["date_formation"].dt.year == annee]
    total_heures = int(df_f["nb_heures"].sum())
    total_cout = round(df_f["cout"].sum(), 2)

    return [
        html.Div([html.H4("Employés actifs"), html.P(f"{nb_employes}")]),
        html.Div([html.H4("Masse salariale"), html.P(f"{total_salaire:,.0f} €")]),
        html.Div([html.H4("Heures formation"), html.P(f"{total_heures}")]),
        html.Div([html.H4("Coûts formations"), html.P(f"{total_cout:,.0f} €")])
    ]

if __name__ == "__main__":
    app.run(debug=True)
