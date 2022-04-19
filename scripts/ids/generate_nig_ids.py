import pandas as pd


nig_ef = pd.read_csv("../../data/NIG/educational-facilities-in-nigeria.csv")
nig_ef = nig_ef[["facility_name"]]
nig_ef = nig_ef.reset_index()
nig_ef['geo_id'] = nig_ef['index'].apply(lambda x: 'NIG-{0:0>6}'.format(x))
nig_ef["deped_id"] = None
nig_ef = nig_ef[["geo_id", "deped_id", "facility_name"]]
nig_ef = nig_ef.rename(columns = {"facility_name":"school_name"})

print(nig_ef.head())


nig_ef.to_csv("../../files_for_db/ids/nig_ids.csv", index = False)
