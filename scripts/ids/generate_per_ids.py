import pandas as pd


per_ef = pd.read_csv("../../data/PER/Relación de instituciones y programas educativos.csv")

per_ef = per_ef.drop_duplicates(subset = ["cod_mod"])

per_ef['cen_edu'] = per_ef['cen_edu'].str.replace('\d+', '')

per_ef = per_ef[["cod_mod", "cen_edu", "nlong_ie", "nlat_ie"]]

per_ef = per_ef.reset_index()

per_ef['geo_id'] = per_ef['index'].apply(lambda x: 'PER-{0:0>6}'.format(x))

per_ef = per_ef.drop(["index"], axis = 1)

per_ef = per_ef[["geo_id", "cod_mod", "cen_edu"]].rename(columns = {"cod_mod": "deped_id", "cen_edu": "school_name"})

print(per_ef.head())

per_ef.to_csv("../../files_for_db/ids/per_ids.csv", index = False)
