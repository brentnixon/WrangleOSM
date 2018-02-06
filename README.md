# Data Wrangling Project - Open Street Map
__Brent Nixon, Dec. 2017__

## Table of Contents

* <a href='#Introduction'>Introduction</a>
* <a href='#Extracting Data from OSM'>Extracting Data from OSM</a>
* <a href='#Overview of Data and Checking for Problems'>Overview of Data and Checking for Problems</a>
* <a href='#Data Processing and Cleaning'>Data Processing and Cleaning</a>
* <a href='#Loading Data into SQL'>Loading Data into SQL</a>
* <a href='#Exploration of Data with SQL'>Exploration of Data with SQL</a>
* <a href='#Worthy Options for Further Cleaning'>Worthy Options for Further Cleaning</a>

Reference:
http://sebastianraschka.com/Articles/2014_ipython_internal_links.html#top

## Introduction <a id='Introduction'></a>

>In this project, I will examine a section of the Open Street Map (OSM). To do this, I will extract the data from OSM, process the data programatically, look for issues in the data (such as cleanliness, uniformity, and validity), load the data into a local SQL database, and then explore the data using SQL to get an overview of the area.

>I chose to examine OSM data from the southeast part of Charlotte, North Carolina, which is where I grew up. 

>Navigate to this link to examine the bounding box describing the area I worked with: http://www.openstreetmap.org/relation/177415#map=11/35.2033/-80.8401

>Charlotte is an interesting city because it has a wide variety of urbanism. There is a dense urban core with high-rises, semi-urban mixed residential and commercial areas, sub-urban residential areas, and low-density sprawl. For a mapping project, there would certainly be a variety of features and idiosyncrasies to sort out. 

### To get a closer look at this project, download and open:
* ## ProjectDocument.html
>or 
* ## Wrangle_OSM_BNixon_jn.ipynb
