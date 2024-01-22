import pandas as pd
import numpy as np

#import necessary data from github
zaf_table = pd.read_excel("../../data/ZAF/National.xlsx")

#select relevant columns
zaf_table = zaf_table[["NatEmis", "Province", "Official_Institution_Name", "EIDistrict", "LMunName", "StreetAddress"]]

#reformat data about adm 1
zaf_table["Province"] = zaf_table["Province"].str.replace("FS", "Free State").replace("ES", "Eastern Cape").replace("GT", "Gauteng").replace("KZN", "KwaZulu-Natal").replace("LP", "Limpopo").replace("MP", "Mpumalanga").replace("NC", "Northern Cape").replace("NW", "North West").replace("WC", "Western Cape").replace("Province", np.nan).replace("", np.nan).replace(" ", np.nan)

#rename columns
zaf_table.columns = ["country_id", "adm1", "school_name", "adm2", "adm3", "address"]

#create geo_ids and adm0 column
zaf_table.reset_index(inplace=True)
zaf_table["geo_id"] = zaf_table["index"].apply(lambda x: "ZAF-{0:0>6}".format(x))
zaf_table["adm0"] = "ZAF"

#final formatting and cleaning
zaf_table = zaf_table[["geo_id", "country_id", "school_name", "address", "adm0", "adm1", "adm2", "adm3"]]
zaf_table["address"] = zaf_table["address"].replace("", np.nan).replace(" ", np.nan)
zaf_table["adm2"] = zaf_table["adm2"].replace("", np.nan).replace(" ", np.nan)
zaf_table["adm3"] = zaf_table["adm3"].replace("", np.nan).replace(" ", np.nan)

#export as csv
zaf_table.to_csv("../../files_for_db/ids/zaf_ids.csv", index=False)