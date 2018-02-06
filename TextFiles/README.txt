Files included with this project:

MISC:
- README.txt 
	* this is what you are reading
- BNixon_OSM_MapArea.txt 
	* contains the OSM link and description of the map area I examined

PROJECT DOCUMENT:
- Wrangle_OSM_BNixon.html 
	* contains the explanations, code examples, and results from the project

XML FILES:
- Charlotte_sample.xml 
	* XML document containing a ~5mb sample of map data
- Charlotte_AOI.xml 
	* XML document containing the entire 58mb of map data used in the project

PYTHON FILES:
**data acquisition**
- OSM_data_acquisition.py
	* uses the Overpass API to export XML file for map area described using the Overpass API export link
**for pre-cleaning audit of data**
- explore_element_types.py
	* lists element names and counts of each name-type
- colonANDprobchar_count.py
	* processes each tag element, looking for colon-structured values and problem characters, yielding a count of each type 
- colonANDprobchar_overview.py
	* processes each tag element, looking for colon-structured values and problem characters, printing each unique type of tag
- street_type_audit.py
	* processes each element in file, looking for values with street information and problematic street types; yields all street values and all problematic street types
**data processing and cleaning**
- schema.py 
	* script that contains a dictionary schema used by the "validate_element" function, which makes sure that the dictionary created from each element has the right data types and format. 
- XMLcleanANDwriteCSV.py 
	* primary script to parse XML file, clean data, and write data to CSV files

CSVs:
- nodes.csv
	* CSV containing the data destined for the nodes SQL table
- nodes_tags.csv
	* CSV containing the data destined for the nodes_tags SQL table
- ways.csv
	* CSV containing the data destined for the ways SQL table
- ways_nodes.csv
	* CSV containing the data destined for the ways_nodes SQL table
- ways_tags.csv
	* CSV containing the data destined for the ways_tgs SQL table

SQLITE FILES:
- SQL_code_for_charlotte_osm_db.sql
	* contains the sqlite3 code to define the tables/schemas, import the CSVs to each table, delete any superfluous header rows, and create two views
- charlotte_osm.db
	* Sqlite database containing the map data
- clt_osm_db_Keys.txt
	* text file with an easy reference for the table structure and column names

		





			

	
			