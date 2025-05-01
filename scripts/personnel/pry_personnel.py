import pandas as pd
import numpy as np

# import ids
ids_pry = pd.read_csv("../../files_for_db/geo/pry_geo.csv")
ids_pry = ids_pry[["geo_id", "deped_id"]]

# import all raw personnel data
pers_2012 = pd.read_csv("../../data/PRY/matriculaciones_educacion_escolar_basica_2012.csv")
pers_2013 = pd.read_csv("../../data/PRY/matriculaciones_educacion_escolar_basica_2013.csv")
pers_2018 = pd.read_csv("../../data/PRY/matriculaciones_educacion_escolar_basica_2018.csv")
pers_2019 = pd.read_csv("../../data/PRY/matriculaciones_educacion_escolar_basica_2019.csv")
pers_2020 = pd.read_csv("../../data/PRY/matriculaciones_educacion_escolar_basica_2020.csv")
pers_2021 = pd.read_csv("../../data/PRY/matriculaciones_educacion_escolar_basica_2021.csv")
pers_2022 = pd.read_csv("../../data/PRY/matriculaciones_educacion_escolar_basica_2022.csv")
pers_2023 = pd.read_csv("../../data/PRY/matriculaciones_educacion_escolar_basica_2023.csv")

# For each personnel file, fill the 'anio' column if necessary
for df in [pers_2012, pers_2013, pers_2018, pers_2019, pers_2020, pers_2021, pers_2022, pers_2023]:
    # If 'anio' is missing, fill it with the mode (most frequent value) of the column
    df["anio"] = df["anio"].fillna(df["anio"].mode()[0])
    # Uncomment the next line if you need to extract a 4-digit year from the column strings
    # df["anio"] = df["anio"].str.extract(r"(\d{4})")
    print(df["anio"].value_counts())

# Concatenate personnel files
pers_pry = pd.concat([pers_2012, pers_2013, pers_2018, pers_2019, pers_2020, pers_2021, pers_2022, pers_2023]).reset_index(drop=True)

# Choose and rename columns
pers_pry = pers_pry[["anio", "codigo_establecimiento", "total_matriculados_hombre", "total_matriculados_mujer"]]
pers_pry.columns = ["year", "deped_id", "total_student_male", "total_student_female"]

print("Rows with null year before merge: ", pers_pry["year"].isna().sum())

# Create a complete grid of school and year combinations.
# List all the years you expect (based on your files)
years = [2012, 2013, 2018, 2019, 2020, 2021, 2022, 2023]
# Get unique schools from ids_pry
schools = ids_pry["deped_id"].unique()

# Create a DataFrame with all combinations (a cartesian product)
school_year_grid = pd.DataFrame([(s, y) for s in schools for y in years],
                                columns=["deped_id", "year"])

# Merge with ids_pry to add the geo_id
school_year_grid = pd.merge(school_year_grid, ids_pry, on="deped_id", how="left")

# Now merge the personnel data with this complete grid.
# This is a left merge so that every school/year in our grid appears.
pers_pry_full = pd.merge(school_year_grid, pers_pry, on=["deped_id", "year"], how="left")

# At this point, any school-year combination that did not have personnel data has NaN in the corresponding columns.
# Fill these missing values with np.nan (year is already populated from the grid)
cols_to_fill = ["total_student_male", "total_student_female"]
pers_pry_full[cols_to_fill] = pers_pry_full[cols_to_fill].fillna(np.nan)

# Create a total student enrollment column (will be np.nan + np.nan = -198 when both values are missing)
pers_pry_full["total_student_enrollment"] = pers_pry_full["total_student_male"] + pers_pry_full["total_student_female"]

# Add columns for teacher info, populated with np.nan (if desired; adjust if you prefer a different fill for teacher columns)
pers_pry_full["total_teacher_male"] = np.nan
pers_pry_full["total_teacher_female"] = np.nan
pers_pry_full["total_teachers"] = np.nan

# Reorder columns as required
pers_pry_full = pers_pry_full[["geo_id", "year", "deped_id",
                               "total_teacher_male", "total_teacher_female", "total_teachers",
                               "total_student_male", "total_student_female", "total_student_enrollment"]]

print("Final shape of pers_pry_full:", pers_pry_full.shape)
print("Unique geo_id count:", len(pers_pry_full["geo_id"].unique()))

# Export the final personnel file
pers_pry_full.to_csv("../../files_for_db/personnel/pry_personnel.csv", index=False)
