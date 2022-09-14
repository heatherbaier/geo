import geopandas as gpd
import pandas as pd

from utils import *


phl_ef = pd.read_csv("../../data/PHL/this_one.csv")
print(phl_ef.columns)
phl_ef = phl_ef[["school_id", "school_name", "longitude", "latitude", "region", "division", "province"]]
phl_ef = phl_ef.drop_duplicates(subset = ["school_id"])
phl_ef = phl_ef.reset_index()
phl_ef['geo_id'] = phl_ef['index'].apply(lambda x: 'PHL-{0:0>6}'.format(x))
phl_ef["adm0"] = "PHL"
phl_ef["address"] = None
phl_ef = phl_ef[["geo_id", "school_id", "school_name", "address", "adm0", "region", "division", "province"]].rename(columns = {"school_id": "deped_id", "region": "adm1", "division":"adm2", "province": "adm3"})
phl_ef = phl_ef[["geo_id","deped_id","school_name","address","adm0","adm1","adm2","adm3"]]

print(phl_ef.head())

phl_ef.to_csv("../../files_for_db/ids/phl_ids.csv", index = False)