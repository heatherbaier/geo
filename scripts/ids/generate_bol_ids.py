import geopandas as gpd
import pandas as pd

from utils import *


bol_ef = gpd.read_file("../../data/BOL/shp/EstabEducativos/EstabEducativos.shp")
bol_ef = bol_ef[["gml_id", "POINT_X", "POINT_Y"]].rename(columns = {"POINT_Y": "latitude", "POINT_X": "longitude"})
print(bol_ef.head())

print(bol_ef.shape)
bol_ef = bol_ef.drop_duplicates(subset = ["gml_id"])
bol_ef = bol_ef.drop_duplicates(subset = ["latitude", "longitude"])

print(bol_ef.shape)



bol_ef = bol_ef.reset_index()
bol_ef['geo_id'] = bol_ef['index'].apply(lambda x: 'BOL-{0:0>6}'.format(x))
bol_ef["school_name"] = None
bol_ef = bol_ef[["geo_id", "gml_id", "school_name", "latitude", "longitude"]].rename(columns = {"gml_id": "deped_id"})
bol_ef["address"] = None
bol_ef["adm0"] = "BOL"
print(bol_ef.head())

# print(bol_ef["geo_id"].value_counts())

# agad

# Geocode to ADM levels
cols = ["geo_id", "deped_id", "school_name", "longitude", "latitude", "address", "adm0"]
for adm in range(1, 4):

    try:

        cols += ["adm" + str(adm)]
        downloadGB("BOL", str(adm), "../../gb")
        shp = gpd.read_file(getGBpath("BOL", str(adm), "../../gb"))
        bol_ef = gpd.GeoDataFrame(bol_ef, geometry = gpd.points_from_xy(bol_ef.longitude, bol_ef.latitude))
        bol_ef = gpd.tools.sjoin(bol_ef, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        print(bol_ef)

    except Exception as e:

        bol_ef["adm" + str(adm)] = None
        print(e)

bol_ef = bol_ef[cols].drop(["longitude", "latitude"], axis = 1)

print(bol_ef.head())

print(bol_ef.shape)



bol_ef.to_csv("../../files_for_db/ids/bol_ids.csv", index = False)
