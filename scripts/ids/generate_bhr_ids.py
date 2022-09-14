from pandas.io.json import json_normalize
import geopandas as gpd
import pandas as pd

from utils import *


bhr_ef = pd.read_csv("../../data/BHR/bahrain_school_locations.csv")
bhr_ef = bhr_ef[bhr_ef["SUBTYPE EN"].isin(["KINDERGARTEN", "PUBLIC SCHOOLS - BOYS", "PUBLIC SCHOOLS - GIRLS"])]
bhr_ef = bhr_ef[["NAME", "#", "POINT_X_Longitude", "POINT_Y_Latitude"]]
bhr_ef = bhr_ef.reset_index()
bhr_ef['geo_id'] = bhr_ef['index'].apply(lambda x: 'BHR-{0:0>6}'.format(x))
bhr_ef = bhr_ef.drop(["index"], axis = 1)
bhr_ef = bhr_ef[["geo_id", "#", "NAME", "POINT_X_Longitude", "POINT_Y_Latitude"]].rename(columns = {"#": "deped_id", "NAME": "school_name", "POINT_X_Longitude": "longitude", "POINT_Y_Latitude": "latitude"})
bhr_ef["address"] = None
bhr_ef["adm0"] = "BHR"
print(bhr_ef.head())

# Geocode to ADM levels
cols = ["geo_id", "deped_id", "school_name", "longitude", "latitude", "address", "adm0"]
for adm in range(1, 4):

    try:

        cols += ["adm" + str(adm)]
        downloadGB("BHR", str(adm), "../../gb")
        shp = gpd.read_file(getGBpath("BHR", str(adm), "../../gb"))
        bhr_ef = gpd.GeoDataFrame(bhr_ef, geometry = gpd.points_from_xy(bhr_ef.longitude, bhr_ef.latitude))
        bhr_ef = gpd.tools.sjoin(bhr_ef, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        print(bhr_ef)

    except Exception as e:

        bhr_ef["adm" + str(adm)] = None
        print(e)

bhr_ef = bhr_ef[cols].drop(["longitude", "latitude"], axis = 1)

bhr_ef.to_csv("../../files_for_db/ids/bhr_ids.csv", index = False)
