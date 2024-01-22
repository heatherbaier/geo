import pandas as pd
from utils import *

ecu_table = pd.read_csv("MINEDUC_RegistrosAdministrativos_2021-2022-Fin.csv", header=None) #import data
ecu_table.columns = ecu_table.iloc[11] #add column names
ecu_table.drop(ecu_table.index[:12], inplace=True) #drop columns at beginning of dataset that just contain metadata
#reset index and create an index column for use in geo_id
ecu_table.reset_index(inplace=True)
ecu_table.drop(columns=["index"], inplace=True)
ecu_table.reset_index(inplace=True)

#create new dataframe with just necessary information
ecu_ids_table = ecu_table[["index","AMIE", "Nombre Institución", "Provincia", "Cantón", "Parroquia"]]
ecu_ids_table = ecu_ids_table.rename_axis(None, axis=1) #get rid of name leftover from adding column names
ecu_ids_table.columns = ["index", "deped_id", "school_name", "adm1", "adm2", "adm3"] #rename columns
#change data from all caps to titlecase
ecu_ids_table["school_name"] = ecu_ids_table["school_name"].str.title()
ecu_ids_table["adm1"] = ecu_ids_table["adm1"].str.title()
ecu_ids_table["adm2"] = ecu_ids_table["adm2"].str.title()
ecu_ids_table["adm3"] = ecu_ids_table["adm3"].str.title()
#add columns that are the same for all rows
ecu_ids_table["address"] = None 
ecu_ids_table["adm0"] = "ECU"
ecu_ids_table['geo_id'] = ecu_ids_table['index'].apply(lambda x: 'ECU-{0:0>6}'.format(x)) #add geo_id based on index
ecu_ids_table = ecu_ids_table[["geo_id", "deped_id", "school_name", "address", "adm0", "adm1", "adm2", "adm3"]] #rename columns and drop unnecessary columns

#export as csv
ecu_ids_table.to_csv("../../files_for_db/ids/ecu_ids.csv", index = False)