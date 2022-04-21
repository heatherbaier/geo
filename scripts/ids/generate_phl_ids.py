import pandas as pd


phl_ef = pd.read_csv("../../data/PHL/this_one.csv")
phl_ef = phl_ef[["school_id", "school_name"]]
phl_ef = phl_ef.drop_duplicates(subset = ["school_id"])

phl_ef = phl_ef.reset_index()
phl_ef['geo_id'] = phl_ef['index'].apply(lambda x: 'PHL-{0:0>6}'.format(x))
phl_ef = phl_ef[["geo_id", "school_id", "school_name"]].rename(columns = {"school_id": "deped_id"})

print(phl_ef.head())

phl_ef.to_csv("../../files_for_db/ids/phl_ids.csv", index = False)


