import pandas as pd

# import GEO IDs file
ids = pd.read_csv("../../files_for_db/geo/hnd_geo.csv")

# limit files to just IDs
ids = ids[["geo_id", "deped_id"]]

# read in 2011 data
data_2011 = pd.read_excel("../../data/HND/35_Matricula_inicial_por_grados_2011.xlsx")

# select and rename relevant columns
data_2011 = data_2011[["Codigo Centro", "Valor Femenino", "Valor Masculino", "Total"]]
data_2011.columns = ["deped_id", "total_student_female", "total_student_male", "total_student_enrollment"]

# add column for year
data_2011["year"] = 2011

# read in 2013 data
data_2013 = pd.read_excel("90_201311_USINIEH_Matricula_Inicial_2013_SEE_por_Grado.xlsx", header=None)
data_2013.columns = data_2013.iloc[1]
data_2013 = data_2013[2:]

# group together students of different ages
data_2013 = data_2013.groupby(lambda x:x, axis=1).sum()

# select and rename relevant columns
data_2013 = data_2013[["Código", "Femenino", "Masculino"]]
data_2013.columns = ["deped_id", "total_student_female", "total_student_male"]

# add column for year
data_2013["year"] = 2013

# create column for total student count
data_2013["total_student_enrollment"] = data_2013["total_student_female"] + data_2013["total_student_male"]

# concatenate 2011 and 2013 data
data = pd.concat([data_2011, data_2013], ignore_index = True)

# merge personnel data with IDs
# I kept entries without geoids, if you don't want this then just remove the how = "left" argument
data = pd.merge(data, ids, on = "deped_id", how = "left")

# add null columns for teacher counts
data["total_teacher_male"] = None
data["total_teacher_female"] = None
data["total_teachers"] = None

# reorder columns
data = data[["geo_id", "year", "deped_id", "total_teacher_male", "total_teacher_female", "total_teachers",
             "total_student_male", "total_student_female", "total_student_enrollment"]]

# save data
data.to_csv("../../files_for_db/personnel/hnd_personnel.csv", index = False)