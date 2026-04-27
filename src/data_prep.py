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
	df = dataset.dropna()
	total_null_entries = np.sum(df.isnull().sum())
	if(bool(total_null_entries != 0)):
		print(f"ERROR: no null values assertion failed. Total null entries: {total_null_entries}")
		return None
	return df



