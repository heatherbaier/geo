import pandas as pd
import os


tan_ef_prim = pd.read_csv("../../data/TAN/Consolidated_Primary_EnrolmentbyGrade_PTR_2022_PSLE2021.csv")
tan_ef_prim = tan_ef_prim[tan_ef_prim["SCHOOL OWNERSHIP"] == "Government"]
tan_ef_prim.columns = [_.title() for _ in tan_ef_prim]
tan_ef_prim = tan_ef_prim[['Region', 'Council', 'Ward', 'School Name']]
tan_ef_prim.columns = ['Region', 'Council', 'Ward', 'School_Name']
tan_ef_prim.columns = [_.lower() for _ in tan_ef_prim]


# tan_ef_prim = tan_ef_prim.rename(columns = {"Latitute": "Latitude"})

tan_ef_sec = pd.read_csv("../../data/TAN/Consolidated_Secondary_EnrolmentbyGrade_PTR_CSEE2021, 2022.csv")
tan_ef_sec = tan_ef_sec[['Region', 'Council', 'Ward', 'School']]
tan_ef_sec.columns = ['Region', 'Council', 'Ward', 'School_Name']
tan_ef_sec.columns = [_.lower() for _ in tan_ef_sec]

ids = pd.read_csv("../../files_for_db/ids/tan_ids.csv")

print(ids["school_name"].value_counts())

print(ids.head())