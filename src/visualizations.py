import pandas as pd
import numpy as np
import dash
import seaborn as sns
from dash import dcc, html
from data_prep import *


from itertools import count

fig_counter = count(1)

def next_fig():
    return next(fig_counter)


def build_housing_section(state_df, df, geometries):
	items = []

	items.append(html.H1("Housing"))
	items.append(html.H2(f"Figure {next_fig()}"))
	items.append(dcc.Graph(
	   figure=px.histogram(state_df, x="housing_cost", nbins=50)
	))

	items.append(html.H2(f"Figure {next_fig()}"))
	items.append(html.Iframe(
	   srcDoc=open(create_choropleth_map(
		  geometries, df, 'state_full', 'housing_cost',
		  'feature.properties.name', [37.7749, -95.7129], 4
	   )).read(),
	   width="800", height="480"
	))

	items.append(html.H2(f"Figure {next_fig()}"))
	items.append(dcc.Graph(
	   figure=px.scatter(state_df, x="housing_cost", y="taxes", color="state")
	))

	return items

def build_transportation_section(state_df, df, geometries):
	items = []

	items.append(html.H1("Transportation"))

	items.append(html.H2(f"Figure {next_fig()}"))
	items.append(dcc.Graph(
	   figure=px.histogram(state_df, x="transportation_cost", nbins=50)
	))

	items.append(html.H2(f"Figure {next_fig()}"))
	items.append(html.Iframe(
	   srcDoc=open(create_choropleth_map(
		  geometries, df, 'state_full', 'transportation_cost',
		  'feature.properties.name', [37.7749, -95.7129], 4
	   )).read(),
	   width="800", height="480"
	))

	items.append(html.H2(f"Figure {next_fig()}"))
	items.append(dcc.Graph(
	   figure=px.scatter(
		  state_df,
		  x="transportation_cost",
		  y="total_cost",
		  trendline="ols"
	   )
	))

	return items

def build_healthcare_section(state_df, df, geometries):
	items = []

	items.append(html.H1("Healthcare"))

	items.append(html.H2(f"Figure {next_fig()}"))
	items.append(dcc.Graph(
	   figure=px.histogram(state_df, x="healthcare_cost", nbins=50)
	))

	items.append(html.H2(f"Figure {next_fig()}"))
	items.append(html.Iframe(
	   srcDoc=open(create_choropleth_map(
		  geometries, df, 'state_full', 'healthcare_cost',
		  'feature.properties.name', [37.7749, -95.7129], 4
	   )).read(),
	   width="800", height="480"
	))

	return items

def build_income_section(state_df, df, geometries):
	items = []

	items.append(html.H1("Income"))
	items.append(html.H2(f"Figure {next_fig()}"))
	items.append(dcc.Graph(
	   figure=px.box(state_df, x="state", y="median_family_income")
	))
	items.append(html.H2(f"Figure {next_fig()}"))
	items.append(html.Iframe(
	   srcDoc=open(create_choropleth_map(
		  geometries, df, 'state_full', 'median_family_income',
		  'feature.properties.name', [37.7749, -95.7129], 4
	   )).read(),
	   width="800", height="480"
	))

	return items

def build_childcare_section(state_df, df, geometries, childcare_sorted_df):
	items = []

	items.append(html.H1("Childcare"))
	items.append(html.H2(f"Figure {next_fig()}"))
	items.append(html.Iframe(
	   srcDoc=open(create_choropleth_map(
		  geometries, df, 'state_full', 'childcare_cost',
		  'feature.properties.name', [37.7749, -95.7129], 4
	   )).read(),
	   width="800", height="480"
	))
	items.append(html.H2(f"Figure {next_fig()}"))
	items.append(dcc.Graph(
	   figure=make_barchart_fig(
		  childcare_sorted_df,
		  "county",
		  "childcare_cost",
		  "Top 12 Highest Childcare Cost Counties"
	   )
	))

	return items

def build_tax_section(state_df, df, geometries, tax_sorted_df):
	items = []

	items.append(html.H1("Taxes"))
	items.append(html.H2(f"Figure {next_fig()}"))
	items.append(dcc.Graph(
	   figure=px.histogram(state_df, "state", "taxes")
	))
	items.append(html.H2(f"Figure {next_fig()}"))
	items.append(html.Iframe(
	   srcDoc=open(create_choropleth_map(
		  geometries, df, 'state_full', 'taxes',
		  'feature.properties.name', [37.7749, -95.7129], 4
	   )).read(),
	   width="800", height="480"
	))
	items.append(html.H2(f"Figure {next_fig()}"))
	items.append(dcc.Graph(
	   figure=make_barchart_fig(
		  tax_sorted_df,
		  "county",
		  "taxes",
		  "Top 12 Highest-Tax Counties"
	   )
	))

	return items

def build_summary_section(state_df, corr):
	items = []
	items.append(html.H1("Summary"))
	items.append(html.H2(f"Figure {next_fig()}"))
	items.append(dcc.Graph(
	   figure=px.scatter(state_df, x="total_cost", y="taxes", trendline="ols")
	))

	items.append(html.H2(f"Figure {next_fig()}"))
	items.append(dcc.Graph(
	   figure=go.Figure(
		  data=go.Heatmap(
			 z=corr.values,
			 x=corr.columns,
			 y=corr.columns
		  )
	   )
	))

	return items

def build_title():
	items = []
	items.append(html.H1("Report on The Cost of Living (US)"))
	items.append(html.H2("By Devin Frost"))
	return items


def build_analysis():
	items = []
	
	# Analysis 
	housing_p = """
	Housing. We all need it, whether we are high up in the mountains of Appalachia or in the Great Plains - to simply survive. Figure 1 is a histogram that shows the typical annual cost of housing per state. Figure 2 shows housing prices by state. and as you can see, housing prices are generally highest near the coasts, and lowest in the Midwest and Southeast.
	Hawaii, being a small slice of Heaven on Earth, naturally has the highest housing prices, with a median of 61k / year. Country-wide it floats at a median of $10,400 each year.
	"""
	items.append(html.P(housing_p))


	transportation_p = """
	A well-functioning economy depends on cheap transportation to move goods, services, and people to where the demand is.
	Figure 3 shows the distribution curve of transportation costs across America. As you can see, the graph is left skewed,
	which, as shown by Figure 4 is due the the outlier, Washington, D.C., which has an impressively cheap $8,500 annual
	cost of transportation.
	"""
	items.append(html.P(transportation_p))



	return items

def build_conclusion():
	items = []
	return items












def make_dashboard(
	df: pd.DataFrame,
	state_df,
	name: str = "Cost Of Living Dashboard"
) -> dash.Dash:

	items = []
	state_df["affordability"] = state_df["total_cost"] / state_df["median_family_income"]

	print(state_df["affordability"])

	geometries = load_state_geometries()

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

	summary_df = (
		stacked_df.groupby("family_member_count", as_index=False)["percent"]
		.mean()
	)

	state_order = (
		stacked_df.groupby("state")["count"]
		.sum()
		.sort_values(ascending=False)
		.index
	)

	family_df = (
		df.groupby("family_member_count", as_index=False)
		.mean(numeric_only=True)
	)




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

	corr = corr_df.corr()


	# Title
	items += build_title()

	items += build_analysis()

	items += build_conclusion()

	# Sections
	items += build_housing_section(state_df, df, geometries)
	items += build_transportation_section(state_df, df, geometries)
	items += build_healthcare_section(state_df, df, geometries)
	items += build_income_section(state_df, df, geometries)
	items += build_childcare_section(state_df, df, geometries, childcare_sorted_df)
	items += build_tax_section(state_df, df, geometries, tax_sorted_df)
	items += build_summary_section(state_df, corr)

	app.layout = html.Div(items)
	return app

	# for reference
	'''			  column		 min		 max		range		mean	   median		mode	 skew  outlier_count  outlier_pct
	0			   case_id	 1.000000	3171.00000	3170.000000   1589.329726   1593.500000	 1.00000 -0.005906			0	0.000000
	1		   housing_cost   4209.311280   61735.58760   57526.276320  11073.359622  10416.000000   8808.00000  2.575029		 1765	0.056174
	2			 food_cost   2220.276840   31178.61960   28958.342760   8287.654372   8129.156280   3112.53768  0.317386		   66	0.002101
	3	 transportation_cost   2216.461440   19816.48200   17600.020560  13593.989839  13698.315000  14366.26920 -0.471037		  227	0.007225
	4		healthcare_cost   3476.379960   37252.27440   33775.894440  13393.008581  13082.514000   5506.79004  0.446041		  316	0.010057
	5   other_necessities_cost   2611.642080   28829.44320   26217.801120   7015.258917   6733.056120   4925.60592  1.166022		  567	0.018046
	6		 childcare_cost	 0.000000   48831.08520   48831.085200   9879.247416  10166.340120	 0.00000  0.302431		  272	0.008657
	7				taxes   1027.800756   47753.39040   46725.589644   7657.101541   6897.747780   6914.53932  2.603167		 1506	0.047931
	8			total_cost  30087.662400  223717.54800  193629.885600  70899.620274  70974.249000  35171.52840  0.483501		  240	0.007638
	9	median_family_income  25529.976562  177662.46875  152132.492188  68315.997017  65955.605469  62893.09375  1.268878		 1180	0.037556
	10			  parents	 1.000000	  2.00000	  1.000000	 1.500000	 1.500000	 1.00000  0.000000			0	0.000000
	11			 children	 0.000000	  4.00000	  4.000000	 2.000000	 2.000000	 0.00000  0.000000			0	0.000000
	12		   family_size	 1.000000	  6.00000	  5.000000	 3.500000	 3.500000	 2.00000  0.000000			0	0.000000

	'''
