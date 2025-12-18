import pandas as pd
import numpy as np


"""
Proportion of schools with access to: 
(a) electricity; 
(b) the Internet for pedagogical purposes; 
(c) computers for pedagogical purposes; 
(d) adapted infrastructure and materials for students with disabilities; 
(e) basic drinking water; 
(f) single-sex basic sanitation facilities; and 
(g) basic handwashing facilities (as per the WASH indicator definitions)

	oedc_id VARCHAR NOT NULL, 
	year VARCHAR NOT NULL, 
	deped_id VARCHAR,
	water VARCHAR,
	internet VARCHAR,
	electricity VARCHAR,
	computers VARCHAR,
	disability_infrastructure VARCHAR,
	sanitation_facilities VARCHAR,
	ss_sanitation_facilities VARCHAR,
	handwashing_facilities VARCHAR
"""


ids = pd.read_csv("../../files_for_db/geo/bra_geo.csv")
print(ids.shape)
id_dict = dict(zip(ids["deped_id"], ids["oedc_id"]))
print(ids.head())
final_columns = ["year", "deped_id", "total_teacher_male", "total_teacher_female", "total_teachers", "total_student_male", "total_student_female", "total_student_enrollment"]





def calculate_bra_resources(file_path):

    print(file_path)

    bra_ef = pd.read_csv(file_path, sep = ";", encoding = "latin-1")
    
    # columns = ["year", "deped_id", "total_teacher_male", "total_teacher_female", "total_teachers", "total_student_male", "total_student_female", "total_student_enrollment"]

    columns = ["NU_ANO_CENSO", "CO_ENTIDADE", "IN_ENERGIA_INEXISTENTE", "QT_COMP_ALUNO", "IN_INTERNET_APRENDIZAGEM", "IN_DEPENDENCIAS_PNE", "IN_BANHEIRO", \
               "IN_AGUA_POTAVEL", "IN_AGUA_FILTRADA", "IN_AGUA_REDE_PUBLICA", "IN_AGUA_POCO_ARTESIANO", "IN_ESGOTO_REDE_PUBLICA", "IN_ESGOTO_FOSSA_SEPTICA"]

    bra_ef = bra_ef[columns].rename(columns = {"NU_ANO_CENSO": "year", 
                                                    "CO_ENTIDADE": "deped_id", 
                                                    "QT_COMP_ALUNO": "computers",
                                                    "IN_ENERGIA_INEXISTENTE": "electricity", 
                                                    "IN_DEPENDENCIAS_PNE": "disability_infrastructure", 
                                                    "IN_INTERNET_APRENDIZAGEM": "internet"
                                                    # "QT_MAT_BAS_MASC": "total_student_male", 
                                                    # "QT_MAT_BAS": "total_student_enrollment"
                                                    })    
    
    water_cols = ["IN_AGUA_POTAVEL", "IN_AGUA_FILTRADA", "IN_AGUA_REDE_PUBLICA", "IN_AGUA_POCO_ARTESIANO"]
    bra_ef["water"] = (bra_ef[water_cols] == 1).any(axis=1).fillna(np.nan).astype('Int64')
    bra_ef = bra_ef.drop(water_cols, axis = 1)
    
    bra_ef["computers"] = (bra_ef["computers"] > 0).fillna(np.nan).astype('Int64')

    bra_ef["internet"] = bra_ef["internet"].fillna(np.nan).astype('Int64')
    bra_ef["electricity"] = bra_ef["electricity"].map({0: 1, 1: 0}).fillna(np.nan).astype('Int64')
    # bra_ef["electricity"] = bra_ef["electricity"]
    bra_ef["disability_infrastructure"] = bra_ef["disability_infrastructure"].fillna(np.nan).astype('Int64')
    bra_ef["year"] = bra_ef["year"].astype('Int64')

    for col in ["sanitation_facilities", "ss_sanitation_facilities", "handwashing_facilities"]:
        if col not in bra_ef.columns:
            bra_ef[col] = np.nan

    bra_ef = bra_ef[["year", "deped_id", "water", "internet", "electricity", "computers", "disability_infrastructure", "sanitation_facilities", "ss_sanitation_facilities", "handwashing_facilities"]]#, ]]

    return bra_ef





tables = []

for year in range(2007, 2023):

    print(year)

    if year == 2024: 
        file_path = "/Users/heatherbaier/Documents/research/geo/data/BRA/microdados_censo_escolar_2024/dados/microdados_ed_basica_2024_new.csv"
    elif year == 2023:
        # file_path = "/Users/heatherbaier/Documents/research/geo/data/BRA/microdados_censo_escolar_2023/dados/microdados_ed_basica_2023.csv"
        continue
    elif year == 2022:
        file_path = "/Users/heatherbaier/Documents/research/geo/data/BRA/Microdados do Censo Escolar da Educa‡Æo B sica 2022/dados/microdados_ed_basica_2022.csv"
    else:
        file_path = f"/Users/heatherbaier/Documents/research/geo/data/BRA/microdados_ed_basica_{year}/dados/microdados_ed_basica_{year}.csv"        

    tables.append(calculate_bra_resources(file_path))


# print("Processing 2023")
# bra_resources_2023 = calculate_bra_resources("../../data/BRA/microdados_censo_escolar_2023/dados/use_for_2023.csv")
# tables.append(bra_resources_2023)


bra_resources = pd.concat(tables)
print(bra_resources.head())

print(bra_resources["year"].value_counts())



# agda


result = pd.merge(ids, bra_resources, on='deped_id', how='left').sort_values(by=['deped_id', 'year'])


print(result["year"].value_counts())


# # Fill missing values in the 'oedc_id' column with np.nan
# result = result.fillna(np.nan)
# result = result[result["oedc_id_x"] != np.nan]
# result = result[["oedc_id_x", "year", "deped_id", "total_teacher_male", "total_teacher_female", "total_teachers", "total_student_male", "total_student_female", "total_student_enrollment"]].rename(columns = {"oedc_id_x": "oedc_id"})
print(result.head())


print(result.shape)
result = result.drop_duplicates(subset=["deped_id", "year"], keep="last")
print(result.shape)

result = result[["oedc_id", "year", "deped_id", "water", "internet", "electricity", "computers", "disability_infrastructure", "sanitation_facilities", "ss_sanitation_facilities", "handwashing_facilities"]]

print(result.head())

result.to_csv("../../files_for_db/resources/bra_resources.csv", index = False)