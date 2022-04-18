#### Generation of GEO School ID's

- This only needs to be done onin two cases: 
    1. The first time a country is added to the database
    2. Whenever new schools are identified wthin the database. In this case, previous school ID's will NOT change, the new school ID's will pick up where the numbering left off.



#### School Coordinate Spreadsheets

1. Remove all rows in the spreadsheet that have missing coordinates  
2. Format the table so that there are four columns in the order: 
    1. school_id
    2. year
    3. longitude
    4. latitude
3. Save the table with the name: “{ISO_3C}_{YEAR}_education_facilities.csv”
