import pandas as pd
import numpy as np

#import necessary data from github
zaf_table = pd.read_excel("../../data/ZAF/National.xlsx")
zaf_ids = pd.read_csv("../../files_for_db/ids/zaf_ids.csv")

#select necessary columns
zaf_table = zaf_table[["NatEmis", "DataYear", "Learners2022", "Educators2022"]]
zaf_table.columns = ["country_id", "year", "student_enrollment", "num_teachers"]

#add student:teacher ratio
zaf_table["st_ratio"] = np.nan
for i in range(len(zaf_table)):
    if zaf_table["num_teachers"].iloc[i] == 0 or zaf_table["num_teachers"].iloc[i] == "Educators2022":
        zaf_table["st_ratio"].iloc[i] = np.nan
    else:
        zaf_table["st_ratio"].iloc[i] = zaf_table["student_enrollment"].iloc[i] / zaf_table["num_teachers"].iloc[i]
        
#specify column types for merge
zaf_table["country_id"] = zaf_table["country_id"].astype("str")
zaf_ids["country_id"] = zaf_ids["country_id"].astype("str")
zaf_table = pd.merge(zaf_table, zaf_ids)

#final additions and formatting
zaf_table["female_student_enrollment"] = np.nan
zaf_table["male_student_enrollment"] = np.nan
zaf_table = zaf_table[["geo_id", "year", "student_enrollment", "female_student_enrollment", "male_student_enrollment", "num_teachers", "st_ratio"]]

#export csv
zaf_table.to_csv("../../files_for_db/personnel/zaf_personnel.csv", index=False)