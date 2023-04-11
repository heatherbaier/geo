import pandas as pd

#import and clean primary school data 
tan_ef_prim = pd.read_csv("../../data/TAN/Consolidated_Primary_EnrolmentbyGrade_PTR_2022_PSLE2021.csv")

tan_ef_prim = tan_ef_prim[tan_ef_prim["SCHOOL OWNERSHIP"] == "Government"]

tan_ef_prim = tan_ef_prim[['SCHOOL REG. NUMBER', 'LATITUTE', 'LONGITUDE']]
tan_ef_prim.columns = [_.title() for _ in tan_ef_prim]
tan_ef_prim = tan_ef_prim.rename(columns = {"Latitute": "Latitude", "School Reg. Number": "deped_id"})

#import and clean secondary school data
tan_ef_sec = pd.read_csv("../../data/TAN/Consolidated_Secondary_EnrolmentbyGrade_PTR_CSEE2021, 2022.csv")
tan_ef_sec = tan_ef_sec[['Reg.No.', 'Latitude', 'Longitude']]
tan_ef_sec = tan_ef_sec.rename(columns = {"Reg.No.":"deped_id"})

#put data together
tan_ef = tan_ef_prim.append(tan_ef_sec)
tan_ef = tan_ef.reset_index()

#match with geo_ids
tan_ids = pd.read_csv("tan_ids.csv")

tan_ef = pd.merge(tan_ef, tan_ids, on="deped_id")

tan_ef = tan_ef[["geo_id", "Longitude", "Latitude"]]
tan_ef.columns = [_.lower() for _ in tan_ef.columns]

#validate and export table
print(tan_ef.head())

tan_ef.to_csv("tan_coordinates.csv", index=False)
