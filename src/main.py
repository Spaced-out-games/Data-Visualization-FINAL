# ------------------------------------------------------------------------------ SETUP ------------------------------------------------------------------------------

# First things first, import data analysis tools
import numpy as np
import pandas as pd

# for standardization
from sklearn.preprocessing import StandardScaler

# For PCA, SVD, and NMF
from sklearn.decomposition import PCA, TruncatedSVD, NMF





# ---------------------------------------------------------------------------- VISUALIZE ----------------------------------------------------------------------------
import matplotlib.pyplot as plt
import folium
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import dash
from dash import dcc, html
# this bypasses an issue on my end regarding VSCode integrated rendering
pio.renderers.default = "browser"



import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd

from data_prep import load_dataset, clean_dataset

df = clean_dataset(load_dataset("cost_of_living_us.csv"))

# Create a Dash Application
app = dash.Dash(__name__)

# ---------------- FIGURES ----------------


def make_barchart_fig(df: pd.DataFrame, x: str, y: str, title: str, agg="mean"):
    grouped = getattr(df.groupby(x)[y], agg)().reset_index()
    grouped = grouped.sort_values(by=y, ascending=False)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=grouped[x], y=grouped[y]))
    fig.update_layout(title=title)
    return fig


def make_interactive_table(df: pd.DataFrame, keys: list[str], labels: list[str], num_entries: int) -> go.Figure:

    # --- validation ---
    if len(keys) != len(labels):
        raise ValueError("keys and labels must have the same length")

    missing = [k for k in keys if k not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in dataframe: {missing}")

    # --- slice data ---
    df_slice = df.iloc[:num_entries]

    # --- build column values dynamically ---
    column_values = [df_slice[key] for key in keys]

    # --- create table ---
    fig = go.Figure(data=[go.Table(
        header=dict(values=labels),
        cells=dict(values=column_values)
    )])

    return fig


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    x: float
    y: float

class Location(Point):
    label: str


def make_cloropleth_map(position: Point, initial_zoom: int, markers: list[Location], map_path: str) -> str:
    m = folium.Map(location=[position.x, position.y], zoom_start=initial_zoom)

    for location in markers:
        folium.Marker(
            location=[location.x, location.y],
            popup=location.label
        ).add_to(m)
    m.save(map_path)
    return map_path # for convenience



#38.7234319,-99.779717


# ---------------- LAYOUT ----------------

app.layout = html.Div([
    html.H1("Cost of Living Dashboard"),

    dcc.Graph(figure=make_interactive_table(df, ["state", "median_family_income", "family_member_count"], ["State", "Income", "Household Size"], 50)),
    dcc.Graph(figure=make_barchart_fig(df, "state", "transportation_cost", "Transportation Cost By State")),
    dcc.Graph(figure=make_barchart_fig(df, "state", "healthcare_cost", "Healthcare Cost By State")),
    dcc.Graph(figure=make_barchart_fig(df, "state", "childcare_cost", "Childcare Cost By State")),
    #dcc.Graph(figure=make_barchart_fig(df, "state", "family_member_count", "Family Makeup By State")),
    html.Iframe(
        srcDoc=open(make_cloropleth_map(Point(0,0), 16, [], "test.html"), "r").read(),
        width="1960",
        height="1080"
	)
])


# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)
