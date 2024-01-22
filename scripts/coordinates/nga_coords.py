import pandas as pd


nig_ef = pd.read_csv("../../data/NIG/educational-facilities-in-nigeria.csv")
nig_ef = nig_ef[["facility_id", "longitude", "latitude"]]
nig_ef = nig_ef.reset_index()

ids = pd.read_csv("../../files_for_db/ids/nig_ids.csv")

nig_ef = nig_ef.rename(columns = {"facility_id": "deped_id"})
nig_ef = pd.merge(nig_ef, ids, on = "deped_id")
nig_ef = nig_ef[["geo_id", "longitude", "latitude"]]

nig_ef = nig_ef[nig_ef["longitude"] != 0]
nig_ef = nig_ef[nig_ef["latitude"] != 0]

print(nig_ef.head())

nig_ef.to_csv("../../files_for_db/coordinates/nig_coordinates.csv", index = False)
