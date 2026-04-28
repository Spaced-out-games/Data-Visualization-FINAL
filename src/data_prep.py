import os
import json
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
	df['state_full'] = df['state'].map(STATE_FULLNAME_LOOKUP)
	df = dataset.dropna()
	total_null_entries = np.sum(df.isnull().sum())
	if(bool(total_null_entries != 0)):
		print(f"ERROR: no null values assertion failed. Total null entries: {total_null_entries}")
		return None
	return df

def load_state_geometries():
	with urlopen(STATE_GEOMETRIES_URL) as response:
    	state_geometries = json.load(response)
	return state_geometries


