import pandas as pd


bhr_ef = pd.read_csv("../../data/BHR/bahrain_school_locations.csv")

bhr_ef = bhr_ef[bhr_ef["SUBTYPE EN"].isin(["KINDERGARTEN", "PUBLIC SCHOOLS - BOYS", "PUBLIC SCHOOLS - GIRLS"])]

bhr_ef = bhr_ef[["NAME", "#"]]

bhr_ef = bhr_ef.reset_index()

bhr_ef['geo_id'] = bhr_ef['index'].apply(lambda x: 'BHR-{0:0>6}'.format(x))

bhr_ef = bhr_ef.drop(["index"], axis = 1)

bhr_ef = bhr_ef[["geo_id", "#", "NAME"]].rename(columns = {"#": "deped_id", "NAME": "school_name"})

print(bhr_ef.head())

bhr_ef.to_csv("../../files_for_db/ids/bhr_ids.csv", index = False)
