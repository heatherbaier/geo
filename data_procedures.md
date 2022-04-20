# Data Collection and Cleaning Procedures

Important note on data collection: **GEO only collects school-level data!** Do not download, save or clean aggregated data.

### 1. Save the data & the link to the data
Before you start cleaning, save any original data files to the data/{ISO-3c} folder. If a fodler doesn't exist for the country you are working on, make one. Save *all* of the original data here. Create or add to the file metadata/{ISO-3c}.txt information about your data. This file should be formatted such that the name of the file is on line X and then the line immediatley beow it should be indented 1 tab and should ocnatin the exact link to where you got the data. The line imediatley below that should be again indented 1 tab and should be the data you retrieved teh file in teh format MM/DD/YYYY. See other files in metadata/ for examples. 


### 2. Generate School IDS  
When you find a spreadsheet or shaepfile for a country not already inour database that has school coordinates, you'll need to generate GEO specific school ID's for each of the schools that are mapped totheir DepEd/contry-specific school IDs. Look in the scripts/ids/ folder for examples of how to do this. If there is no school name or DepEd ID column in the dataframe, then fill the columns with None values. You will save a spreadhseet to the files_for_db folder with the title {ISO-3c}_ids.csv. The cleaned spreadsheet will have three columns with these names and in this order:
    - geo_id
    - deped_id
    - school_name  
- This only needs to be done in two cases: 
    1. The first time a country is added to the database
    2. Whenever new schools are identified wthin the database. In this case, previous school ID's will NOT change, the new school ID's will pick up where the numbering left off.



### 3. Create School Coordinate Spreadsheets

1. Remove all rows (i.e. schools) in the spreadsheet that have missing coordinates  
2. Format the table so that there are four columns in the order: 
    1. school_id
    2. year
    3. longitude
    4. latitude
3. Save the table with the name: “{ISO_3C}_{YEAR}_education_facilities.csv”
