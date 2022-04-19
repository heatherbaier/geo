import pandas as pd


tan_ef = pd.read_csv("../../data/TAN/pri-performing-all.csv")
tan_ef = tan_ef[["CODE", "NAME", "LONGITUDE", "LATITUDE"]]
tan_ef = tan_ef.drop_duplicates(subset = ["CODE"])


ids = pd.read_csv("../../files_for_db/ids/tan_ids.csv")

print(ids.head())

tan_ef = tan_ef.rename(columns = {"CODE": "deped_id"})
tan_ef = pd.merge(tan_ef, ids, on = "deped_id")
tan_ef.columns = [_.lower() for _ in tan_ef.columns]

tan_ef = tan_ef[["geo_id", "longitude", "latitude"]]

tan_ef = tan_ef[tan_ef["longitude"] != 0]
tan_ef = tan_ef[tan_ef["latitude"] != 0]

print(tan_ef.head())

tan_ef.to_csv("../../files_for_db/coordinates/tan_coordinates.csv", index = False)
