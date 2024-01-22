import pandas as pd

#import data from github
cri_table1 = pd.read_excel("../../data/CRI/MATRICULA_INICIAL_COLEGIOS_2014-2021_POR_AÑO_CURSADO_Y_SEXO.xlsx", header=2)
cri_table2 = pd.read_excel("../../data/CRI/MATRICULA_INICIAL_ESCUELAS_DIURNAS_2014-2021_POR_AÑO_CURSADO_Y_SEXO.xlsx", header=2)

#append tables
cri_table1 = cri_table1[["NOMBRE", "PROVINCIA", "CANTON", "DISTRITO"]]
cri_table2 = cri_table2[["NOMBRE", "PROVINCIA", "CANTON", "DISTRITO"]]
cri_table = cri_table1.append(cri_table2)

#drop duplicate entries
#there are so many duplicates because this data covers multiple years
cri_table.drop_duplicates(inplace=True)
cri_table.reset_index(inplace=True, drop=True)

#rename files
cri_table.columns = ["school_name", "adm1", "adm2", "adm3"]

#create geo_ids
cri_table.reset_index(inplace=True)
cri_table["geo_id"] = cri_table["index"].apply(lambda x: 'CRI-{0:0>6}'.format(x))

#final additions and cleaning
cri_table["country_id"] = None
cri_table["address"] = None
cri_table["adm0"] = "CRI"
cri_table = cri_table[["geo_id", "country_id", "school_name", "address", "adm0", "adm1", "adm2", "adm3"]]

#export as csv
cri_table.to_csv("../../files_for_db/ids/cri_ids.csv", index=False)