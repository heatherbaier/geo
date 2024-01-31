import geopandas as gpd
import pandas as pd
import os

from utils import *


iso = "TZA"
tan_ef = pd.read_csv("/Users/heatherbaier/Documents/geo_git/files_for_db/ids/tan_ids.csv")
tan_ef["adm0"] = iso
tan_ef["address"] = None

print(tan_ef.head())

coords = pd.read_csv("/Users/heatherbaier/Documents/geo_git/files_for_db/coordinates/tan_coordinates.csv")
tan_ef = pd.merge(tan_ef, coords, on = "geo_id")

print(tan_ef.head())


longs = tan_ef["longitude"].values
lats = tan_ef["latitude"].values

# Geocode to ADM levels
cols = ["geo_id", "deped_id", "school_name", "adm0", "address"]
for adm in range(1, 4):

    try:

        cols += ["adm" + str(adm)]
        downloadGB(iso, str(adm), "../../gb")
        shp = gpd.read_file(getGBpath(iso, f"ADM{str(adm)}", "../../gb"))
        tan_ef = gpd.GeoDataFrame(tan_ef, geometry = gpd.points_from_xy(tan_ef.longitude, tan_ef.latitude))
        tan_ef = gpd.tools.sjoin(tan_ef, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        tan_ef["longitude"] = longs
        tan_ef["latitude"] = lats
        print(tan_ef.head())


    except Exception as e:

        tan_ef["adm" + str(adm)] = None
        print(e)

tan_ef = tan_ef[["geo_id", "deped_id", "school_name", "address", "adm0", "adm1", "adm2", "adm3"]]

# tan_ef = tan_ef[cols].drop(["longitude", "latitude"], axis = 1)

tan_ef.to_csv("/Users/heatherbaier/Documents/geo_git/files_for_db/basic/tan_basic.csv", index = False)

