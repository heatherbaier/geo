import pandas as pd
import numpy as np
import os



column_map = {"docente_h": "total_teacher_male",
                "docente_m": "total_teacher_female",
                "tot_doc": "total_teachers",
                "hom_t": "total_student_male",
                "muj_t": "total_student_female",
                "insc_t": "total_student_enrollment"}


basica1920 = pd.read_csv("/Users/heatherbaier/Documents/geo_git/data/MEX/BASICA_2019-2020.csv")
basica1920 = basica1920.rename(columns = column_map)
basica1920 = basica1920[["clavecct"] + list(column_map.values())]
basica1920 = pd.DataFrame(basica1920.groupby(["clavecct"]).aggregate("sum")).reset_index()
basica1920["year"] = 2019

basica2021 = pd.read_csv("/Users/heatherbaier/Documents/geo_git/data/MEX/BASICA_2020-2021.csv")
basica2021 = basica2021.rename(columns = column_map)
basica2021 = basica2021[list(column_map.values()) + ["clavecct"]]
basica2021 = pd.DataFrame(basica2021.groupby(["clavecct"]).aggregate("sum")).reset_index()
basica2021["year"] = 2020

basica2122 = pd.read_csv("/Users/heatherbaier/Documents/geo_git/data/MEX/BASICA_2021-2022.csv")
basica2122 = basica2122.rename(columns = column_map)
basica2122 = basica2122[list(column_map.values()) + ["clavecct"]]
basica2122 = pd.DataFrame(basica2122.groupby(["clavecct"]).aggregate("sum")).reset_index()
basica2122["year"] = 2021

basica2223 = pd.read_csv("/Users/heatherbaier/Documents/geo_git/data/MEX/BASICA_2022-2023.csv")
basica2223 = basica2223.rename(columns = column_map)
basica2223 = basica2223[list(column_map.values()) + ["clavecct"]]
basica2223 = pd.DataFrame(basica2223.groupby(["clavecct"]).aggregate("sum")).reset_index()
basica2223["year"] = 2022

basica2324 = pd.read_csv("/Users/heatherbaier/Documents/geo_git/data/MEX/ESTANDAR_BASICA_I2324.csv")
basica2324 = basica2324.rename(columns = column_map)
basica2324 = basica2324[list(column_map.values()) + ["clavecct"]]
basica2324 = pd.DataFrame(basica2324.groupby(["clavecct"]).aggregate("sum")).reset_index()
basica2324["year"] = 2023

basica = pd.concat([basica1920, basica2021, basica2122, basica2223, basica2324], ignore_index=True).rename(columns={"clavecct": "deped_id"})
basica["year"] = basica["year"].astype("Int64")

# print(basica.head())
# print(basica["year"].value_counts())


column_map = {"docentes_h": "total_teacher_male",
                "docentes_m": "total_teacher_female",
                "docentes": "total_teachers",
                "hombres": "total_student_male",
                "mujeres": "total_student_female",
                "alumnos": "total_student_enrollment"}


medias1920 = pd.read_csv("/Users/heatherbaier/Documents/geo_git/data/MEX/media_superior_2019-2020.csv")
medias1920 = medias1920.rename(columns = column_map)
medias1920 = medias1920[["escuela"] + list(column_map.values())]
medias1920["escuela"] = medias1920["escuela"].astype(str).str[0:-1]
medias1920 = pd.DataFrame(medias1920.groupby(["escuela"]).aggregate("sum")).reset_index()
medias1920["year"] = 2019

medias2021 = pd.read_csv("/Users/heatherbaier/Documents/geo_git/data/MEX/media_superior_2020-2021.csv")
medias2021 = medias2021.rename(columns = column_map)
medias2021 = medias2021[["escuela"] + list(column_map.values())]
medias2021["escuela"] = medias2021["escuela"].astype(str).str[0:-1]
medias2021 = pd.DataFrame(medias2021.groupby(["escuela"]).aggregate("sum")).reset_index()
medias2021["year"] = 2020

medias2122 = pd.read_csv("/Users/heatherbaier/Documents/geo_git/data/MEX/media_superior_2021-2022.csv")
medias2122 = medias2122.rename(columns = column_map)
medias2122 = medias2122[["escuela"] + list(column_map.values())]
medias2122["escuela"] = medias2122["escuela"].astype(str).str[0:-1]
medias2122 = pd.DataFrame(medias2122.groupby(["escuela"]).aggregate("sum")).reset_index()
medias2122["year"] = 2021

medias2223 = pd.read_csv("/Users/heatherbaier/Documents/geo_git/data/MEX/media_superior_2022-2023.csv")
medias2223 = medias2223.rename(columns = column_map)
medias2223 = medias2223[["escuela"] + list(column_map.values())]
medias2223["escuela"] = medias2223["escuela"].astype(str).str[0:-1]
medias2223 = pd.DataFrame(medias2223.groupby(["escuela"]).aggregate("sum")).reset_index()
medias2223["year"] = 2022

medias2324 = pd.read_csv("/Users/heatherbaier/Documents/geo_git/data/MEX/media_superior_2023-2024.csv")
medias2324 = medias2324.rename(columns = column_map)
medias2324 = medias2324[["escuela"] + list(column_map.values())]
medias2324["escuela"] = medias2324["escuela"].astype(str).str[0:-1]
medias2324 = pd.DataFrame(medias2324.groupby(["escuela"]).aggregate("sum")).reset_index()
medias2324["year"] = 2023


medias = pd.concat([medias1920, medias2021, medias2122, medias2223, medias2324], ignore_index=True).rename(columns={"escuela": "deped_id"})
medias["year"] = medias["year"].astype("Int64")

# print(medias.head())


ids = pd.read_csv("../../files_for_db/geo/mex_geo.csv")


basica = basica[["year", "deped_id", "total_teacher_male", "total_teacher_female", "total_teachers", "total_student_male", "total_student_female", "total_student_enrollment"]]
medias = medias[["year", "deped_id", "total_teacher_male", "total_teacher_female", "total_teachers", "total_student_male", "total_student_female", "total_student_enrollment"]]

result = pd.concat([basica, medias], ignore_index=True)
result = pd.merge(ids[["geo_id", "deped_id"]], result, on='deped_id', how='left').sort_values(by=['deped_id', 'year'])

print(result.head())
print(result.shape)
print(result["geo_id"].value_counts())
print(result["deped_id"].value_counts())



# daga

# Fill missing values in the 'geo_id' column with np.nan
result = result.fillna(np.nan)
result = result[result["geo_id"] != np.nan]
result = result[["geo_id", "year", "deped_id", "total_teacher_male", "total_teacher_female", "total_teachers", "total_student_male", "total_student_female", "total_student_enrollment"]]
print(result.head())

result.to_csv("../../files_for_db/personnel/mex_personnel.csv", index = False)

# dsaga






