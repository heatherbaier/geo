import pandas as pd

#import necessary data from github
cri_table1 = pd.read_excel("../../data/CRI/MATRICULA_INICIAL_COLEGIOS_2014-2021_POR_AÑO_CURSADO_Y_SEXO.xlsx", header=2)
cri_table2 = pd.read_excel("../../data/CRI/MATRICULA_INICIAL_ESCUELAS_DIURNAS_2014-2021_POR_AÑO_CURSADO_Y_SEXO.xlsx", header=2)
cri_ids = pd.read_csv("../../files_for_db/ids/cri_ids.csv")

#prep data for merging with ids
cri_table1 = cri_table1 = cri_table1[["CURSO LECTIVO", "NOMBRE", "DISTRITO", "TOTAL", "HOMBRES", "MUJERES"]]
cri_table2 = cri_table2 = cri_table1[["CURSO LECTIVO", "NOMBRE", "DISTRITO", "TOTAL", "HOMBRES", "MUJERES"]]

cri_table = cri_table1.append(cri_table2)

cri_table.columns = ["year", "school_name", "adm3", "student_enrollment", "male_student_enrollment", "female_student_enrollment"]

#merge data with id table based on school name and adm3

cri_table = pd.merge(cri_table, cri_ids, how="inner")

#final formatting
cri_table["num_teachers"] = None
cri_table["st_ratio"] = None

cri_table = cri_table[["geo_id", "year", "student_enrollment", "female_student_enrollment", "male_student_enrollment", "num_teachers", "st_ratio"]]

#export final table as csv
cri_table.to_csv("../../files_for_db/personnel/cri_pers.csv", index=False)