
from visualizations import make_dashboard
from data_prep import clean_dataset, load_dataset, parse_family_size

if __name__ == "__main__":
	# first things first, clean the dataset
	df = clean_dataset(load_dataset("cost_of_living_us.csv"))
	df["family_size_numeric"] = df["family_member_count"].apply(parse_family_size)

	stacked_df = (
	df.groupby(["state", "family_member_count"])
	  .size()
	  .reset_index(name="count")
	  
	)

	state_df = (
    df.groupby(["state", "state_full"], as_index=False)
      .agg({
          "housing_cost": "mean",
          "food_cost": "mean",
          "transportation_cost": "mean",
          "healthcare_cost": "mean",
          "other_necessities_cost": "mean",
          "childcare_cost": "mean",
          "taxes": "mean",
          "total_cost": "mean",
          "median_family_income": "mean",
      })
)
	


	stacked_df = stacked_df.sort_values(["state", "family_member_count"])
	state_order = (
		stacked_df.groupby("state")["count"]
		.sum()
		.sort_values(ascending=False)
		.index
	)

	print(df.head())

	dashboard = make_dashboard(df, state_df, "Cost Of Living Dashboard")

	dashboard.run(debug=True)
