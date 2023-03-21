import pandas as pd
from utils import *

#import data and format so json file will read better into dataframe
with open("../../data/KEN/schools.json") as schools_raw:
    schools_raw = schools_raw.read()[96:-1]
ken_table = pd.read_json(schools_raw)

#extract info from dictionaries to create columns
ken_table["adm1"] = None
ken_table["adm2"] = None
ken_table["adm3"] = None
ken_table["school_name"] = None

for i in range(len(ken_table)):
    ken_table["adm1"].iloc[i] = ken_table["properties"].iloc[i]["County"].title()
    ken_table["adm2"].iloc[i] = ken_table["properties"].iloc[i]["SUB_COUNTY"]
    ken_table["adm3"].iloc[i] = ken_table["properties"].iloc[i]["Ward"].title()
    if ken_table["adm3"].iloc[i] == " ":
        ken_table["adm3"].iloc[i] = None
    ken_table["school_name"].iloc[i] = ken_table["properties"].iloc[i]["SCHOOL_NAM"].title()

#clean adm3 inconsistencies
ken_table["adm3"] = ken_table["adm3"].str.replace('   ', ' ')
ken_table["adm3"] = ken_table["adm3"].str.replace('  ', ' ')
ken_table["adm3"] = ken_table["adm3"].str.replace('\\', '/')
ken_table["adm3"] = ken_table["adm3"].str.replace('-', '/')
ken_table["adm3"] = ken_table["adm3"].str.replace(' / ', '/')
ken_table["adm3"] = ken_table["adm3"].str.replace('/ ', '/')
ken_table["adm3"] = ken_table["adm3"].str.replace(' /', '/')
ken_table["adm3"] = ken_table["adm3"].str.replace('\n', '')
ken_table["adm3"] = ken_table["adm3"].str.replace("’", "'")
#these are inconsistencies I found by hand based on geoBoundaries adm3 names
ken_table["adm3"] = ken_table["adm3"].str.replace('Baba Dogo', 'Babadogo')
ken_table["adm3"] = ken_table["adm3"].str.replace('Bassi', 'Bobasi')
ken_table["adm3"] = ken_table["adm3"].str.replace('Basi', 'Bobasi')
ken_table["adm3"] = ken_table["adm3"].str.replace('Bobasi/Boitangare', 'Bobasi Boitangare')
ken_table["adm3"] = ken_table["adm3"].str.replace('Walatsi', 'Waltsi')
ken_table["adm3"] = ken_table["adm3"].str.replace('Centrl', 'Central')
ken_table["adm3"] = ken_table["adm3"].str.replace('Kimathi', 'Kimanthi')
ken_table["adm3"] = ken_table["adm3"].str.replace('Lenkism', 'Lenkisim')
ken_table["adm3"] = ken_table["adm3"].str.replace('Oo Nkidong', 'Oonkidong')
ken_table["adm3"] = ken_table["adm3"].str.replace("Kachieng'", "Kachien'G")
ken_table["adm3"] = ken_table["adm3"].str.replace('Lakezone', 'Lake Zone')
ken_table["adm3"] = ken_table["adm3"].str.replace('Loiyamorok', 'Loiyamorock')
ken_table["adm3"] = ken_table["adm3"].str.replace('Mackinon Road', 'Mackinnon Road')
ken_table["adm3"] = ken_table["adm3"].str.replace('Maji Moto', 'Majimoto')
ken_table["adm3"] = ken_table["adm3"].str.replace('Malaha/Isongo/Makun Ga', 'Isongo/Makunga/Malaha')
ken_table["adm3"] = ken_table["adm3"].str.replace('Malaha/Isongo/Makunga', 'Isongo/Makunga/Malaha')
ken_table["adm3"] = ken_table["adm3"].str.replace("Manyatta B", "Manyatta 'B'")
ken_table["adm3"] = ken_table["adm3"].str.replace('Muhoroni Koru', 'Muhoroni/Koru')
ken_table["adm3"] = ken_table["adm3"].str.replace('Mutitu', 'Mutito')
ken_table["adm3"] = ken_table["adm3"].str.replace('Muvau/Kikumini', 'Muvau/Kikuumini')
ken_table["adm3"] = ken_table["adm3"].str.replace('Namboboto/Nambuku', 'Namboboto Nambuku')
ken_table["adm3"] = ken_table["adm3"].str.replace('Naromoru/Kiamathaga', 'Naromoru Kiamathaga')
ken_table["adm3"] = ken_table["adm3"].str.replace("Nyalenda A", "Nyalenda 'A'")
ken_table["adm3"] = ken_table["adm3"].str.replace("Sarang'Ombe", "Sarangombe")
ken_table["adm3"] = ken_table["adm3"].str.replace('Shauri Moyo', 'Shaurimoyo')
ken_table["adm3"] = ken_table["adm3"].str.replace('Tulwet/Chiyat', 'Tulwet/Chuiyat')
ken_table["adm3"] = ken_table["adm3"].str.replace("Wang'Chieng", "Wangchieng")
ken_table["adm3"] = ken_table["adm3"].str.replace('Ingostse/Mathia', 'Ingostse-Mathia')
ken_table["adm3"] = ken_table["adm3"].str.replace('Ingotse/Matiha', 'Ingostse-Mathia') 

#create specific table for ids with only necessary columns
ken_table_ids = ken_table[["id", "adm1", "adm2", "adm3", "school_name"]]

#create geoIDs
ken_table_ids.reset_index(inplace=True)
ken_table_ids["geo_id"] = ken_table_ids["index"].apply(lambda x: 'KEN-{0:0>6}'.format(x))

#fill in remaining columns and reorder
ken_table_ids["address"] = None
ken_table_ids["adm0"] = "KEN"
ken_table_ids["country_id"] = ken_table_ids["id"]
ken_table_ids = ken_table_ids[["geo_id", "country_id", "school_name", "address", "adm0", "adm1", "adm2", "adm3"]]

#export as csv
ken_table_ids.to_csv("../../files_for_db/ids/ken_ids.csv", index=False)
