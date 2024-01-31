import pandas as pd

#import necessary data from github
slv_table = pd.read_excel("../../data/SLV/el_salv_coordinates.xlsx")
slv_ids = pd.read_csv("../../data/SLV/slv_ids.csv")

#select necessary columns
slv_table = slv_table[["School Code", "lat", "lng"]]
slv_table.columns = ["country_id", "latitude", "longitude"]

#merge with id table to get geo_ids
slv_table["country_id"] = slv_table["country_id"].astype("str")
slv_table = pd.merge(slv_table, slv_ids, how = "inner")

#final formatting
slv_table = slv_table[["geo_id", "longitude", "latitude"]]

#export as csv
# slv_table.to_csv("../../files_for_db/coordinates/slv_coordinates.csv", index=False)