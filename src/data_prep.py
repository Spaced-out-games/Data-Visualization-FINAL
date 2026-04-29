import os
import copy
import json
import folium
import plotly.graph_objects as go
from urllib.request import urlopen

print (f"Current working directory: {os.getcwd()}")


STATE_FULLNAME_LOOKUP = {
	'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
	'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'DC': 'District of Columbia',
	'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois',
	'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana',
	'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota',
	'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
	'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
	'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon',
	'PA': 'Pennsylvania', 'PR': 'Puerto Rico', 'RI': 'Rhode Island', 'SC': 'South Carolina',
	'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
	'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
}

STATE_GEOMETRIES_URL = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"


# import processing libraries
import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA, TruncatedSVD, NMF

# Whether or not this project is being run on a local machine or in a Colab notebook 
LOCAL_ENV = True
DATASET_DIR = None
if(not LOCAL_ENV):
	from google.colab import drive
	drive.mount('/content/drive')
	DATASET_DIR = "/content/drive/MyDrive/datasets/"
else:
	DATASET_DIR = "data/"

# Helper functions
def apply_PCA(target: np.ndarray, num_components: int, standardize: bool = True) -> np.ndarray:
	# auto-standardize if you wish
	if(standardize):
		target = StandardScaler().fit_transform(target)

	transformer = PCA(n_components=num_components)
	return transformer.fit_transform(target)
def apply_SVD(target: np.ndarray, num_components: int, standardize: bool = True) -> np.ndarray:
	if(standardize):
		target = StandardScaler().fit_transform(target)

	U, S, VT = np.linalg.svd(target)

	# grab the left singular values
	U = U[:,:num_components]

	# grab the singular values
	S = np.diag(S[:num_components])

	#grab the right singular values
	VT = VT[:num_components, :]

	return np.dot(U, np.dot(S, VT))

def apply_NMF(target: np.ndarray, num_components: int, standardize: bool = True) -> np.ndarray:
	if(standardize):
		target = StandardScaler().fit_transform(target)

	transformer = NMF(n_components=num_components)
	return transformer.fit_transform(target)



def load_dataset(dataset_name: str) -> pd.DataFrame:

	filename: str = f'{DATASET_DIR}{dataset_name}'
	print(f"Loading file {filename}...")
	df: pd.DataFrame = pd.read_csv(filename)

	return df

def clean_dataset(dataset: pd.DataFrame) -> pd.DataFrame:
	dataset['state_full'] = dataset['state'].map(STATE_FULLNAME_LOOKUP)
	dataset = dataset.dropna()
	total_null_entries = np.sum(dataset.isnull().sum())
	if(bool(total_null_entries != 0)):
		print(f"ERROR: no null values assertion failed. Total null entries: {total_null_entries}")
		return None
	return dataset

def load_state_geometries():
	with urlopen(STATE_GEOMETRIES_URL) as response:
		state_geometries = json.load(response)
	return state_geometries


def create_choropleth_map(
	geo_data,
	dataframe,
	state_col_df,  # Column in dataframe for state names
	value_col_df,  # Column in dataframe for values to color code
	key_on_geojson,  # GeoJSON property to join on (e.g., 'feature.properties.name')
	map_location=[37.7749, -122.4194],
	map_zoom=4,
	fill_color_scheme='YlGn',
	legend_title='Value',
	map_path: str = "untitled"
):
	"""Generates a Folium choropleth map.

	Args:
		geo_data (dict): The GeoJSON data for the map.
		dataframe (pd.DataFrame): DataFrame containing data to be mapped.
		state_col_df (str): Name of the column in `dataframe` that contains the state identifiers.
		value_col_df (str): Name of the column in `dataframe` that contains the values for color coding.
		key_on_geojson (str): The GeoJSON property to join on (e.g., 'feature.properties.name').
		map_location (list): Latitude and longitude for the map's center.
		map_zoom (int): Initial zoom level of the map.
		fill_color_scheme (str): Colormap to use for the choropleth (e.g., 'YlGn', 'RdBu', 'Plasma').
		legend_title (str): Title for the color legend.

	Returns:
		folium.Map: The generated Folium map object.
	"""
	m = folium.Map(location=map_location, zoom_start=map_zoom)

	# Make a copy of the GeoJSON data to avoid modifying the original
	geo_data_copy = copy.deepcopy(geo_data)

	# Extract the actual property key from key_on_geojson (e.g., 'name' from 'feature.properties.name')
	geojson_prop_key = key_on_geojson.split('.')[-1]

	# Create a dictionary for quick lookup of values from the dataframe
	data_lookup = dataframe.set_index(state_col_df)[value_col_df].to_dict()

	# Iterate through GeoJSON features and add the value_col_df to their properties
	for feature in geo_data_copy['features']:
		state_name_in_geojson = feature['properties'].get(geojson_prop_key)
		if state_name_in_geojson in data_lookup:
			feature['properties'][value_col_df] = data_lookup[state_name_in_geojson]
		else:
			# Handle cases where a state in GeoJSON might not be in the dataframe
			feature['properties'][value_col_df] = None # Assign None or a default value

	choropleth_layer = folium.Choropleth(
		geo_data=geo_data_copy, # Use the modified geo_data
		name='choropleth',
		data=dataframe, # Keep data and columns for choropleth coloring logic
		columns=[state_col_df, value_col_df],
		key_on=key_on_geojson,
		fill_color=fill_color_scheme,
		fill_opacity=0.7,
		line_opacity=0.2,
		legend_name=legend_title
	).add_to(m)

	# Now the GeoJsonTooltip can access value_col_df directly from feature.properties
	choropleth_layer.geojson.add_child(
		folium.features.GeoJsonTooltip(
			fields=[geojson_prop_key, value_col_df], # Now 'childcare_cost' is in properties
			aliases=['State', legend_title], # Aliases for display
			localize=True,
			sticky=False,
			labels=True,
			style="""
				background-color: #F0EFEF;
				border: 2px solid black;
				border-radius: 3px;
				box-shadow: 3px;
			""",
			max_width=800,
		)
	)

	folium.LayerControl().add_to(m)
	m.save(map_path)
	return map_path


def make_barchart_fig(df, x, y, title, agg="mean", color=None, colorscale=None):
	if agg:
		grouped = df.groupby(x, as_index=False)[y].agg(agg)
	else:
		grouped = df[[x, y]].copy()

	grouped = grouped.sort_values(by=y, ascending=False)

	# --- CASE 1: colorscale (data-driven) ---
	if colorscale:
		fig = px.bar(
			grouped,
			x=x,
			y=y,
			title=title,
			color=y,
			color_continuous_scale=colorscale
		)
		fig.update_coloraxes(
			cmin=grouped[y].min(),
			cmax=grouped[y].max() * 10
		)

	# --- CASE 2: single color ---
	else:
		fig = px.bar(
			grouped,
			x=x,
			y=y,
			title=title
		)

		if color:
			fig.update_traces(marker_color=color)

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

def parse_family_size(s):
	return int(s[0]) + int(s[2])
	# import re
	# nums = list(map(int, re.findall(r'\d+', s)))
	# return sum(nums) if nums else None

