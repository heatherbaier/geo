import pandas as pd
import os


tan_ef_prim = pd.read_csv("../../data/TAN/Consolidated_Primary_EnrolmentbyGrade_PTR_2022_PSLE2021.csv")
tan_ef_prim = tan_ef_prim[tan_ef_prim["SCHOOL OWNERSHIP"] == "Government"]
tan_ef_prim.columns = [_.title() for _ in tan_ef_prim]
tan_ef_prim = tan_ef_prim[['Region', 'Council', 'Ward', 'School Name', 'Total Boys', 'Total Girls', 'All Teachers Male', 'All Teachers Female']]
tan_ef_prim.columns = ['Region', 'Council', 'Ward', 'School_Name', 'Total_male_students_2122', 'Total_female_students_2122', 'total_male_teachers_2122', 'total_female_teachers_2122']
tan_ef_prim.columns = [_.lower() for _ in tan_ef_prim]
tan_ef_prim["total_students_2122"] = tan_ef_prim['total_male_students_2122'] + tan_ef_prim['total_female_students_2122']

# tan_ef_prim = tan_ef_prim.rename(columns = {"Latitute": "Latitude"})

tan_ef_sec = pd.read_csv("../../data/TAN/Consolidated_Secondary_EnrolmentbyGrade_PTR_CSEE2021, 2022.csv")
tan_ef_sec = tan_ef_sec[['Region', 'Council', 'Ward', 'School', 'M-Total', 'F-Total', 'Total Teachers-Male', 'Total Teachers-Female']]
tan_ef_sec.columns = ['Region', 'Council', 'Ward', 'School_Name', 'Total_male_students_2122', 'Total_female_students_2122', 'total_male_teachers_2122', 'total_female_teachers_2122']
tan_ef_sec.columns = [_.lower() for _ in tan_ef_sec]
tan_ef_sec["total_students_2122"] = tan_ef_sec['total_male_students_2122'] + tan_ef_sec['total_female_students_2122']

tan_ef = tan_ef_prim.append(tan_ef_sec)

ids = pd.read_csv("../../files_for_db/ids/tan_ids.csv")

# tan_ef = tan_ef.reset_index()
# tan_ef['geo_id'] = tan_ef['index'].apply(lambda x: 'TAN-{0:0>6}'.format(x))
# tan_ef["deped_id"] = None

# tan_ef = tan_ef[["geo_id", "Longitude", "Latitude"]]#.rename(columns = {"School Name": "school_name"})
# tan_ef.columns = [_.lower() for _ in tan_ef.columns]

print(ids.head())
