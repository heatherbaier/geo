import pandas as pd

tan_ef = pd.read_csv("../../data/TAN/pri-performing-all.csv")
tan_ef = tan_ef[["CODE", "NAME", "REGION", "DISTRICT", "WARD", "OWNERSHIP", "LONGITUDE", "LATITUDE"]]
tan_ef = tan_ef.drop_duplicates(subset = ["CODE"])
tan_ef = tan_ef.reset_index()
tan_ef['geo_id'] = tan_ef['index'].apply(lambda x: 'TAN-{0:0>6}'.format(x))
tan_ef = tan_ef.drop(["index"], axis = 1)
tan_ef = tan_ef[["geo_id", "CODE", "NAME"]].rename(columns = {"CODE": "deped_id", "NAME": "school_name"})
print(tan_ef.head())
tan_ef.to_csv("../../files_for_db/ids/tan_ids.csv", index = False)



# tan_ef_prim = pd.read_csv("../../data/TAN/Consolidated_Primary_EnrolmentbyGrade_PTR_2022_PSLE2021.csv")
# tan_ef_prim = tan_ef_prim[tan_ef_prim["SCHOOL OWNERSHIP"] == "Government"]
# tan_ef_prim = tan_ef_prim[['REGION', 'COUNCIL', 'WARD', 'SCHOOL NAME', 'SCHOOL REG. NUMBER', 'LATITUTE', 'LONGITUDE']]
# tan_ef_prim.columns = [_.title() for _ in tan_ef_prim.columns]
# tan_ef_prim = tan_ef_prim.rename(columns = {"Latitute": "Latitude", "School Reg. Number": "deped_id"})

# tan_ef_sec = pd.read_csv("../../data/TAN/Consolidated_Secondary_EnrolmentbyGrade_PTR_CSEE2021, 2022.csv")
# tan_ef_sec = tan_ef_sec[['Region', 'Council', 'Ward', 'School', 'Reg.No.', 'Latitude', 'Longitude']]
# tan_ef_sec = tan_ef_sec.rename(columns = {"School": "School Name", "Reg.No.":"deped_id"})

# tan_ef = tan_ef_prim.append(tan_ef_sec)

# tan_ef = tan_ef.reset_index()
# tan_ef['geo_id'] = tan_ef['index'].apply(lambda x: 'TAN-{0:0>6}'.format(x))

# tan_ef["address"] = None
# tan_ef["adm0"] = "TAN"
# tan_ef = tan_ef[["geo_id", "deped_id", "School Name", "address", "adm0",  "Region", "Council", "Ward"]].rename(columns = {"School Name": "school_name"})
# tan_ef.columns = ["geo_id", "deped_id", "School_Name", "address", "adm0", "adm1", "adm2", "adm3"]
# tan_ef.columns = [_.lower() for _ in tan_ef.columns]

# print(tan_ef.head())

# tan_ef.to_csv("../../files_for_db/ids/tan_ids.csv", index = False)
