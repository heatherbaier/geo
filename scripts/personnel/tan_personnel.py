import pandas as pd

ids = pd.read_csv("../../archive/tan_geo.csv")

prim = pd.read_csv("/Users/heatherbaier/Documents/geo_git/data/TAN/Consolidated_Primary_EnrolmentbyGrade_PTR_2022_PSLE2021.csv")
prim = prim.rename(columns = {"SCHOOL REG. NUMBER": "deped_id"})

seco = pd.read_csv("/Users/heatherbaier/Documents/geo_git/data/TAN/Consolidated_Secondary_EnrolmentbyGrade_PTR_CSEE2021, 2022.csv")
seco = seco.rename(columns = {"School": "School Name", "Reg.No.": "deped_id"})

tan = pd.merge(ids, prim, on = "deped_id")
tan = tan[['geo_id', 'deped_id', 'TOTAL BOYS', 'TOTAL GIRLS', 'ALL TEACHERS MALE',
       'ALL TEACHERS FEMALE']]

tan = pd.merge(tan, seco, on = "deped_id", how = "left")

tan = tan[['geo_id', 'deped_id', 'TOTAL BOYS', 'TOTAL GIRLS', 'ALL TEACHERS MALE',
       'ALL TEACHERS FEMALE', 'M-Total', 'F-Total', 'Total Teachers-Male',
       'Total Teachers-Female']]

tan = tan.rename(columns = {'TOTAL BOYS': "total_student_male", 
                           'TOTAL GIRLS': "total_student_female", 
                           'ALL TEACHERS MALE': "total_teacher_male", 
                           'ALL TEACHERS FEMALE': "total_teacher_female", 
                           'M-Total': "total_student_male", 
                           'F-Total': "total_student_female", 
                           'Total Teachers-Male': "total_teacher_male", 
                           'Total Teachers-Female': "total_teacher_female"})

tan["year"] = 2021

tan = tan.groupby(lambda x:x, axis=1).sum()

tan["total_teachers"] = tan["total_teacher_male"] + tan["total_teacher_female"]
tan["total_student_enrollment"] = tan["total_student_male"] + tan["total_student_female"]


print(tan.head())

tan = tan[["geo_id", "year", "deped_id", "total_teacher_male", "total_teacher_female", "total_teachers",
             "total_student_male", "total_student_female", "total_student_enrollment"]]

tan.to_csv("../../files_for_db/personnel/tan_personnel.csv", index = False)