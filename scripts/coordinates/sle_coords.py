import pandas as pd


sle_ef = pd.read_csv("../../data/SLE/sleeducptstewardschools.csv")
sle_ef = sle_ef[["Educ_Code", "Longitude", "Latitude"]]

ids = pd.read_csv("../../files_for_db/ids/sle_ids.csv")

print(ids.head())

sle_ef = sle_ef.rename(columns = {"Educ_Code": "deped_id"})
sle_ef = pd.merge(sle_ef, ids, on = "deped_id").rename(columns = {"Longitude": "longitude", "Latitude": "latitude"})

sle_ef = sle_ef[["geo_id", "longitude", "latitude"]]

sle_ef = sle_ef[sle_ef["longitude"] != 0]
sle_ef = sle_ef[sle_ef["latitude"] != 0]

print(sle_ef.head())

sle_ef.to_csv("../../files_for_db/coordinates/sle_coordinates.csv", index = False)



