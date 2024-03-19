import pandas as pd


ids = pd.read_csv("../../archive/nig_geo.csv")

data = pd.read_csv("../../data/NGA/educational-facilities-in-nigeria.csv")

data = data[['facility_name', 'num_tchr_full_time', 'num_students_total',
       'num_students_male', 'num_students_female', 'num_tchrs_male',
       'num_tchrs_female', 'date_of_survey', 'facility_id']]
data.columns = ["school_name", "total_teachers", "total_student_enrollment", 
                "total_student_male", "total_student_female", "total_teacher_male", 
                "total_teacher_female", "year", "deped_id"]

data["year"] = data["year"].astype(str).str[0:4]

data = pd.merge(data, ids, on = "deped_id")

data = data[["geo_id", "year", "deped_id", "total_teacher_male", "total_teacher_female", "total_teachers",
             "total_student_male", "total_student_female", "total_student_enrollment"]]

data.to_csv("../../files_for_db/personnel/nig_personnel.csv", index = False)