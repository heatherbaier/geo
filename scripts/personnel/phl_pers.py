import pandas as pd
import numpy as np
from utils import *

#import necessary data from github
phl_raw = pd.read_csv("../../data/PHL/this_one.csv")
phl_ids = pd.read_csv("../../files_for_db/ids/phl_ids.csv")

#select and rename necessary columns
phl_personnel = phl_raw[["school_year", "school_id", "total_enrollment", "total_female", "total_male", "total_teachers", "student_teacher_ratio"]]
phl_personnel.rename(columns = {"school_year":"year", "school_id":"deped_id", "total_enrollment":"student_enrollment", "total_female":"female_student_enrollment", "total_male":"male_student_enrollment", "total_teachers":"num_teachers", "student_teacher_ratio":"st_ratio"}, inplace=True)

#merge to get geo_ids
phl_personnel = pd.merge(phl_personnel, phl_ids, how="inner")
phl_personnel = phl_personnel[["geo_id", "year", "student_enrollment", "female_student_enrollment", "male_student_enrollment", "num_teachers", "st_ratio"]]

#export as csv
phl_personnel.to_csv("../../files_for_db/personnel/phl_pers.csv", index = False)