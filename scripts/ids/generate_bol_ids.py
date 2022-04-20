import geopandas as gpd
import pandas as pd


bol_ef = gpd.read_file("../../data/BOL/shp/EstabEducativos/EstabEducativos.shp")
bol_ef = bol_ef[["gml_id"]]
bol_ef = bol_ef.reset_index()
bol_ef['geo_id'] = bol_ef['index'].apply(lambda x: 'BOL-{0:0>6}'.format(x))
bol_ef["school_name"] = None
bol_ef = bol_ef[["geo_id", "gml_id", "school_name"]].rename(columns = {"gml_id": "deped_id"})

print(bol_ef.head())

bol_ef.to_csv("../../files_for_db/ids/bol_ids.csv", index = False)
