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


# 2010
data2010 = pd.read_csv("../../data/HND/12_Estadistica_inicial_2010_porNivelSubNivel.csv")
data2010 = data2010[['deped_id', 'total_teacher_female', 'total_teacher_male',
       'total_student_female', 'total_student_male']].fillna(0)
data2010["total_student_enrollment"] = data2010['total_student_female'] + data2010['total_student_male']
data2010["total_teachers"] = data2010['total_teacher_female'] + data2010['total_teacher_male']
data2010["year"] = 2010
data2010 = create_cols(data2010)
print(data2010.head())


# 2011
data2011 = pd.read_csv("../../data/HND/35_Matricula_inicial_por_grados_2011.csv").rename(columns = {"Codigo Centro": "deped_id"})
data2011["year"] = 2011
data2011["deped_id"] = data2011["deped_id"].fillna(np.nan).astype('Int64')
data2011 = data2011[["year", 'deped_id', "Valor Femenino", "Valor Masculino", "Total"]]
data2011.columns = ["year", "deped_id", "total_student_female", "total_student_male", "total_student_enrollment"]
data2011 = pd.DataFrame(data2011.groupby(["deped_id"]).aggregate("sum")).reset_index()#.rename(columns = {"total": "total_student_enrollment"})
data2011["year"] = 2011
data2011 = create_cols(data2011)
print(data2011.head())


# 2013
data2013 = pd.read_csv("../../data/HND/79_201308_USINIEH_Matricula_Inicial_2013_No_Oficial (2).csv").rename(columns = {"Codigo": "deped_id"}).fillna(0)
data2013["deped_id"] = data2013["deped_id"].fillna(np.nan).astype('Int64')
data2013["total"] = data2013["total"].str.replace(",", "").fillna(np.nan).astype('Int64')
data2013 = data2013[["deped_id", 'total']]
data2013 = pd.DataFrame(data2013.groupby(["deped_id"]).aggregate("sum")).reset_index().rename(columns = {"total": "total_student_enrollment"})
data2013["year"] = 2013
data2013 = create_cols(data2013)
print(data2013.head())


result = pd.concat([data2010, data2011, data2013], ignore_index=True)
result = result[result["deped_id"] != 0]

# result["geo_id"] = result["deped_id"].map(id_dict)
# result = result[~result["geo_id"].isna()]
# result = result[["geo_id", "year", "deped_id", "total_teacher_male", "total_teacher_female", "total_teachers", "total_student_male", "total_student_female", "total_student_enrollment"]]
# print(result.head())





result = pd.merge(ids, result, on='deped_id', how='left')
# Fill missing values in the 'geo_id' column with np.nan
result = result.fillna(np.nan)
result = result[result["geo_id"] != np.nan]
result = result[["geo_id", "year", "deped_id", "total_teacher_male", "total_teacher_female", "total_teachers", "total_student_male", "total_student_female", "total_student_enrollment"]]
print(result.head(10))

result = result.drop_duplicates(subset=["deped_id", "year"], keep="last")

result.to_csv("../../files_for_db/personnel/hnd_personnel.csv", index = False)