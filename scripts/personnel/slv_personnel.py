import pandas as pd
import numpy as np

#import necessary data from github
slv_table = pd.read_excel("../../data/SLV/Base de datos de Censo Final 2018.xlsx")
slv_ids = pd.read_csv("../../files_for_db/ids/slv_ids.csv")

#pivot so male and female enrollment become columns
slv_table = slv_table.pivot_table(index=["CODIGO", "AÑO"], columns="SEXO", values="TOTAL GENERAL", aggfunc=np.sum).reset_index()

#prep and merge data with id table
slv_table.columns = ["country_id", "year", "male_student_enrollment", "female_student_enrollment"]
slv_table["country_id"] = slv_table["country_id"].astype("str")
slv_table = pd.merge(slv_table, slv_ids, how="inner")

#add final columns
slv_table["student_enrollment"] = slv_table["female_student_enrollment"] + slv_table["male_student_enrollment"]
slv_table["num_teachers"] = None
slv_table["st_ratio"] = None

#final formatting
slv_table = slv_table[["geo_id", "year", "student_enrollment", "female_student_enrollment", "male_student_enrollment", "num_teachers", "st_ratio"]]

#export as csv
slv_table.to_csv("../../files_for_db/personnel/slv_pers.csv", index=False)