import pandas as pd
import numpy as np


ids = pd.read_csv("../../files_for_db/geo/bra_geo.csv")
print(ids.shape)
id_dict = dict(zip(ids["deped_id"], ids["oedc_id"]))
print(ids.head())
final_columns = ["year", "deped_id", "total_teacher_male", "total_teacher_female", "total_teachers", "total_student_male", "total_student_female", "total_student_enrollment"]





def calculate_bra_personnel(file_path):

    print(file_path)

    bra_ef = pd.read_csv(file_path, sep = ";", encoding = "latin-1")
    
    # columns = ["year", "deped_id", "total_teacher_male", "total_teacher_female", "total_teachers", "total_student_male", "total_student_female", "total_student_enrollment"]

    columns = ["NU_ANO_CENSO", "CO_ENTIDADE", "QT_DOC_BAS", "QT_MAT_BAS_FEM", "QT_MAT_BAS_MASC", "QT_MAT_BAS"]

    bra_ef = bra_ef[columns].rename(columns = {"NU_ANO_CENSO": "year", 
                                                    "CO_ENTIDADE": "deped_id", 
                                                    "QT_DOC_BAS": "total_teachers", 
                                                    "QT_MAT_BAS_FEM": "total_student_female", 
                                                    "QT_MAT_BAS_MASC": "total_student_male", 
                                                    "QT_MAT_BAS": "total_student_enrollment"})
    # bra_ef["total_student_male"] = bra_ef["total_student_enrollment"] - bra_ef["total_student_female"]
    
    return bra_ef




tables = []

for year in range(2007, 2025):

    print(year)

    if year == 2024: 
        file_path = "/Users/heatherbaier/Documents/research/geo/data/BRA/microdados_censo_escolar_2024/dados/microdados_ed_basica_2024_new.csv"
    elif year == 2023:
        file_path = "/Users/heatherbaier/Documents/research/geo/data/BRA/microdados_censo_escolar_2023/dados/microdados_ed_basica_2023.csv"
    elif year == 2022:
        file_path = "/Users/heatherbaier/Documents/research/geo/data/BRA/Microdados do Censo Escolar da Educa‡Æo B sica 2022/dados/microdados_ed_basica_2022.csv"
    else:
        file_path = f"/Users/heatherbaier/Documents/research/geo/data/BRA/microdados_ed_basica_{year}/dados/microdados_ed_basica_{year}.csv"        

    tables.append(calculate_bra_personnel(file_path))


# print("Processing 2023")
# bra_personnel_2023 = calculate_bra_personnel("../../data/BRA/microdados_censo_escolar_2023/dados/use_for_2023.csv")
# tables.append(bra_personnel_2023)


bra_personnel = pd.concat(tables)
bra_personnel.head()

print(bra_personnel["year"].value_counts())


result = pd.merge(ids, bra_personnel, on='deped_id', how='left').sort_values(by=['deped_id', 'year'])


print(result["year"].value_counts())

for col in final_columns:
    if col not in result.columns:
        result[col] = np.nan
    if col in ["total_teacher_male", "total_teacher_female", "total_teachers", "total_student_male", "total_student_female", "total_student_enrollment"]:
        result[col] = result[col].fillna(np.nan).astype('Int64')

result = result[final_columns]


# # Fill missing values in the 'oedc_id' column with np.nan
# result = result.fillna(np.nan)
# result = result[result["oedc_id_x"] != np.nan]
# result = result[["oedc_id_x", "year", "deped_id", "total_teacher_male", "total_teacher_female", "total_teachers", "total_student_male", "total_student_female", "total_student_enrollment"]].rename(columns = {"oedc_id_x": "oedc_id"})
print(result.head())


print(result.shape)
result = result.drop_duplicates(subset=["deped_id", "year"], keep="last")
print(result.shape)


result.to_csv("../../files_for_db/personnel/bra_personnel.csv", index = False)