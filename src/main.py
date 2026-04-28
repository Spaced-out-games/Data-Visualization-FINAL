# ------------------------------------------------------------------------------ SETUP ------------------------------------------------------------------------------

# First things first, import data analysis tools
import numpy as np
import pandas as pd

# for standardization
from sklearn.preprocessing import StandardScaler

# For PCA, SVD, and NMF
from sklearn.decomposition import PCA, TruncatedSVD, NMF





# ---------------------------------------------------------------------------- VISUALIZE ----------------------------------------------------------------------------
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
import folium
import dash
import copy
from dash import dcc, html
# this bypasses an issue on my end regarding VSCode integrated rendering
pio.renderers.default = "browser"



from data_prep import *


# Create a Dash Application
app = dash.Dash("Cost Of Living Dashboard")

# ---------------- RUN ----------------

if __name__ == "__main__":
    df = clean_dataset(load_dataset("cost_of_living_us.csv"))
    df["family_size_numeric"] = df["family_member_count"].apply(parse_family_size)
    print(df)
    #grouped = df.groupby("family_member_count", as_index=True)["family_member_count"]
    app.layout = html.Div([
		html.H1("Cost of Living"),
        
		dcc.Graph(figure=make_interactive_table(df, ["state", "median_family_income", "family_member_count"], ["State", "Income", "Household Size"], 50)),
        
		dcc.Graph(figure=make_barchart_fig(df, "state", "transportation_cost", "Transportation Cost By State")),
        html.Iframe(
			srcDoc=open(create_choropleth_map(load_state_geometries(), df, 'state_full', 'transportation_cost', 'feature.properties.name', [37.7749, -95.7129], 4,
				# fill_color_scheme='YlOrRd',
				legend_title='Transportation Cost'
			), "r").read(),
			width="1960",
			height="1080"
		),
        
		dcc.Graph(figure=make_barchart_fig(df, "state", "healthcare_cost", "Healthcare Cost By State")),
        html.Iframe(
			srcDoc=open(create_choropleth_map(load_state_geometries(), df, 'state_full', 'healthcare_cost', 'feature.properties.name', [37.7749, -95.7129], 4,
				# fill_color_scheme='YlOrRd',
				legend_title='Healthcare Cost'
			), "r").read(),
			width="1960",
			height="1080"
		),
        
		dcc.Graph(figure=make_barchart_fig(df, "state", "childcare_cost", "Childcare Cost By State")),
		html.Iframe(
			srcDoc=open(create_choropleth_map(load_state_geometries(), df, 'state_full', 'childcare_cost', 'feature.properties.name', [37.7749, -95.7129], 4,
				# fill_color_scheme='YlOrRd',
				legend_title='Childcare Cost'
			), "r").read(),
			width="1960",
			height="1080"
		),
        
		dcc.Graph(figure=make_barchart_fig(df, "state", "taxes", "Taxes By State")),
		html.Iframe(
			srcDoc=open(create_choropleth_map(load_state_geometries(), df, 'state_full', 'taxes', 'feature.properties.name', [37.7749, -95.7129], 4,
				# fill_color_scheme='YlOrRd',
				legend_title='Taxes'
			), "r").read(),
			width="1960",
			height="1080"
		),

		dcc.Graph(figure=make_barchart_fig(df, "state", "median_family_income", "Median Income By State")),
		html.Iframe(
			srcDoc=open(create_choropleth_map(load_state_geometries(), df, 'state_full', 'median_family_income', 'feature.properties.name', [37.7749, -95.7129], 4,
				# fill_color_scheme='YlOrRd',
				legend_title='Median Income'
			), "r").read(),
			width="1960",
			height="1080"
		),
        
		dcc.Graph(figure=px.bar(grouped, x="state", y="family_size_numeric", color="family_size_numeric", title="Long-Form Input")),

		
		
	])
    app.run(debug=True)
