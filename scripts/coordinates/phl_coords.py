import pandas as pd


phl_ef = pd.read_csv("../../data/PHL/this_one.csv")
phl_ef = phl_ef[["school_id", "longitude", "latitude"]]

ids = pd.read_csv("../../files_for_db/ids/phl_ids.csv")

print(ids.head())

phl_ef = phl_ef.rename(columns = {"school_id": "deped_id"})
phl_ef = pd.merge(phl_ef, ids, on = "deped_id")

phl_ef = phl_ef[["geo_id", "longitude", "latitude"]]

phl_ef = phl_ef[phl_ef["longitude"] != 0]
phl_ef = phl_ef[phl_ef["latitude"] != 0]

print(phl_ef.head())

phl_ef.to_csv("../../files_for_db/coordinates/phl_coordinates.csv", index = False)



