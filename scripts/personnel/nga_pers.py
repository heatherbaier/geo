import pandas as pd
import numpy as np
from utils import *

#import necessary data from github
nga_table = pd.read_csv("../../data/NGA/educational-facilities-in-nigeria.csv")
nga_id_table = pd.read_csv("../../files_for_db/ids/nga_ids.csv")

#create new columns with data from original source
nga_table["year"] = nga_table["date_of_survey"].str[:4]

nga_table["st_ratio"] = nga_table["num_students_total"] / nga_table["num_tchr_full_time"]
nga_table["st_ratio"] = nga_table["st_ratio"].replace([np.inf, 0], np.nan)

#keep only necessary columns
nga_table_personnel = nga_table[["facility_id", "year", "num_students_total", "num_students_female", "num_students_male", "num_tchr_full_time", "st_ratio"]]

#merge with ID table to get geoIDs
nga_table_personnel["deped_id"] = nga_table_personnel["facility_id"]
nga_table_personnel = pd.merge(nga_table_personnel, nga_id_table, how="inner")

#final formatting
nga_table_personnel = nga_table_personnel[["geo_id", "year", "num_students_total", "num_students_female", "num_students_male", "num_tchr_full_time", "st_ratio"]]
nga_table_personnel.columns = ["geo_id", "year", "student_enrollment", "female_student_enrollment", "male_student_enrollment", "num_teachers", "st_ratio"]

#export final table as csv
nga_table_personnel.to_csv("../../files_for_db/personnel/nga_pers.csv", index = False)
