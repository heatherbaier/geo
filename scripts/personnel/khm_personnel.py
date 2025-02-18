import geopandas as gpd
import pandas as pd
import shutil
import os


# geo_id VARCHAR NOT NULL, 
# year VARCHAR NOT NULL, 
# deped_id VARCHAR,
# total_teacher_male VARCHAR, 
# total_teacher_female VARCHAR, 
# total_teachers VARCHAR,
# total_student_male VARCHAR,
# total_student_female VARCHAR,
# total_student_enrollment VARCHAR


ids = pd.read_csv("../../files_for_db/geo/khm_geo.csv")
id_dict = dict(zip(ids["deped_id"], ids["geo_id"]))
print(ids.head())


# Fetch and read the datasets
DATA_PATH = str(os.path.abspath(os.path.join(__file__ ,"../../.."))) + "/data/KHM/"
khm_schools = gpd.read_file(DATA_PATH + "Basic information of school (2014)/basic_information_of_school_2014.shp").rename(columns = {"SCHOOL_COD": "deped_id"})
khm_schools = khm_schools.to_crs("epsg:4326")

khm_schools['total_student_enrollment'] = khm_schools['Total_enro'].str.replace(",", "").fillna(0).astype(int)
khm_schools['total_student_female'] = khm_schools['Female_Enr'].str.replace(",", "").fillna(0).astype(int)

# Create new columns for male students and male teachers:
khm_schools['total_student_male'] = khm_schools['total_student_enrollment'] - khm_schools['total_student_female']
khm_schools['total_teacher_male'] = khm_schools['Total_Teac'] - khm_schools['Female_Tec']

# Optionally, rename the existing columns for clarity:
khm_schools = khm_schools.rename(columns={
    # 'Total_enro': 'Total_Students',
    # 'Female_Enr': 'Female_Students',
    'Total_Teac': 'total_teachers',
    'Female_Tec': 'total_teacher_female'
})

khm_schools["year"] = 2014
khm_schools["geo_id"] = khm_schools["deped_id"].map(id_dict)

# geo_id VARCHAR NOT NULL, 
# year VARCHAR NOT NULL, 
# deped_id VARCHAR,
# total_teacher_male VARCHAR, 
# total_teacher_female VARCHAR, 
# total_teachers VARCHAR,
# total_student_male VARCHAR,
# total_student_female VARCHAR,
# total_student_enrollment VARCHAR

khm_schools = khm_schools[["geo_id", "year", "deped_id", "total_teacher_male", "total_teacher_female", "total_teachers", "total_student_male", "total_student_female", "total_student_enrollment"]]

print(khm_schools.head())

khm_schools.to_csv("../../files_for_db/personnel/khm_personnel.csv", index = False)