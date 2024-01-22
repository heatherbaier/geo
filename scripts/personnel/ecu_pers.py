import pandas as pd
import numpy as np
from utils import *

#import necessary data from github
ecu_table = pd.read_csv("../../data/ECU/MINEDUC_RegistrosAdministrativos_2021-2022-Fin.csv")
ecu_id_table = pd.read_csv("../../files_for_db/ids/ecu_ids.csv")

#data cleaning for original data source
ecu_table.columns = ecu_table.iloc[11]
ecu_table.drop(ecu_table.index[:12], inplace=True)
ecu_table.reset_index(inplace=True)
ecu_table

#extracting data for preliminary personnel table
ecu_table_personnel = ecu_table[["AMIE", "Total_Estudiantes", "Estudiantes_Femenino", "Estudiantes_Masculino", "Total_Docentes"]]

#calculate student-teacher ratio
ecu_table_personnel["st_ratio"] = ecu_table_personnel["Total_Estudiantes"].astype(int) / ecu_table_personnel["Total_Docentes"].astype(int)
ecu_table_personnel["st_ratio"] = ecu_table_personnel["st_ratio"].replace([np.inf, 0], np.nan)

#rename columns
ecu_table_personnel.columns = ["deped_id", "student_enrollment", "female_student_enrollment", "male_student_enrollment", "num_teachers", "st_ratio"]

#merge tables and final cleanup
ecu_table_personnel_final = pd.merge(ecu_table_personnel, ecu_id_table, how="inner")
ecu_table_personnel_final["year"] = "2122"
ecu_table_personnel_final = ecu_table_personnel_final[["geo_id", "year", "student_enrollment","female_student_enrollment", "male_student_enrollment", "num_teachers", "st_ratio"]]

#export final table as csv
ecu_table_personnel_final.to_csv("../../files_for_db/personnel/ecu_pers.csv", index = False)
