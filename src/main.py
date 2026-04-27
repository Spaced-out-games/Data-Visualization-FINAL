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


def interactive_table(df: DataFrame) -> go.Figure:
	table = go.Figure(data=[go.Table(
		header=dict(values=["Location", "Family Archetype", "Median Family Income"],
					fill_color='paleturquoise',
					align='left'),
		cells=dict(values=[df.areaname, df.family_member_count, df.median_family_income],
				fill_color='lavender',
				align='left'))
	])
	return table


# 3. Draw graphs and analyze the following with state separately: transportation, healthcare_cost, childcare_cost, taxes, median_family_income; family_member_count     

def transportation_graph(df: pd.DataFrame) -> go.Figure:
	if not isinstance(df, pd.DataFrame):
		raise ValueError("Invalid value passed into transportation_graph(): pass a DataFrame")
	
	if not ("state" in df.columns and "transportation_cost" in df.columns):
		raise ValueError("pd.DataFrame doesn't have the needed columns!")
	# dependency checks


	# don't forget to make a copy of `df` so we can sort it without messing with the ordering too much
	data = df.copy()
	fig = go.Figure()



	data = df.groupby("state", as_index=False)["transportation_cost"].mean()
	data = data.sort_values(by="transportation_cost", ascending=False)
	#data = data[:10]

	print(data)

	fig.add_trace(go.Bar(
		x = data["state"],
		
		y = data["transportation_cost"]
	))

	fig.update_layout(
		title="Top 10 Most Expensive Transportation Costs By State",
	    xaxis_title="State",
    	yaxis_title="Transportation Cost"
	)

	return fig
	"""
		As you can see in the title, this is a bar chart of the top ten most expensive states to live in by transportation costs. The dataset originally organized
		the data by the mean costs per family unit, per region, and so naturally I grouped all of them by state and got the medians. Since transportaion costs are relatively
		homogenous across states, I decided to graph by medians, since they are more resistant to outliers.
	
	"""


def healthcare_graph(df: pd.DataFrame) -> go.Figure:
	if not isinstance(df, pd.DataFrame):
		raise ValueError("Invalid value passed into transportation_graph(): pass a DataFrame")
	
	if not ("state" in df.columns and "healthcare_cost" in df.columns):
		raise ValueError("pd.DataFrame doesn't have the needed columns!")
	# dependency checks


	# don't forget to make a copy of `df` so we can sort it without messing with the ordering too much
	data = df.copy()
	fig = go.Figure()



	data = df.groupby("state", as_index=False)["healthcare_cost"].mean()
	data = data.sort_values(by="healthcare_cost", ascending=False)
	#data = data[:10]

	print(data)

	fig.add_trace(go.Bar(
		x = data["state"],
		
		y = data["healthcare_cost"]
	))

	fig.update_layout(
		title="Top 10 Most Expensive Transportation Costs By State",
	    xaxis_title="State",
    	yaxis_title="Healcare Cost (Average USD Per Household)"
	)

	return fig
	"""
		As you can see in the title, this is a bar chart of the top ten most expensive states to live in by transportation costs. The dataset originally organized
		the data by the mean costs per family unit, per region, and so naturally I grouped all of them by state and got the medians. Since transportaion costs are relatively
		homogenous across states, I decided to graph by medians, since they are more resistant to outliers.
	
	"""

#38.7234319,-99.779717

# ------------------------------------------------------------------------------ DRIVER -----------------------------------------------------------------------------
from data_prep import load_dataset, clean_dataset
DATASET_FILENAME = "cost_of_living_us.csv"


if __name__ == "__main__":
	# load the dataset
	df = load_dataset(DATASET_FILENAME)

	# Clean the dataset
	df = clean_dataset(df)
	# show the cleaned dataset
	print(df)

	int_table = interactive_table(df[:1000])
	trans_graph = transportation_graph(df)#.show()
	health_graph = healthcare_graph(df)

	result = go.Figure(data=int_table.data + trans_graph.data + health_graph.data)
	result.show()
