import pandas as pd

#import data
#file located at ../../data/ARG is a zip file and needs to be downloaded and unzipped
arg_table = pd.read_excel("Mae actualizado 2019-09-16_Envios.xls", header=11)

#select only primary and secondary schools
arg_table = arg_table[(arg_table["Primaria"] == "X") | (arg_table["Secundaria"] == "X") | (arg_table["Secundaria Técnica (INET)"] == "X")]
arg_table.reset_index(inplace = True)

#select and rename necessary columns
arg_table = arg_table[["CUE Anexo", "Nombre", "Jurisdicción", "Departamento"]]
arg_table.columns = ["country_id", "school_name", "adm1", "adm2"]

#generate geo_ids
arg_table.reset_index(inplace=True)
arg_table["geo_id"] = arg_table["index"].apply(lambda x: 'ARG-{0:0>6}'.format(x))

#create and reorder colums
arg_table["address"] = None
arg_table["adm0"] = "ARG"
arg_table["adm3"] = None

arg_table = arg_table[["geo_id", "country_id", "school_name", "address", "adm0", "adm1", "adm2", "adm3"]]

#export as csv
arg_table.to_csv("../../files_for_db/ids/arg_ids.csv", index=False)