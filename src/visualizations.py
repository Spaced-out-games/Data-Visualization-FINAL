import pandas as pd
import numpy as np
import dash
from dash import dcc, html
from data_prep import *



def make_dashboard(df: pd.Dataframe, name: str = "Cost Of Living Dashboard", dataset: str = "cost_of_living_us.csv") -> dash.Dash:



	items = []
	
	
	# make family_member_count numeric
	#df["family_size_numeric"] = df["family_member_count"].apply(parse_family_size)

	app = dash.Dash("Cost Of Living Dashboard")









	stacked_df = (
	df.groupby(["state", "family_member_count"])
	  .size()
	  .reset_index(name="count")
	  
	).sort_values(["state", "family_member_count"])

	state_order = (
		stacked_df.groupby("state")["count"]
		.sum()
		.sort_values(ascending=False)
		.index
	)


	items.append(html.H1("Cost of Living"))

	items.append(dcc.Graph(figure=make_barchart_fig(df, "state", "transportation_cost", "Transportation Cost By State")))
	
	items.append(dcc.Graph(figure=make_barchart_fig(df, "state", "transportation_cost", "Transportation Cost By State")))

	items.append(html.Iframe(
			srcDoc=open(create_choropleth_map(load_state_geometries(), df, 'state_full', 'transportation_cost', 'feature.properties.name', [37.7749, -95.7129], 4,
				# fill_color_scheme='YlOrRd',
				legend_title='Transportation Cost'
			), "r").read(),
			width="1960",
			height="1080"
		)
	)

	items.append(dcc.Graph(figure=make_barchart_fig(df, "state", "healthcare_cost", "Healthcare Cost By State")))

	items.append(html.Iframe(srcDoc=open(create_choropleth_map(load_state_geometries(), df, 'state_full', 'healthcare_cost', 'feature.properties.name', [37.7749, -95.7129], 4,
				# fill_color_scheme='YlOrRd',
				legend_title='Healthcare Cost'
			), "r").read(),
			width="1960",
			height="1080"
		)
	)

	items.append(dcc.Graph(figure=make_barchart_fig(df, "state", "childcare_cost", "Childcare Cost By State")))

	items.append(html.Iframe(
			srcDoc=open(create_choropleth_map(load_state_geometries(), df, 'state_full', 'childcare_cost', 'feature.properties.name', [37.7749, -95.7129], 4,
				# fill_color_scheme='YlOrRd',
				legend_title='Childcare Cost'
			), "r").read(),
			width="1960",
			height="1080"
		)
	)

	items.append(dcc.Graph(figure=make_barchart_fig(df, "state", "taxes", "Taxes By State")))


	items.append(html.Iframe(
			srcDoc=open(create_choropleth_map(load_state_geometries(), df, 'state_full', 'taxes', 'feature.properties.name', [37.7749, -95.7129], 4,
				# fill_color_scheme='YlOrRd',
				legend_title='Taxes'
			), "r").read(),
			width="1960",
			height="1080"
		)
	)

	items.append(dcc.Graph(figure=make_barchart_fig(df, "state", "median_family_income", "Median Income By State")))

	items.append(html.Iframe(
			srcDoc=open(create_choropleth_map(load_state_geometries(), df, 'state_full', 'median_family_income', 'feature.properties.name', [37.7749, -95.7129], 4,
				# fill_color_scheme='YlOrRd',
				legend_title='Median Income'
			), "r").read(),
			width="1960",
			height="1080"
		)
	)

	items.append(dcc.Graph(figure = px.bar(
		stacked_df,
		x="state",
		y="count",
		color="family_member_count",
		barmode="stack",
		color_discrete_sequence=px.colors.qualitative.Set2
	).update_layout(xaxis={'categoryorder':'array', 'categoryarray': state_order})))

	app.layout = html.Div(items)

	return app
