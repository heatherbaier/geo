#please note that for the number of teachers and student:teacher ratios, those values may be reversed. the data is not clear, but the values in the file have decimals, so it assumed that it is the ratio

import pandas as pd
import numpy as np

#import necessary data from github

usa_table = pd.read_csv("../../data/USA/ccd_sch_059_2122_l_1a_071722.csv")
usa_stu_table = pd.read_csv("ccd_SCH_052_2122_l_1a_071722.csv") #this data is not in github and must be downloaded - see metadata about usa data
usa_id_table = pd.read_csv("../../files_for_db/ids/usa_ids.csv")

#prepping table with student:teacher ratios
usa_table = usa_table[["SCHOOL_YEAR", "SCHID", "TEACHERS"]]
usa_table.columns = ["year", "country_id", "st_ratio"]

#merge with id table
usa_table = pd.merge(usa_table, usa_id_table, how="inner")

#prepping table with student enrollment
usa_stu_table = usa_stu_table.pivot_table(index=["SCHID", "SCHOOL_YEAR"], columns="SEX", values="STUDENT_COUNT", aggfunc=np.sum).reset_index()
usa_stu_table["student_enrollment"] = usa_stu_table["Female"] + usa_stu_table["Male"] + usa_stu_table["Not Specified"]
usa_stu_table.columns = ["country_id", "year", "female_student_enrollment", "male_student_enrollment", "temp1", "temp2", "student_enrollment"]

#merge with other tables
usa_table = pd.merge(usa_table, usa_stu_table, how="inner")

#calculate number of teachers (see note at top of this script)
usa_table["num_teachers"] = round(usa_table["student_enrollment"] / usa_table["st_ratio"])

#final formatting
usa_table = usa_table[["geo_id", "year", "student_enrollment", "female_student_enrollment", "male_student_enrollment", "num_teachers", "st_ratio"]]

#export final table as csv
usa_table.to_csv("../../files_for_db/personnel/usa_pers.csv", index = False)