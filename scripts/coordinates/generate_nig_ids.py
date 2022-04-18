import pandas as pd


nig_ef = pd.read_csv("./data/nigeria/educational-facilities-in-nigeria.csv")
nig_ef = nig_ef[["facility_name", "latitude", "longitude"]]
nig_ef = nig_ef.reset_index()
nig_ef['geo_id'] = nig_ef['index'].apply(lambda x: 'NIG-{0:0>6}'.format(x))
nig_ef = nig_ef.drop(["facility_name"], axis = 1)
nig_ef = nig_ef[["geo_id", "longitude", "latitude"]]

print(nig_ef.head())


nig_ef.to_csv("./files_for_db/coordinates/nig_coordinates.csv", index = False)
