import pandas as pd


per_ef = pd.read_csv("../../data/PER/Relación de instituciones y programas educativos.csv")

per_ef = per_ef.drop_duplicates(subset = ["cod_mod"])

per_ef['cen_edu'] = per_ef['cen_edu'].str.replace('\d+', '')

per_ef = per_ef[["cod_mod", "nlong_ie", "nlat_ie"]].rename(columns = {"cod_mod": "deped_id", "cen_edu": "school_name"})

ids = pd.read_csv("../../files_for_db/ids/per_ids.csv")

per_ef = pd.merge(per_ef, ids, on = "deped_id").rename(columns = {"nlong_ie": "longitude", "nlat_ie": "latitude"})

per_ef = per_ef[["geo_id", "longitude", "latitude"]]

per_ef = per_ef[per_ef["longitude"] != 0]
per_ef = per_ef[per_ef["latitude"] != 0]

print(per_ef.head())

per_ef.to_csv("../../files_for_db/coordinates/per_coordinates.csv", index = False)