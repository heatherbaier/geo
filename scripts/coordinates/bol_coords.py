import geopandas as gpd
import pandas as pd


bol_ef = gpd.read_file("../../data/BOL/shp/EstabEducativos/EstabEducativos.shp")
bol_ef = bol_ef[["gml_id", "POINT_X", "POINT_Y"]]
bol_ef = bol_ef.reset_index()

ids = pd.read_csv("../../files_for_db/ids/bol_ids.csv")

bol_ef = bol_ef.rename(columns = {"gml_id": "deped_id", "POINT_X": "longitude", "POINT_Y": "latitude"})
bol_ef = pd.merge(bol_ef, ids, on = "deped_id")
bol_ef = bol_ef[["geo_id", "longitude", "latitude"]]

bol_ef = bol_ef[bol_ef["longitude"] != 0]
bol_ef = bol_ef[bol_ef["latitude"] != 0]

print(bol_ef.head())

bol_ef.to_csv("../../files_for_db/coordinates/bol_coordinates.csv", index = False)
