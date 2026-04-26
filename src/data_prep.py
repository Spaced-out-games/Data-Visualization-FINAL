import os

print (f"Current working directory: {os.getcwd()}")

# import processing libraries
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA, TruncatedSVD, NMF

# Whether or not this project is being run on a local machine or in a Colab notebook 
LOCAL_ENV = True
DATASET_DIR = None
DATASET_FILENAME = "cost_of_living_us.csv"
if(not LOCAL_ENV):
	from google.colab import drive
	drive.mount('/content/drive')
	DATASET_DIR = "/content/drive/MyDrive/datasets/"
else:
	DATASET_DIR = "data/"




def load_dataset(dataset_name: str) -> pd.DataFrame:

	filename: str = f'{DATASET_DIR}{dataset_name}'
	print(f"Loading file {filename}...")
	df: pd.DataFrame = pd.read_csv(filename)
	df.dropna(inplace=True)
	total_null_entries = np.sum(df.isnull().sum())
	if(bool(total_null_entries != 0)):
		print(f"ERROR: no null values assertion failed. Total null entries: {total_null_entries}")






if __name__ == '__main__':
	df = load_dataset(DATASET_FILENAME)
	df.head()
else:
	print("test failed")
