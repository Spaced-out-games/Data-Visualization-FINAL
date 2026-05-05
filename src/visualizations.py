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

	items.append(html.H2(f"*Figure {next_fig()}"))
	items.append(dcc.Graph(
	   figure=px.histogram(state_df, x="transportation_cost", nbins=50)
	))

	items.append(html.H2(f"*Figure {next_fig()}"))
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
	   figure=px.box(df, x="state", y="median_family_income")
	))
	items.append(html.H2(f"Figure {next_fig()}"))
	items.append(html.Iframe(
	   srcDoc=open(create_choropleth_map(
		  geometries, df, 'state_full', 'median_family_income',
		  'feature.properties.name', [37.7749, -95.7129], 4
	   )).read(),
	   width="800", height="480"
	))

	items.append(html.H2(f"Figure {next_fig()}"))
	items.append(
		dcc.Graph(

			figure = px.histogram(
				state_df,
				x="median_family_income",
				y="taxes",
				color = "state",
				nbins=60
			)
		)
	)

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
	items.append(html.H2(f"Figure {next_fig()}"))
	items.append(
		dcc.Graph(

			figure = px.histogram(
				state_df,
				x="childcare_cost",
				y="taxes",
				color = "state",
				nbins=35
			)
		)
	)

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

def build_summary_section(df, state_df, corr):
	items = []

	#items.append(dcc.Graph(go.Figure(data=[go.Table(
    #header=dict(values=["areaname", "county", "median_family_income"],
    #            fill_color='paleturquoise',
    #            align='left'),
    #cells=dict(values=[df.areaname, df.county, df.median_family_income],
    #           fill_color='lavender',
    #           align='left'))
	#])))


	items.append(html.H1("Summary"))

	# 10.
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
	
	items.append(html.H2(f"Figure {next_fig()}"))
	items.append(
		dcc.Graph(
			figure=go.Figure(
				data=[go.Table(
					header=dict(
						values=list(df.columns),
						fill_color='paleturquoise',
						align='left'
					),
					cells=dict(
						values=[df[col] for col in df.columns],
						fill_color='lavender',
						align='left'
					)
				)]
			),
			config={"displayModeBar": False}
		)
	)

	return items

def build_title():
	items = []
	items.append(html.H1("Report on The Cost of Living (US)"))
	items.append(html.H2("By Devin Frost"))
	return items


def build_analysis():
	items = []

	intro = """
	In recent years, the US economy has been hit hard by multiple economic crises, from global pandemics to supply chain shocks to wars, and naturally, the expenditure of resources to combat these crises has negatively impacted the cost of living in the US. This report takes a holistic look into the cost of living in the United States, using data from the
	Economic Policy Institute (EPI) In order to understand the state of the US economy, we first need to measure the cost of living, then normalize it in accordance to median incomes in order to gauge regional affordability. 
	"""
	items.append(html.P(intro))

	data_prep = """
	To prepare my data for this analysis, I dropped rows with null values to simplify the analysis process. It only meant losing 10 records, which should not meaningfully offset the value of this analysis.
	I also synthesized numerous measures using the dataset. The dataset gives a simple 'family_member_count' feild, which isn't provided as a numerical value. I parse the values into the `parents` and `children` feilds.
	Further, I sum these up into a `family_size` value. In order to measure the affordability of a region, I take total expenditures and divide it by median income, to normalize the values.
	
	
	"""
	items.append(html.P(data_prep))
	

	childcare = """
	The family unit is not complete without children, and in the modern, fast-paced world, childcare is a necessity.  Figure 1 is a map of 
	childcare costs by state. Childcare costs have considerable variation across the states. Figure 2 is a bar chart of the top 12 most
	expensive counties in which to raise a child. It includes counties from New York and the District of Columbia.
	"""
	items.append(html.P(childcare))

	# Analysis 
	housing = """
	Housing. We all need it, whether we are high up in the mountains of Appalachia or in the Great Plains - to simply survive the elements.
	Figure 4 is a histogram that shows the typical annual cost of housing per state. Figure 5 shows housing prices by state on a map,
	and as you can see, housing prices are generally highest near the coasts, and lowest in the Midwest and Southeast. Hawaii, being a small
	slice of Heaven on Earth, naturally has the highest housing prices, with a median of 61k / year. Country-wide it floats at a median of
	$10,400 each year. Figure 6 is a scatterplot of housing prices versus taxes, and suggests that higher housing costs is positively correlated
	with higher taxes, which is likely due to property tax law.
	"""
	items.append(html.P(housing))

	transportation = """
	A well-functioning economy depends on cheap transportation to move goods, services, and people to where the demand is.
	Figure 7 shows the distribution curve of transportation costs across America. As you can see, the graph is left skewed
	with a median of approximately $13,800 a year, which, as shown by Figure 8 is due the the outlier Washington, D.C.,
	where transportation is cheap. Figure 9 is a regression plot of transportation cost versus total expenditures, and it
	shows that transportation costs are negatively correlated with total costs. This may indicate that cheaper transportation
	leads to more economic growth and therefore higher paying jobs and cost of living
	"""
	items.append(html.P(transportation))

	healthcare = """
	Our quality of life is impacted largely by our health, and consequently, regions with high healthcare costs are
	indicative of regions that struggle to meet a standard of living. Figure 10 is a histogram of the distribution of healthcare
	expenditures accross the country. It is somewhat right-skewed, but is largely normally distributed. Figure 11 shows that West
	Virginia is by far the most expensive place to pay for healthcare, with a median price of $37,000 annually. It is reflective of
	poor policy decisions in the region. 
	"""
	items.append(html.P(healthcare))

	





	


	taxes = """
	Unfortunately, in order to organize society, any state needs a government, and any government needs tax dollars to power programs that
	power public infrustructure and social programs. Figure 12 is a bar chart of taxes by state, and Figure 13 is a map thereof. As shown
	by the map, Oregan and Washington, DC have some of the highest taxes in the country. Figure 14 is a bar chart of the top 12 highest-tax
	counties in the country. Counties from New York and Washington, D.C have the highest taxes of any region in the United States
	"""
	items.append(html.P(taxes))



	income = """
	In order to pay for all of this, people naturally need sturdy, competitive incomes. Figure 15 is a boxplot of median household
	incomes across the counties of the 50 United States, plus the District of Columbia, and it shows that incomes across the state are
	highly variable, ranging from $27,000 in Georgia, up to $177k in Virginia. Virginia was by far the most riddled with inter-county
	income inequality. Deleware had the least variation. Figure 16 better conveys this information geographically. Figure 17 is a histogram
	of median family incomes by state and it is evident that the median wage in the US is approximately $70,000 a year.

	"""
	items.append(html.P(income))
	return items

def build_conclusion():
	items = []
	income = """
	Figure 19 is a correlation matrix between each of the aforementioned factors and concludes that family size is highly
	correlated with the cost of food and healthcare, that total costs are highly correlated with the cost of food and the cost of
	extraneus necessities, and, interestingly, housing costs are correlated with extraneuss necessity expenditures. Figure 18 shows
	that total expenditures are positively correlated with higher taxes. A small table is provided to illustrate the data that were
	provided by the Economic Policy Institute (EPI), including the aforementioned feilds `parents`, `children`, `family_size`, and
	`is_foodcost_outlier`.
	"""
	items.append(html.P(income))
	return items












def make_dashboard(df, state_df, name = "Cost Of Living Dashboard") -> dash.Dash:

	items = []
	state_df["affordability"] = state_df["total_cost"] / state_df["median_family_income"]


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
	items += build_childcare_section(state_df, df, geometries, childcare_sorted_df)
	items += build_housing_section(state_df, df, geometries)
	items += build_transportation_section(state_df, df, geometries)
	items += build_healthcare_section(state_df, df, geometries)
	items += build_tax_section(state_df, df, geometries, tax_sorted_df)
	items += build_income_section(state_df, df, geometries)
	items += build_summary_section(df, state_df, corr)

	app.layout = html.Div(items)
	return app

	# for my reference
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
