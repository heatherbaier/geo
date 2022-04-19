import pandas as pd


tan_ef = pd.read_csv("../../data/TAN/pri-performing-all.csv")

tan_ef = tan_ef[["CODE", "NAME"]]

tan_ef = tan_ef.drop_duplicates(subset = ["CODE"])

tan_ef = tan_ef.reset_index()

tan_ef['geo_id'] = tan_ef['index'].apply(lambda x: 'TAN-{0:0>6}'.format(x))

tan_ef = tan_ef.drop(["index"], axis = 1)

tan_ef = tan_ef[["geo_id", "CODE", "NAME"]].rename(columns = {"CODE": "deped_id", "NAME": "school_name"})

print(tan_ef.head())

tan_ef.to_csv("../../files_for_db/ids/tan_ids.csv", index = False)
