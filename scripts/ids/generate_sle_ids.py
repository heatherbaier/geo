import pandas as pd


sle_ef = pd.read_csv("../../data/SLE/sleeducptstewardschools.csv")
print(sle_ef.columns)
sle_ef = sle_ef[["Educ_Code", "Educ_Name", 'Adm2_Name', 'Adm3_Name', 'Adm4_Name']].rename(columns = {'Adm2_Name':"adm1", 'Adm3_Name': "adm2", 'Adm4_Name':"adm3"})
sle_ef = sle_ef.reset_index()
sle_ef['geo_id'] = sle_ef['index'].apply(lambda x: 'SLE-{0:0>6}'.format(x))
sle_ef["address"] = "None"
sle_ef["adm0"] = "SLE"
sle_ef = sle_ef[["geo_id", "Educ_Code", "Educ_Name", "address","adm0","adm1","adm2","adm3"]].rename(columns = {"Educ_Code": "deped_id", "Educ_Name": "school_name"})

print(sle_ef.head())

sle_ef.to_csv("../../files_for_db/ids/sle_ids.csv", index = False)


