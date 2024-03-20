import pandas as pd

ids = pd.read_csv("../../archive/phl_geo.csv")

data = pd.read_csv("../../data/PHL/this_one.csv")
data = data[['school_year', 'school_id', 'total_teachers',
       'total_female', 'total_male',
       'total_enrollment']]
data.columns = ['year', 'deped_id', 'total_teachers',
       'total_student_female', 'total_student_male',
       'total_student_enrollment']
data['total_teacher_male'] = None
data['total_teacher_female'] = None


data = pd.merge(data, ids, on = "deped_id")
data = data[["geo_id", "year", "deped_id", "total_teacher_male", "total_teacher_female", "total_teachers",
             "total_student_male", "total_student_female", "total_student_enrollment"]]

data.to_csv("../../files_for_db/personnel/phl_personnel.csv", index = False)