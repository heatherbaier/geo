import pandas as pd

# import ids and select columns for merging
ids = pd.read_csv("../../files_for_db/geo/lby_geo.csv")
ids = ids[["geo_id", "deped_id"]]

# import raw personnel data
data = pd.read_csv("../../data/LBY/reach_lby_nationalschoolsassessment_complete_db_reliable__not_reliable_18oct2012.csv", low_memory=False)

# set year column
data["year"] = 2012

# merge in geo_ids
data.rename(columns={'QI_eSchoolID': 'deped_id'}, inplace=True)
data = pd.merge(data, ids, on = "deped_id")

# rename relevant columns
data.rename(columns={'Q2_1NumberofStudentsTotalNow': 'total_student_enrollment',
                     'Q2_1NumberofStudentsBoysNow' : 'total_student_male',
                     'Q2_1NumberofStudentsGirlsNow': 'total_student_female',
                     'Q2_4NumberOfStaff2Now': 'total_teachers'}, inplace=True)

# gender of teachers isn't specified, so set those columns as None
data["deped_id"] = None
data["total_teacher_male"] = None
data["total_teacher_female"] = None

# select relevant columns
data = data[["geo_id",
             "year",
             "deped_id",
             "total_teacher_male",
             "total_teacher_female",
             "total_teachers",
             "total_student_male",
             "total_student_female",
             "total_student_enrollment"]]

print(data.shape)

data = data.dropna(subset = "geo_id")

print(data.head())

print(data.shape)

# save to csv
data.to_csv("../../files_for_db/personnel/lby_personnel.csv", index = False)