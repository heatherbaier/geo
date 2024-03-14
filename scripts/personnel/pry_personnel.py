import pandas as pd

# import ids
ids_pry = pd.read_csv("../../files_for_db/geo/pry_geo.csv")

# import all raw personnel data
pers_2012 = pd.read_csv("../../data/PRY/matriculaciones_educacion_escolar_basica_2012.csv")
pers_2013 = pd.read_csv("../../data/PRY/matriculaciones_educacion_escolar_basica_2013.csv")
pers_2018 = pd.read_csv("../../data/PRY/matriculaciones_educacion_escolar_basica_2018.csv")
pers_2019 = pd.read_csv("../../data/PRY/matriculaciones_educacion_escolar_basica_2019.csv")
pers_2020 = pd.read_csv("../../data/PRY/matriculaciones_educacion_escolar_basica_2020.csv")
pers_2021 = pd.read_csv("../../data/PRY/matriculaciones_educacion_escolar_basica_2021.csv")
pers_2022 = pd.read_csv("../../data/PRY/matriculaciones_educacion_escolar_basica_2022.csv")
pers_2023 = pd.read_csv("../../data/PRY/matriculaciones_educacion_escolar_basica_2023.csv")

# prep ids for merge
ids_pry = ids_pry[["geo_id", "deped_id"]]

# concatenate personnel files
pers_pry = pd.concat([pers_2012, pers_2013, pers_2018, pers_2019, pers_2020, pers_2021, pers_2022, pers_2023]).reset_index(drop=True)

# choose and rename columns
pers_pry = pers_pry[["anio", "codigo_establecimiento", "total_matriculados_hombre", "total_matriculados_mujer"]]
pers_pry.columns = ["year", "deped_id", "total_student_male", "total_student_female"]

# merge ids and personnel data
# might need to be changed
pers_pry = pd.merge(ids_pry, pers_pry, on = "deped_id", how="left")

# create total students column
pers_pry["total_student_enrollment"] = pers_pry["total_student_male"] + pers_pry["total_student_female"]

# add columns for teacher info with None
pers_pry["total_teacher_male"] = None
pers_pry["total_teacher_female"] = None
pers_pry["total_teachers"] = None

# reorder columns
pers_pry = pers_pry[["geo_id", "year", "deped_id", "total_teacher_male", "total_teacher_female", "total_teachers", "total_student_male", "total_student_female", "total_student_enrollment"]]

pers_pry = pers_pry[~pers_pry["year"].isna()]

pers_pry["year"] = pers_pry["year"].astype(int)

# export final personnel file
pers_pry.to_csv("../../files_for_db/personnel/pry_personnel.csv", index = False)