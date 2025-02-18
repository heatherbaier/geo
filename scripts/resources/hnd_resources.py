import pandas as pd

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
data['water'] = data['Tipo Agua'].apply(lambda x: 0 if x == 'Ninguna' else 1)
data['electricity'] = data['Suministro Electricidad'].apply(lambda x: 0 if x == 'Ninguno' else 1)
data["computers"] = data["Cant. PC Alumnos"] + data["Cant. PC Maestros"] + data["Cant. PC Administracion"]

print(data.head())


# # extract year from date
data["year"] = 2011


# # merge to get geo_ids


# add columns with no values
data["handwashing_facilities"] = -99
data["sanitation_facilities"] = -99
data["ss_sanitation_facilities"] = -99
data["disability_infrastructure"] = -99

data = pd.merge(data, ids[["geo_id", "deped_id"]], on = "deped_id")

data = data[["geo_id", "year", "deped_id", "water", "internet", "electricity", "computers", "disability_infrastructure", "sanitation_facilities", "ss_sanitation_facilities", "handwashing_facilities"]]

print(data['internet'].value_counts())

print(data.head())

# # export
data.to_csv("../../files_for_db/resources/hnd_resources.csv", index = False)