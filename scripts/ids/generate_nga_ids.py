import geopandas as gpd
import pandas as pd

from utils import *


nig_ef = pd.read_csv("../../data/NGA/educational-facilities-in-nigeria.csv")
nig_ef = nig_ef[["facility_name", "longitude", "latitude"]]

print(nig_ef.shape)
nig_ef = nig_ef.drop_duplicates(subset = ["longitude", "latitude"])
print(nig_ef.shape)


# dgasa


nig_ef = nig_ef.reset_index()
nig_ef['geo_id'] = nig_ef['index'].apply(lambda x: 'NIG-{0:0>6}'.format(x))
nig_ef["deped_id"] = None
nig_ef = nig_ef[["geo_id", "deped_id", "facility_name", "longitude", "latitude"]]
nig_ef = nig_ef.rename(columns = {"facility_name":"school_name"})
nig_ef["address"] = None
nig_ef["adm0"] = "NGA"

print(nig_ef.head())

print(nig_ef.shape)



# agfdag

# Geocode to ADM levels
cols = ["geo_id", "deped_id", "school_name", "longitude", "latitude", "address", "adm0"]
for adm in range(1, 4):

    try:

        cols += ["adm" + str(adm)]
        downloadGB("NGA", str(adm), "../../gb")
        shp = gpd.read_file(getGBpath("NGA", str(adm), "../../gb"))
        nig_ef = gpd.GeoDataFrame(nig_ef, geometry = gpd.points_from_xy(nig_ef.longitude, nig_ef.latitude))
        nig_ef = gpd.tools.sjoin(nig_ef, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        print(nig_ef)

    except Exception as e:

        nig_ef["adm" + str(adm)] = None
        print(e)


nig_ef = nig_ef[cols].drop(["longitude", "latitude"], axis = 1)

print(nig_ef)

print(nig_ef.shape)

nig_ef.to_csv("../../files_for_db/ids/nga_ids.csv", index = False)
