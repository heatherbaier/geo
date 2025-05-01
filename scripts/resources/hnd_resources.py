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

	geo_id VARCHAR NOT NULL, 
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

# import ids
ids = pd.read_csv("../../files_for_db/geo/hnd_geo.csv")

# use only geo_id and deped_id from id file
ids = ids[["geo_id", "deped_id"]]


# # import raw resources data
data = pd.read_csv("../../data/HND/31_MatriculaInicial2011_Infraestructura_porCentroEducativoCompleto.csv", low_memory=False)
data = data.rename(columns = {"Tiene Internet": "internet", "Codigo.2": "deped_id"})
data['internet'] = data['internet'].map({"No": 0, "Si": 1})
data['water'] = data['Tipo Agua'].apply(lambda x: 1 if x in ['Potable', 'Well'] else (0 if pd.notnull(x) else np.nan))
data['electricity'] = data['Suministro Electricidad'].apply(
    lambda x: 1 if x in ['ENEE', 'Motor', 'Solar'] else (0 if x == 'Ninguno' else pd.NA)
)
data["computers"] = (
    data["Cant. PC Alumnos"] + data["Cant. PC Maestros"] + data["Cant. PC Administracion"]
).apply(lambda x: 1 if pd.notnull(x) and x > 0 else 0)
print(data.head())



data["year"] = 2011


# # merge to get geo_ids


# add columns with no values
data["handwashing_facilities"] = np.nan
data["sanitation_facilities"] = np.nan
data["ss_sanitation_facilities"] = np.nan
data["disability_infrastructure"] = np.nan

data = pd.merge(data, ids[["geo_id", "deped_id"]], on = "deped_id", how = "right")

data = data[["geo_id", "year", "deped_id", "water", "internet", "electricity", "computers", "disability_infrastructure", "sanitation_facilities", "ss_sanitation_facilities", "handwashing_facilities"]]

print(data['internet'].value_counts())


# # extract year from date
data["year"] = 2011


# replace all instances of True in the dataframe with 1 and all instances of False with 0 as integers
data = data.replace({True: 1, False: 0})

# convert all columns to integers
data["year"] = data["year"].fillna(np.nan).astype('Int64')
data["water"] = data["water"].fillna(np.nan).astype('Int64')
data["electricity"] = data["electricity"].fillna(np.nan).astype('Int64')
data["internet"] = data["internet"].fillna(np.nan).astype('Int64')
data["computers"] = data["computers"].fillna(np.nan).astype('Int64')
data["disability_infrastructure"] = data["disability_infrastructure"].fillna(np.nan).astype('Int64')
data["sanitation_facilities"] = data["sanitation_facilities"].fillna(np.nan).astype('Int64')
data["ss_sanitation_facilities"] = data["ss_sanitation_facilities"].fillna(np.nan).astype('Int64')
data["handwashing_facilities"] = data["handwashing_facilities"].fillna(np.nan).astype('Int64')

data = data.drop_duplicates(subset=["deped_id", "year"], keep="last")

print(data.head())

# # export
data.to_csv("../../files_for_db/resources/hnd_resources.csv", index = False)