import pandas as pd
import numpy as np

#import necessary data from github
zaf_table = pd.read_excel("../../data/ZAF/National.xlsx")
zaf_ids = pd.read_csv("../../files_for_db/ids/zaf_ids.csv")

#select and rename necessary columns
zaf_table = zaf_table[["NatEmis", "GIS_Long", "GIS_Lat"]]
zaf_table.columns = ["country_id", "longitude", "latitude"]

#specify column types for merge
zaf_table["country_id"] = zaf_table["country_id"].astype("str")
zaf_ids["country_id"] = zaf_ids["country_id"].astype("str")
zaf_table = pd.merge(zaf_table, zaf_ids)

#select final columns
zaf_table = zaf_table[["geo_id", "longitude", "latitude"]]

#export csv
zaf_table.to_csv("../../files_for_db/coordinates/zaf_coordinates.csv", index=False)