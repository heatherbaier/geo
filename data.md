## GEO Educational Data Overview



### Codebook

|Table|Description|Column Name|Column Description|
|---|---|---|---|
|Country-specific|Table mapping the GEO School ID’s to the ID’s used by the country’s DepEd|geo_id|GEO School ID|
|||country_id|Country given school ID|
|Coordinates|Table containing the longitude and latitude of every school|geo_id|GEO School iD|
|||longitude|Longitude|
|||latitude|Latitude|
|Basic|Table containing the basic & administrative spatial information about a school's location|geo_id|GEO School ID|
|||school_name|School Name|
|||address|Address of the school|
|||adm0|Name of zero-th level administrative boundary (i.e. country name) from GeoBoundaries dataset|
|||adm1|Name of first level administrative boundary from GeoBoundaries dataset|
|||adm2|Name of second level administrative boundary from GeoBoundaries dataset|
|||adm3|Name of Third level administrative boundary from GeoBoundaries dataset (if available)|
|Personnel|"Table containing data on admin| teacher and student profiles"|geo_id|GEO School ID|
|||year|School Year|
|||student_enrollment|Number of enrolled students during given year|
|||female_student_enrollment|Number of female-identifying students enrolled during given year|
|||male_student_enrollment|Number of male-identifying students enrolled during given year|
|||num_teachers|Number of instructional teachers during given year|
|||str|(Calculated) Student-Teacher Ratio|
|Resources|Table containing data on resources available to schools|geo_id||
|||year||
|||water||
|||internet||
|||electricity||
|||library||
|||cafeteria||
|Performance|Table containing data on school performance.|geo_id||
|||year||
|Finance|Table containing data on school financing|geo_id||
|||year||
|Protected|"Table containing data that the GEO team has deemed as sensitive. Data will be made available upon reasonable request. Data request form can be access here: . Our data ethics framework can be accessed here:"|idg_students|Number of students of indigenous descent|
|||sped_students|Number of students with learning disabilities|
|||disabled_students|Number of students with physical disabilities|
|||pov_students|Number of students living below the poverty line|