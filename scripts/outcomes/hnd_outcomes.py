import pandas as pd
import numpy as np


ids = pd.read_csv("../../files_for_db/geo/hnd_geo.csv")
print(ids.shape)
id_dict = dict(zip(ids["deped_id"], ids["geo_id"]))

print(ids.head())

columns = ['year', 'deped_id', 'dropouts_female', 'dropouts_male', 'dropouts_total',
       'transfers_female', 'transfers_male', 'transfers_total',
       'promoted_female', 'promoted_male', 'promoted_total', 'failed_female',
       'failed_male', 'failed_total', 'graduates_female',
       'graduates_male', 'graduates_total']


def create_cols(df):
    for col in columns:
        if col not in df.columns:
            df[col] = np.nan
    df = df[columns]
    return df




data2009 = pd.read_csv("../../data/HND/9_MatriculaFinalPorGrados_2009 (1).csv")

# print(data2009.columns)

# dfgs

data2009 = data2009[['Codigo', 'Desertores F',
       'Desertores M', 'Desertores T', 'Traslados F', 'Traslados M',
       'Traslados T', 'Aprobados F', 'Aprobados M', 'Aprobados T',
       'Reprobados F', 'Reprobados M', 'Reprobados T', 'Graduados F',
       'Graduados M', 'Graduados T']]
rename_map = {
    'Codigo': 'deped_id',
    'Desertores F': 'dropouts_female',
    'Desertores M': 'dropouts_male',
    'Desertores T': 'dropouts_total',
    'Traslados F': 'transfers_female',
    'Traslados M': 'transfers_male',
    'Traslados T': 'transfers_total',
    'Aprobados F': 'promoted_female',
    'Aprobados M': 'promoted_male',
    'Aprobados T': 'promoted_total',
    'Reprobados F': 'failed_female',
    'Reprobados M': 'failed_male',
    'Reprobados T': 'failed_total',
    'Graduados F': 'graduates_female',
    'Graduados M': 'graduates_male',
    'Graduados T': 'graduates_total'
}
# Apply renaming
data2009 = data2009.rename(columns=rename_map)
# # print(data2009.dtypes)
for i in data2009.columns[1:]:
    data2009[i] = data2009[i].str.replace(",", "", regex=False).str.replace("-", "", regex=False).str.strip().replace("", np.nan).astype("Int64")     # <-- key part.astype("Int64")
# print(data2009.dtypes)
data2009 = pd.DataFrame(data2009.groupby(["deped_id"]).aggregate("sum")).reset_index()#.rename(columns = {"total": "total_student_enrollment"})
data2009["year"] = 2009
data2009["deped_id"] = data2009["deped_id"].fillna(np.nan).astype('Int64')
# data2009 = create_cols(data2009)
# print(data2009.columns)
# print(data2009.head())


# dsga


# 2010
# # student counts come from final
data2010_final = pd.read_csv("../../data/HND/Estadistica_final_2010_2011.csv")
print(data2010_final.columns)
rename_map = {
    'Año': 'year',
    'Codigo Centro': "deped_id",
    'DESERTORES femenino': 'dropouts_female',
    'DESERTORES masculino': 'dropouts_male',
    'TRASLADOS femenino': 'transfers_female',
    'TRASLADOS masculino': 'transfers_male',
    'APROBADOS femenino': 'promoted_female',
    'APROBADOS masculino': 'promoted_male',
    'REPROBADOS femenino': 'failed_female',
    'REPROBADOS masculino': 'failed_male',
    'GRADUADOS femenino': 'graduates_female',
    'GRADUADOS masculino': 'graduates_male'
}
# print(data2010_final.columns)
data2010_final = data2010_final[['Año', 'Codigo Centro', 'DESERTORES femenino', 'DESERTORES masculino', 'TRASLADOS femenino',
       'TRASLADOS masculino', 'APROBADOS femenino', 'APROBADOS masculino',
       'REPROBADOS femenino', 'REPROBADOS masculino', 'GRADUADOS femenino', 'GRADUADOS masculino']].fillna(0).rename(columns=rename_map)
data2010_final = data2010_final[data2010_final['year'] == 2010]
data2010_final = data2010_final.sort_values(by = 'deped_id').drop(columns=['year'], axis = 1)
data2010_final["dropouts_total"] = data2010_final['dropouts_female'] + data2010_final['dropouts_male']
data2010_final["transfers_total"] = data2010_final['transfers_female'] + data2010_final['transfers_male']
data2010_final["promoted_total"] = data2010_final['promoted_female'] + data2010_final['promoted_male']
data2010_final["failed_total"] = data2010_final['failed_female'] + data2010_final['failed_male']
data2010_final["graduates_total"] = data2010_final['graduates_female'] + data2010_final['graduates_male']
data2010_final = pd.DataFrame(data2010_final.groupby(["deped_id"]).aggregate("sum")).reset_index()#.rename(columns = {"total": "total_student_enrollment"})
data2010_final = data2010_final.replace(",", "", regex=False).replace("-", "", regex=False).replace("", np.nan).astype("Int64")
data2010_final = data2010_final.loc[:, ~data2010_final.columns.duplicated()]
data2010_final = create_cols(data2010_final)
data2010_final["year"] = 2010


# print(data2010_final.columns)
# print(data2010_final.head())




data2011_final = pd.read_csv("../../data/HND/Estadistica_final_2010_2011.csv")
# print(data2011_final.columns)
data2011_final = data2011_final[['Año', 'Codigo Centro', 'DESERTORES femenino', 'DESERTORES masculino', 'TRASLADOS femenino',
       'TRASLADOS masculino', 'APROBADOS femenino', 'APROBADOS masculino',
       'REPROBADOS femenino', 'REPROBADOS masculino', 'GRADUADOS femenino', 'GRADUADOS masculino']].fillna(0).rename(columns=rename_map)
data2011_final = data2011_final[data2011_final['year'] == 2011]
data2011_final = data2011_final.sort_values(by = 'deped_id').drop(columns=['year'], axis = 1)
data2011_final["dropouts_total"] = data2011_final['dropouts_female'] + data2011_final['dropouts_male']
data2011_final["transfers_total"] = data2011_final['transfers_female'] + data2011_final['transfers_male']
data2011_final["promoted_total"] = data2011_final['promoted_female'] + data2011_final['promoted_male']
data2011_final["failed_total"] = data2011_final['failed_female'] + data2011_final['failed_male']
data2011_final["graduates_total"] = data2011_final['graduates_female'] + data2011_final['graduates_male']
data2011_final = pd.DataFrame(data2011_final.groupby(["deped_id"]).aggregate("sum")).reset_index()#.rename(columns = {"total": "total_student_enrollment"})
data2011_final = data2011_final.replace(",", "", regex=False).replace("-", "", regex=False).replace("", np.nan).astype("Int64")
data2011_final = data2011_final.loc[:, ~data2011_final.columns.duplicated()]
data2011_final = create_cols(data2011_final)
data2011_final["year"] = 2011

# print(data2011_final.columns)
print(data2011_final.head())



# dagas




print(data2009.head())
print(data2010_final.head())
print(data2011_final.head())


print(data2009.shape)
print(data2010_final.shape)
print(data2011_final.shape)


result = pd.concat([data2009, data2010_final, data2011_final], ignore_index=True)
result = result[result["deped_id"] != 0]
result["geo_id"] = result["deped_id"].map(id_dict)
result = result[~result["geo_id"].isna()]
result = result[["geo_id", 'year', 'deped_id', 'dropouts_female', 'dropouts_male', 'dropouts_total',
       'transfers_female', 'transfers_male', 'transfers_total',
       'promoted_female', 'promoted_male', 'promoted_total', 'failed_female',
       'failed_male', 'failed_total', 'graduates_female',
       'graduates_male', 'graduates_total']]
result["year"] = result["year"].replace(",", "", regex=False).replace("-", "", regex=False).replace("", np.nan).astype("Int64")
# print(result.head())

# print(result.shape)

# dsaga


result = pd.merge(ids, result, on='deped_id', how='left').sort_values(by=['deped_id', 'year'])

# Fill missing values in the 'geo_id' column with np.nan
result = result.fillna(np.nan)
result = result[result["geo_id_x"] != np.nan]
result = result[["geo_id_x", 'year', 'deped_id', 'dropouts_female', 'dropouts_male', 'dropouts_total',
       'transfers_female', 'transfers_male', 'transfers_total',
       'promoted_female', 'promoted_male', 'promoted_total', 'failed_female',
       'failed_male', 'failed_total','graduates_female',
       'graduates_male', 'graduates_total']].rename(columns = {"geo_id_x": "geo_id"})
# print(result.head())
# print(result.shape)



result = result.drop_duplicates(subset=["deped_id", "year"], keep="last")


# daga

result.to_csv("../../files_for_db/outcomes/hnd_outcomes.csv", index = False)