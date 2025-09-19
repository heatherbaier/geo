import pandas as pd
import numpy as np


ids = pd.read_csv("../../files_for_db/geo/hnd_geo.csv")
print(ids.shape)
id_dict = dict(zip(ids["deped_id"], ids["geo_id"]))

print(ids.head())

columns = ["year", "deped_id", "total_teacher_male", "total_teacher_female", "total_teachers", "total_student_male", "total_student_female", "total_student_enrollment"]


def create_cols(df):
    for col in columns:
        if col not in df.columns:
            df[col] = np.nan
    df = df[columns]
    return df




data2009 = pd.read_csv("../../data/HND/9_MatriculaFinalPorGrados_2009 (1).csv")
data2009 = data2009[['Codigo', 'Consolidada F', 'Consolidada M', 'Consolidada T']]
data2009.columns = ["deped_id", "total_student_female", "total_student_male", "total_student_enrollment"]
# print(data2009.dtypes)
for i in data2009.columns[1:]:
    data2009[i] = data2009[i].str.replace(",", "", regex=False).str.replace("-", "", regex=False).str.strip().replace("", np.nan).astype("Int64")     # <-- key part.astype("Int64")
# print(data2009.dtypes)
data2009 = pd.DataFrame(data2009.groupby(["deped_id"]).aggregate("sum")).reset_index()#.rename(columns = {"total": "total_student_enrollment"})
data2009["year"] = 2009
data2009["deped_id"] = data2009["deped_id"].fillna(np.nan).astype('Int64')
data2009 = create_cols(data2009)
# print(data2009.head())



# # 2010
# data2010 = pd.read_csv("../../data/HND/12_Estadistica_inicial_2010_porNivelSubNivel.csv")
# data2010 = data2010[['deped_id', 'total_teacher_female', 'total_teacher_male',
#        'total_student_female', 'total_student_male']].fillna(0)
# data2010["total_student_enrollment"] = data2010['total_student_female'] + data2010['total_student_male']
# data2010["total_teachers"] = data2010['total_teacher_female'] + data2010['total_teacher_male']
# data2010["year"] = 2010
# data2010 = create_cols(data2010)
# print(data2010.head())


# 2010
# teacher counts come from initial
data2010 = pd.read_csv("../../data/HND/12_Estadistica_inicial_2010_porNivelSubNivel.csv")
data2010 = data2010[['deped_id', 'total_teacher_female', 'total_teacher_male']].fillna(0)
data2010["total_teachers"] = data2010['total_teacher_female'] + data2010['total_teacher_male']
data2010["year"] = 2010

# student counts come from final
data2010_final = pd.read_csv("../../data/HND/Estadistica_final_2010_2011.csv")
# print(data2010_final.columns)
data2010_final = data2010_final[['Año', 'Codigo Centro', 'MATRICULA FINAL femenino', 'MATRICULA FINAL masculino']].fillna(0)
data2010_final = data2010_final[data2010_final['Año'] == 2010]
data2010_final = data2010_final.sort_values(by = 'Codigo Centro').drop(columns=['Año'], axis = 1)
data2010_final.columns = ["deped_id", "total_student_female", "total_student_male"]
data2010_final["total_student_enrollment"] = data2010_final['total_student_female'] + data2010_final['total_student_male']
data2010_final = pd.DataFrame(data2010_final.groupby(["deped_id"]).aggregate("sum")).reset_index()#.rename(columns = {"total": "total_student_enrollment"})
data2010 = pd.concat([data2010, data2010_final], axis=1)
data2010 = data2010.replace(",", "", regex=False).replace("-", "", regex=False).replace("", np.nan).astype("Int64")
data2010 = create_cols(data2010)
data2010 = data2010.loc[:, ~data2010.columns.duplicated()]

# print(data2010.head())





# 2011
# data2011 = pd.read_csv("../../data/HND/35_Matricula_inicial_por_grados_2011.csv").rename(columns = {"Codigo Centro": "deped_id"})
# data2011["year"] = 2011
# data2011["deped_id"] = data2011["deped_id"].fillna(np.nan).astype('Int64')
# data2011 = data2011[["year", 'deped_id', "Valor Femenino", "Valor Masculino", "Total"]]
# data2011.columns = ["year", "deped_id", "total_student_female", "total_student_male", "total_student_enrollment"]
# data2011 = pd.DataFrame(data2011.groupby(["deped_id"]).aggregate("sum")).reset_index()#.rename(columns = {"total": "total_student_enrollment"})
# data2011["year"] = 2011
# data2011 = create_cols(data2011)
# print(data2011.head())


data2011 = pd.read_csv("../../data/HND/Estadistica_final_2010_2011.csv")
# print(data2010_final.columns)
data2011 = data2011[['Año', 'Codigo Centro', 'MATRICULA FINAL femenino', 'MATRICULA FINAL masculino']].fillna(0)
data2011 = data2011[data2011['Año'] == 2011]
data2011 = data2011.sort_values(by = 'Codigo Centro').drop(columns=['Año'], axis = 1)
data2011.columns = ["deped_id", "total_student_female", "total_student_male"]
data2011["total_student_enrollment"] = data2011['total_student_female'] + data2011['total_student_male']
data2011 = pd.DataFrame(data2011.groupby(["deped_id"]).aggregate("sum")).reset_index()#.rename(columns = {"total": "total_student_enrollment"})
data2011 = data2011.replace(",", "", regex=False).replace("-", "", regex=False).replace("", np.nan).astype("Int64")
data2011 = create_cols(data2011)
data2011["year"] = 2011

# print(data2011.head())



# 2013
# data2013 = pd.read_csv("../../data/HND/79_201308_USINIEH_Matricula_Inicial_2013_No_Oficial (2).csv").rename(columns = {"Codigo": "deped_id"}).fillna(0)
# data2013["deped_id"] = data2013["deped_id"].fillna(np.nan).astype('Int64')
# data2013["total"] = data2013["total"].str.replace(",", "").fillna(np.nan).astype('Int64')
# data2013 = data2013[["deped_id", 'total']]
# data2013 = pd.DataFrame(data2013.groupby(["deped_id"]).aggregate("sum")).reset_index().rename(columns = {"total": "total_student_enrollment"})
# data2013["year"] = 2013
# data2013 = create_cols(data2013)
# print(data2013.head())


print(data2009.head())
print(data2010.head())
print(data2011.head())


print(data2009.shape)
print(data2010.shape)
print(data2011.shape)


result = pd.concat([data2009, data2010, data2011], ignore_index=True)
result = result[result["deped_id"] != 0]
result["geo_id"] = result["deped_id"].map(id_dict)
result = result[~result["geo_id"].isna()]
result = result[["geo_id", "year", "deped_id", "total_teacher_male", "total_teacher_female", "total_teachers", "total_student_male", "total_student_female", "total_student_enrollment"]]


# dsaga


result = pd.merge(ids, result, on='deped_id', how='left').sort_values(by=['deped_id', 'year'])

# Fill missing values in the 'geo_id' column with np.nan
result = result.fillna(np.nan)
result = result[result["geo_id_x"] != np.nan]
result = result[["geo_id_x", "year", "deped_id", "total_teacher_male", "total_teacher_female", "total_teachers", "total_student_male", "total_student_female", "total_student_enrollment"]].rename(columns = {"geo_id_x": "geo_id"})
print(result.head())


result = result.drop_duplicates(subset=["deped_id", "year"], keep="last")

result.to_csv("../../files_for_db/personnel/hnd_personnel.csv", index = False)