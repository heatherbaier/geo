import pandas as pd


# tan_ef = pd.read_csv("../../data/TAN/pri-performing-all.csv")
# tan_ef = tan_ef[["CODE", "NAME", "LONGITUDE", "LATITUDE"]]
# tan_ef = tan_ef.drop_duplicates(subset = ["CODE"])


# ids = pd.read_csv("../../files_for_db/ids/tan_ids.csv")

# print(ids.head())

# tan_ef = tan_ef.rename(columns = {"CODE": "deped_id"})
# tan_ef = pd.merge(tan_ef, ids, on = "deped_id")
# tan_ef.columns = [_.lower() for _ in tan_ef.columns]

# tan_ef = tan_ef[["geo_id", "longitude", "latitude"]]

# tan_ef = tan_ef[tan_ef["longitude"] != 0]
# tan_ef = tan_ef[tan_ef["latitude"] != 0]

# print(tan_ef.head())

# tan_ef.to_csv("../../files_for_db/coordinates/tan_coordinates.csv", index = False)


tan_ef_prim = pd.read_csv("../../data/TAN/Consolidated_Primary_EnrolmentbyGrade_PTR_2022_PSLE2021.csv")
tan_ef_prim = tan_ef_prim[tan_ef_prim["SCHOOL OWNERSHIP"] == "Government"]
tan_ef_prim = tan_ef_prim[['REGION', 'COUNCIL', 'WARD', 'SCHOOL NAME', 'LATITUTE', 'LONGITUDE']]
tan_ef_prim.columns = [_.title() for _ in tan_ef_prim]
tan_ef_prim = tan_ef_prim.rename(columns = {"Latitute": "Latitude"})

tan_ef_sec = pd.read_csv("../../data/TAN/Consolidated_Secondary_EnrolmentbyGrade_PTR_CSEE2021, 2022.csv")
tan_ef_sec = tan_ef_sec[['Region', 'Council', 'Ward', 'School', 'Latitude', 'Longitude']]
tan_ef_sec = tan_ef_sec.rename(columns = {"School": "School Name"})

tan_ef = tan_ef_prim.append(tan_ef_sec)

tan_ef = tan_ef.reset_index()
tan_ef['geo_id'] = tan_ef['index'].apply(lambda x: 'TAN-{0:0>6}'.format(x))
tan_ef["deped_id"] = None

tan_ef = tan_ef[["geo_id", "Longitude", "Latitude"]]#.rename(columns = {"School Name": "school_name"})
tan_ef.columns = [_.lower() for _ in tan_ef.columns]

print(tan_ef.head())
