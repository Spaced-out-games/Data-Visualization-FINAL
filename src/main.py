
from visualizations import make_dashboard
from data_prep import *

if __name__ == "__main__":
	# first things first, clean the dataset
	df = clean_dataset(load_dataset("cost_of_living_us.csv"))

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


	# secondary attempt
	numeric_cols = df.select_dtypes(include=np.number).columns
	state_df = (
    df.groupby(["state", "state_full"], as_index=False)[numeric_cols]
      .median()
)

	Q1 = state_df["food_cost"].quantile(0.25)
	Q3 = state_df["food_cost"].quantile(0.75)
	IQR = Q3 - Q1
	lower = Q1 - 1.5 * IQR
	upper = Q3 + 1.5 * IQR

	state_df["is_foodcost_outlier"] = (state_df["food_cost"] < lower) | (state_df["food_cost"] > upper)
	


	stacked_df = stacked_df.sort_values(["state", "family_member_count"])
	state_order = (
		stacked_df.groupby("state")["count"]
		.sum()
		.sort_values(ascending=False)
		.index
	)




	dashboard = make_dashboard(df, state_df, "Cost Of Living Dashboard")

	

	print(df) # [df if df["is_foodcost_outlier"]]

	dashboard.run(debug=True)
