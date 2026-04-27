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

def make_transport_fig(df):
    data = df.groupby("state", as_index=False)["transportation_cost"].mean()
    data = data.sort_values(by="transportation_cost", ascending=False)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=data["state"], y=data["transportation_cost"]))
    fig.update_layout(title="Transportation Cost by State")
    return fig


def make_health_fig(df):
    data = df.groupby("state", as_index=False)["healthcare_cost"].mean()
    data = data.sort_values(by="healthcare_cost", ascending=False)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=data["state"], y=data["healthcare_cost"]))
    fig.update_layout(title="Healthcare Cost by State")
    return fig


def make_interactive_table(df):
    return go.Figure(data=[go.Table(
        header=dict(values=["State", "Income", "Household Size"]),
        cells=dict(values=[
            df["state"][:20],
            df["median_family_income"][:20],
            df["family_member_count"][:20]
        ])
    )])

# ---------------- LAYOUT ----------------

app.layout = html.Div([
    html.H1("Cost of Living Dashboard"),

    dcc.Graph(figure=make_interactive_table(df)),
    dcc.Graph(figure=make_transport_fig(df)),
    dcc.Graph(figure=make_health_fig(df))
])

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)
