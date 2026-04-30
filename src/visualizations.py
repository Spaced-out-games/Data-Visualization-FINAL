import pandas as pd
import numpy as np
import dash
import seaborn as sns
from dash import dcc, html
from data_prep import *



def make_dashboard(
	df: pd.DataFrame,
	state_df,
	name: str = "Cost Of Living Dashboard"
) -> dash.Dash:

	items = []

	app = dash.Dash(name)

	stacked_df = (
    df.groupby(["state", "family_member_count"])
      .size()
      .reset_index(name="count")
)

	# Normalize to percentages within each state
	stacked_df["percent"] = (
		stacked_df["count"] /
		stacked_df.groupby("state")["count"].transform("sum")
)

	state_order = (
		stacked_df.groupby("state")["count"]
		.sum()
		.sort_values(ascending=False)
		.index
	)

	# Title
	items.append(html.H1("Cost of Living"))


	# Housing Cost by State
	items.append(dcc.Graph(
		figure=px.histogram(state_df, "state", "housing_cost",title = "Housing Cost By State")
	))

	items.append(html.H1("Housing Cost By State"))
	items.append(html.Iframe(
		srcDoc=open(
			create_choropleth_map(
				load_state_geometries(),
				df,
				'state_full',
				'housing_cost',
				'feature.properties.name',
				[37.7749, -95.7129],
				4,
				legend_title='Housing Cost'
			),
			"r"
		).read(),
		width="1960",
		height="1080"
	))


	# Transportation cost by state
	items.append(dcc.Graph(
		figure=px.histogram(state_df, "state", "transportation_cost", title="Transportation Cost By State")
	))
	items.append(html.H1("Transportation Cost By State"))
	items.append(html.Iframe(
		srcDoc=open(
			create_choropleth_map(
				load_state_geometries(),
				df,
				'state_full',
				'transportation_cost',
				'feature.properties.name',
				[37.7749, -95.7129],
				4,
				legend_title='Transportation Cost'
			),
			"r"
		).read(),
		width="1960",
		height="1080"
	))


	# Healthcare cost by state
	items.append(dcc.Graph(
		figure=px.histogram(state_df, "state", "healthcare_cost", title ="Healthcare Cost By State")
	))
	items.append(html.H1("Healthcare Cost By State"))
	items.append(html.Iframe(
		srcDoc=open(
			create_choropleth_map(
				load_state_geometries(),
				df,
				'state_full',
				'healthcare_cost',
				'feature.properties.name',
				[37.7749, -95.7129],
				4,
				legend_title='Healthcare Cost'
			),
			"r"
		).read(),
		width="1960",
		height="1080"
	))

	# Childcare cost by state
	items.append(dcc.Graph(
		figure=px.histogram(state_df, "state", "childcare_cost", title ="Childcare Cost By State")
	))
	items.append(html.H1("Childcare Cost By State"))
	items.append(html.Iframe(
		srcDoc=open(
			create_choropleth_map(
				load_state_geometries(),
				df,
				'state_full',
				'childcare_cost',
				'feature.properties.name',
				[37.7749, -95.7129],
				4,
				legend_title='Childcare Cost'
			),
			"r"
		).read(),
		width="1960",
		height="1080"
	))




	# Taxes by state
	items.append(dcc.Graph(
		figure=px.histogram(state_df, "state", "taxes", title ="Taxes By State")
	))
	items.append(html.H1("Taxes By State"))
	items.append(html.Iframe(
		srcDoc=open(
			create_choropleth_map(
				load_state_geometries(),
				df,
				'state_full',
				'taxes',
				'feature.properties.name',
				[37.7749, -95.7129],
				4,
				legend_title='Taxes'
			),
			"r"
		).read(),
		width="1960",
		height="1080"
	))


	# Median income by state
	items.append(dcc.Graph(
		figure=px.histogram(state_df, "state", "median_family_income", title ="Median Income By State")
	))
	items.append(html.H1("Median Income By State"))
	items.append(html.Iframe(
		srcDoc=open(
			create_choropleth_map(
				load_state_geometries(),
				df,
				'state_full',
				'median_family_income',
				'feature.properties.name',
				[37.7749, -95.7129],
				4,
				legend_title='Median Income'
			),
			"r"
		).read(),
		width="1960",
		height="1080"
	))

	# This is meant to color-code the contribution of each 

	items.append(dcc.Graph(
    figure=px.bar(
        stacked_df,
        x="state",
        y="percent",  # <-- use percent instead of count
        color="family_member_count",
        barmode="stack",
        color_discrete_sequence=px.colors.qualitative.Set2,
    ).update_layout(
        xaxis={'categoryorder': 'array', 'categoryarray': state_order},
        yaxis_title="Proportion of Family Sizes"
    )
))
	
	summary_df = (
    stacked_df.groupby("family_member_count", as_index=False)["percent"]
    .mean()
)
	# test
	items.append(dcc.Graph(
		figure=px.pie(
			summary_df,
			names="family_member_count",
			values="percent",
			color="family_member_count",
			color_discrete_sequence=px.colors.qualitative.Set2,
		).update_layout(
			title="Average Family Size Distribution (Across States)"
		)
	))

	'''                 column           min           max          range          mean        median         mode      skew  outlier_count  outlier_pct
	0                  case_id      1.000000    3171.00000    3170.000000   1589.329726   1593.500000      1.00000 -0.005906              0     0.000000
	1             housing_cost   4209.311280   61735.58760   57526.276320  11073.359622  10416.000000   8808.00000  2.575029           1765     0.056174
	2                food_cost   2220.276840   31178.61960   28958.342760   8287.654372   8129.156280   3112.53768  0.317386             66     0.002101
	3      transportation_cost   2216.461440   19816.48200   17600.020560  13593.989839  13698.315000  14366.26920 -0.471037            227     0.007225
	4          healthcare_cost   3476.379960   37252.27440   33775.894440  13393.008581  13082.514000   5506.79004  0.446041            316     0.010057
	5   other_necessities_cost   2611.642080   28829.44320   26217.801120   7015.258917   6733.056120   4925.60592  1.166022            567     0.018046
	6           childcare_cost      0.000000   48831.08520   48831.085200   9879.247416  10166.340120      0.00000  0.302431            272     0.008657
	7                    taxes   1027.800756   47753.39040   46725.589644   7657.101541   6897.747780   6914.53932  2.603167           1506     0.047931
	8               total_cost  30087.662400  223717.54800  193629.885600  70899.620274  70974.249000  35171.52840  0.483501            240     0.007638
	9     median_family_income  25529.976562  177662.46875  152132.492188  68315.997017  65955.605469  62893.09375  1.268878           1180     0.037556
	10                 parents      1.000000       2.00000       1.000000      1.500000      1.500000      1.00000  0.000000              0     0.000000
	11                children      0.000000       4.00000       4.000000      2.000000      2.000000      0.00000  0.000000              0     0.000000
	12             family_size      1.000000       6.00000       5.000000      3.500000      3.500000      2.00000  0.000000              0     0.000000

	'''
	items.append(dcc.Graph(
		figure=px.scatter(
			state_df,
			x="total_cost",
			y="transportation_cost",
			color="state",
			labels={
				"total_cost": "Total Cost",
				"transportation_cost": "Transportation Cost (USD/Household)"
			},
			title="Average Total Expenditures vs Transportation Costs"
		)
	))

	items.append(dcc.Graph(
		figure=px.scatter(
			state_df,
			x="childcare_cost",
			y="taxes",
			color="state",
			labels={
				"childcare_cost": "Childcare Cost (USD/Household)",
				"taxes": "Taxes (USD/Household)"
			},
			title="Average Childcare Expenditures vs Taxes"
		)
	))

	items.append(dcc.Graph(
		figure=px.scatter(
			state_df,
			x="median_family_income",
			y="taxes",
			color="state",
			labels={
				"median_family_income": "Median Family Income (USD)",
				"taxes": "Taxes (USD/Household)"
			},
			title="Average Income vs Taxes"
		)
	))

	items.append(dcc.Graph(
		figure=px.scatter(
			state_df,
			x="housing_cost",
			y="taxes",
			color="state",
			labels={
				"housing_cost": "Housing Cost (USD/Household)",
				"taxes": "Taxes (USD/Household)"
			},
			title="Housing Cost vs Taxes"
		)
	))

	items.append(dcc.Graph(
		figure=px.scatter(
			state_df,
			x="total_cost",
			y="taxes",
			trendline="ols",
			labels={
				"total_cost": "Total Expenditures By Household",
				"taxes": "Taxes (USD/Household)"
			},
			title="Total Expenditures vs Taxes"
		)
	))


	


	childcare_sorted_df = (
		df.groupby("county", as_index=False)["childcare_cost"]
		  .mean()
		  .sort_values("childcare_cost", ascending=False)
		  .head(12)
	)

	tax_sorted_df = (
		df.groupby("county", as_index=False)["taxes"]
		  .mean()
		  .sort_values("taxes", ascending=False)
		  .head(12)
	)

	corr_df = pd.DataFrame()

	corr_df = df.copy()

	corr_df.drop(columns=["case_id", "state", "isMetro", "areaname", "county", "family_member_count", "state_full","parents","children","is_foodcost_outlier"], inplace=True, errors="ignore")

	print(corr_df.keys())

	# corr_df["childcare_cost"] = df["childcare_cost"]
	# corr_df["housing_cost"] = df["housing_cost"]
	#corr_df["taxes"] = df["taxes"]

	corr = corr_df.corr()


	# do not remove; this auto-sorts
	items.append(dcc.Graph(
		figure=make_barchart_fig(childcare_sorted_df, "county", "childcare_cost",
								"Top 12 Highest Childcare Cost Counties")
	))

	items.append(dcc.Graph(
		figure=make_barchart_fig(tax_sorted_df, "county", "taxes",
								"Top 12 Highest-Tax Counties")
	))


	# items.append(dcc.Graph(
		# figure=sns.heatmap(corr_df.corr(), annot=True)
		# figure=px.density_heatmap(
		# 	corr_df,
		# 	x="childcare_cost",
		# 	y="housing_cost",
		# 	z="taxes",
		# 	histfunc="avg"
		# )
	# ))

	items.append(dcc.Graph(
    figure=go.Figure(
        data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale="RdBu",
            zmin=-1,
            zmax=1
        )
    )
	))
	
	items.append(dcc.Graph(
		figure=px.scatter(
			state_df,
			x="family_size",
			y="taxes",
			trendline="ols",
			labels={
				"family_size": "Number of people per household",
				"taxes": "Taxes (USD/Household)"
			},
			title="Family Size vs Taxes"
		)
	))

	items.append(dcc.Graph(
		figure=px.scatter(
			df,
			x="food_cost",
			y="taxes",
			size="childcare_cost",
			color="isMetro",
			labels={
				"food_cost": "Annual cost of food per household",
				"taxes": "Taxes (USD/Household)"
			},
			title="Childcare cost vs Number Of Children"
		)
	))

	items.append(dcc.Graph(
		figure=px.scatter(
			df,
			x="housing_cost",
			y="taxes",
			size="transportation_cost",
			color="state",
			labels={
				"housing_cost": "Annual Cost of Housing Per household",
				"taxes": "Taxes (USD/Household)"
			},
			title="Childcare cost vs Number Of Children"
		)
	))

	items.append(dcc.Graph(figure = px.scatter_3d(
		state_df,
		x = "transportation_cost",
		y = "healthcare_cost",
		z = "taxes"
	)))

	items.append(dcc.Graph(figure = px.scatter_3d(
		state_df,
		x = "childcare_cost",
		y = "taxes",
		z = "median_family_income"
	)))

	#TODO: Add PCA & NMF graphs / integrate PCA/NMF

	app.layout = html.Div(items)

	return app
