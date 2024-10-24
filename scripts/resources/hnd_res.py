import pandas as pd
import numpy as np

"""
Proportion of schools with access to: 
(a) electricity (Suministro_electrico); 
(b) the Internet for pedagogical purposes (tiene_internet); 
(c) computers for pedagogical purposes (pc_alimnos and pc_maestros); 
(d) adapted infrastructure and materials for students with disabilities (N/A); 
(e) basic drinking water (Forma_Almacenamiento_Agua, anything other than Ninguna); 
(f) single-sex basic sanitation facilities (N/A); and 
(g) basic handwashing facilities (N/A)
"""

# import files
data_2010 = pd.read_excel("../../data/HND/42_Infraestrcutura.xlsx", sheet_name = "2010")
data_2011 = pd.read_excel("../../data/HND/42_Infraestrcutura.xlsx", sheet_name = "2011")

# it does not seem that there are any deped_ids here, the closest is id_boleta but it's not the same structure
# in this code, I labled the id_boleta as the deped_id and left the geo_id column empty

# add years column
data_2010["year"] = 2010
data_2011["year"] = 2011

# concatenate data files
data = pd.concat([data_2010, data_2011], ignore_index = True)

# change electricity column so it's a binary indicator
data["Suministro_electrico"] = data["Suministro_electrico"].fillna("Ninguno")     # fill in nan's as Ninguno (None)
data["electricity"] = np.where(data["Suministro_electrico"] != "Ninguno", 1, 0)   # None is 0, rest is 1

# change internet column so it's a binary indicator
data["tiene_internet"] = data["tiene_internet"].fillna("No")        # fill in nan's with No
data["internet"] = np.where(data["tiene_internet"] != "No", 1, 0)   # No is 0, Si (yes) is 1

# fill in nan values and add together computer types
data["pc_alimnos"] = data["pc_alimnos"].fillna(0)
data["pc_maestros"] = data["pc_maestros"].fillna(0)
data["computers"] = data["pc_alimnos"] + data["pc_maestros"]

# change water column so it's a binary indicator
data["Forma_Almacenamiento_Agua"] = data["Forma_Almacenamiento_Agua"].fillna("Ninguno")   # fill in nan's as Ninguno (None)
data["water"] = np.where(data["Forma_Almacenamiento_Agua"] != "Ninguno", 1, 0)            # None is 0, rest is 1

# add empty columns
data["disability_infrastructure"] = None
data["sanitation_facilities"] = None
data["ss_sanitation_facilities"] = None
data["handwashing_facilities"] = None
data["geo_id"] = None

# change id_boleta to stand in as deped_id column
data["deped_id"] = data["id_boleta"]

# select and order relevant columns
data = data[["geo_id", "deped_id", "year", "electricity", "internet", "computers", "water", "disability_infrastructure",
         "sanitation_facilities", "ss_sanitation_facilities", "handwashing_facilities"]]

# save final file
data.to_csv("../../files_for_db/resources/hnd_resources.csv", index = False)