import geopandas as gpd
import pandas as pd
import os
import numpy as np

 # Get geo ID data for KHM secondary schools
DATA_PATH = os.path.join(os.getcwd(),"../../files_for_db/geo/khm_geo.csv")
khm_csv_data = pd.read_csv(DATA_PATH)
sec_schools = khm_csv_data[khm_csv_data['deped_id'].str.contains("Lycee G7-12|Lycee G10-12", na=False)]

# Get raw secondary school data
DATA_PATH1 = os.path.join(os.getcwd(),"../../data/KHM/lycee-g7-12/Lycee G7-12.shp")
DATA_PATH2 = os.path.join(os.getcwd(),"../../data/KHM/lycee-g10-12/Lycee G10-12.shp")
g7_12 = gpd.read_file(DATA_PATH1)
g10_12 = gpd.read_file(DATA_PATH2)

# Add dependency IDs to map to geo IDs
# Secondary schools 7-12
deped_id_ls = ["Lycee G7-12" + f".{idx}" for idx in range(1,g7_12.shape[0]+1)]
g7_12["deped_id"] = deped_id_ls
# Secondary schools 10-12
deped_id_ls = ["Lycee G10-12" + f".{idx}" for idx in range(1,g10_12.shape[0]+1)]
g10_12["deped_id"] = deped_id_ls

# Combine secondary school data
g7_10_12 = pd.concat([g7_12, g10_12], ignore_index=True)
# Join geo IDs to personnel data
per_schools = pd.merge(sec_schools, g7_10_12, on='deped_id')

# Filter, add, and restructure features
per_schools['year'] = np.nan
per_schools['total_teacher_male'] = np.nan
per_schools['total_teacher_female'] = np.nan
per_schools['total_student_male'] = np.nan
per_schools['total_student_female'] = np.nan
per_schools.rename(columns={'Teach_staf': 'total_teachers','Enrol':'total_student_enrollment'},inplace=True)
per_schools = per_schools[['geo_id','deped_id','total_teacher_male','total_teacher_female','total_teachers','total_student_male','total_student_female','total_student_enrollment']]

per_schools.to_csv('../../files_for_db/personnel/khm_personnel.csv',index=False)