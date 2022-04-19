import pandas as pd


bhr_ef = pd.read_csv("../../data/BHR/bahrain_school_locations.csv")
bhr_ef = bhr_ef[bhr_ef["SUBTYPE EN"].isin(["KINDERGARTEN", "PUBLIC SCHOOLS - BOYS", "PUBLIC SCHOOLS - GIRLS"])]
bhr_ef = bhr_ef[["#", "POINT_X_Longitude", "POINT_Y_Latitude"]]
# bhr_ef = bhr_ef.reset_index()

ids = pd.read_csv("../../files_for_db/ids/bhr_ids.csv")

print(ids.head())

bhr_ef = bhr_ef.rename(columns = {"#": "deped_id"})
bhr_ef = pd.merge(bhr_ef, ids, on = "deped_id").rename(columns = {"POINT_X_Longitude": "longitude", "POINT_Y_Latitude": "latitude"})

bhr_ef = bhr_ef[["geo_id", "longitude", "latitude"]]

bhr_ef = bhr_ef[bhr_ef["longitude"] != 0]
bhr_ef = bhr_ef[bhr_ef["latitude"] != 0]

print(bhr_ef.head())

bhr_ef.to_csv("../../files_for_db/coordinates/bhr_coordinates.csv", index = False)
