# Charlie Sproul EGM722 Assignment

--- 

### Introduction
There are two scripts within this repository, the first undertakes a geodetic conversion of Ordnance Survey grid
reference positions for sewer outfall locations in England that are permitted under licence to discharge raw
untreated sewage in the river network at times of high flow rate. It converts the co-ordinates into longitude and 
laitude. The second script manipulates multiple data files 
and merges these, creating a shapefile of the sewer outfall locations in England. It also plots an interactive map
that displays and categorises the outfall locations based on the spill time of raw sewage into the River Network. 
Additionally, it plots the locations of bathing waters as published by the Environment Agency and creates a search bar
to enable the user to search for locations and to obtain information regarding the state of rivers nearby the user
inputted location. 
 
- - -

### Installation/Set up Instructions
The codes within this repository require the use of an Integrated Development Environment (IDE) and PyCharm is utilised 
by the author for this work. Additionally, a Jupyter Notebook is used for the Sewage Interactive Map and to run the 
environment for these scripts. 


All code, data files and dependencies can be found within the repository 'Charlie-Sproul' EGM722 Assignment, accessible
here: https://github.com/csproul08/Charlie-Sproul-EGM722-Assingment

--- 
### Requirements
Anaconda Navigator and PyCharm are both required and recommended for running both of these scripts. 

To install [PyCharm Community Edition](www.jetbrains.com/edu-products/download/other-PCE.html)

To install [Anaconda Navigator](docs.anaconda.com/free/navigator/index.html)

---
### Dependencies 
The following list sets out the dependencies required to run these scripts: 
- Python
- geopandas
- cartopy>=0.21
- notebook
- rasterio
- pyepsg
- folium
- pyproj
- tqdm
- pandas
- geopy
- pyogrio
- openpyxl