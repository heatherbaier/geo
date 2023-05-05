import pandas as pd

#import data from github
slv_table = pd.read_csv("../../data/SLV/datos_sedes_educativas.csv")

#select and rename necessary columns
slv_table = slv_table[["Departamento","Municipio", "Dirección", "Código sede", "Nombre sede"]]
slv_table.columns = ["adm1", "adm2", "address", "country_id", "school_name"]

#create geo_ids
slv_table.reset_index(inplace=True)
slv_table.reset_index(inplace=True)

#final formatting
slv_table["adm0"] = "SLV"
slv_table["adm3"] = None
slv_table = slv_table[["geo_id", "country_id", "school_name", "address", "adm0", "adm1", "adm2", "adm3"]]

#export as csv
slv_table.to_csv("../../files_for_db/ids/slv_ids.csv", index=False)