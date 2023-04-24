import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# Load OS Grid Ref CSV and Storm Overflow Annual Return .xlsx file
sewers = pd.read_csv('os_grid_ref.csv')
excel_file = 'EDM 2022 Storm Overflow Annual Return - all water and sewerage companies.xlsx'
spilltime_all = pd.concat(pd.read_excel(excel_file, sheet_name=None).values(), ignore_index=True)

# Change name of spilltime .xls column 'EA Permit Reference (EA Consents Database) to 'PERMIT_NUMBER'
spilltime_all.columns = spilltime_all.columns.str.replace("EA Permit Reference (EA Consents Database)", "PERMIT_NUMBER")

# save spilltime_all xlsx as a csv file for merge function
spilltime_all.to_csv('spilltime_all.csv', encoding='utf-8')

# Move the column name from the second row of the spilltime_all.csv file and set this as the column name, to allow the
# merge function to take place for both csv files
spilltime_all.columns = spilltime_all.iloc[0]

# remove the second row as this is no longer needed
spilltime_all = spilltime_all.drop(index=1)

# Change the name of the column called 'EA Permit Reference\n(EA Consents Database)' to 'PERMIT_NUMBER' to allow for
# a merge of both csv files
spilltime_all = spilltime_all.rename(columns={'EA Permit Reference\n(EA Consents Database)': 'PERMIT_NUMBER'})

# Merge both csv files using 'PERMIT_NUMBER' as a common column
sewers_spilltime = pd.merge(sewers, spilltime_all, on='PERMIT_NUMBER')

# Remove columns no longer needed for later analysis
sewers_spilltime = sewers_spilltime.drop(
    columns=['EFFLUENT_GRID_REF', 'DISCHARGE_SITE_TYPE_CODE', 'DISTRICT_COUNCIL', 'CATCHMENT_CODE', 'EA_REGION',
             'PERMIT_VERSION', 'RECEIVING_ENVIRON_TYPE_CODE', 'REC_ENV_CODE_DESCRIPTION', 'ISSUED_DATE',
             'EFFECTIVE_DATE', 'REVOCATION_DATE', 'STATUS_OF_PERMIT', 'STATUS_DESCRIPTION', 'OUTLET_NUMBER',
             'OUTLET_TYPE_CODE', 'OUTLET_GRID_REF', 'EFFLUENT_NUMBER', 'Water Company Name',
             'Site Name\n(EA Consents Database)',
             'Site Name\n(WaSC operational)\n[optional]', 'WaSC Supplementary Permit Ref.\n[optional]',
             'Activity Reference on Permit', 'Storm Discharge Asset Type',
             'Outlet Discharge NGR\n(EA Consents Database)',
             'WFD Waterbody ID (Cycle 2)\n(discharge outlet)',
             'WFD Waterbody Catchment Name (Cycle 2)\n(discharge outlet)',
             'Receiving Water / Environment (common name)\n(EA Consents Database)',
             'Shellfish Water (only populate for storm overflow with a Shellfish Water EDM requirement)',
             'Treatment Method\n(over & above Storm Tank settlement / screening)', 'Initial EDM Commission Date',
             'EDM Operation -\n% of reporting period EDM operational',
             'EDM Operation -\nReporting % -\nPrimary Reason <90%',
             'EDM Operation -\nAction taken / planned -\nStatus & timeframe',
             'High Spill Frequency -\nOperational Review -\nPrimary Reason',
             'High Spill Frequency -\nAction taken / planned -\nStatus & timeframe',
             'High Spill Frequency -\nEnvironmental Enhancement -\nPlanning Position (Hydraulic capacity)'])

# Split lat long data stored in 'DISCHARGE_NGR' column into two seperate columns, to allow conversion to shapefile
# for use with Folium
sewers_spilltime = sewers_spilltime.assign(lon=sewers_spilltime['DISCHARGE_NGR'].str.split(',').str[0],
                                           lat=sewers_spilltime['DISCHARGE_NGR'].str.split(',').str[1])

sewers_spilltime['geometry'] = list(zip(sewers_spilltime['lon'], sewers_spilltime['lat']))
sewers_spilltime['geometry'] = sewers_spilltime['geometry'].apply(Point)

# Delete the 'DISCHARGE_NGR' colum
sewers_spilltime.drop('DISCHARGE_NGR', axis=1, inplace=True)

# save the merged and cleaned DataFrame to a new csv file for use with folium
sewers_spilltime.to_csv('sewers_spill_merged.csv', index=False)

# Read the new dataframe and convert lat lon into a single coumn called geometry and apply as a point (instead of tuple)
spm = pd.read_csv('sewers_spill_merged.csv')
spm['geometry'] = list(zip(sewers_spilltime['lon'], sewers_spilltime['lat']))
spm['geometry'] = spm['geometry'].apply(Point)

# Create a new GeoDataFrame from the dataframe spm
gdf = gpd.GeoDataFrame(spm)
gdf.set_crs("EPSG:4326", inplace=True)

print(gdf)
gdf.to_file('spm_points.shp')

# Script to create map in folium and basemap, legend, etc...
my_map = folium.Map(location=[51.664386, 0.52167739], tiles="OpenStreetMap", prefer_canvas=True,
                    zoom_start=14, control_scale=True)

# Script to load spm_points (assign colour and point object), OS river network and OS green spaces
rivers = gpd.read_file(os.path.abspath('Data/WatercourseLink.shp'))
#greenspace = gpd.read_file(os.path.abspath('Data/GB_GreenspaceSite.shp'))

# Add shapefiles to map
folium.GeoJson(rivers).add_to(my_map)
#folium.GeoJson(greenspace).add_to(my_map)

my_map.save('HanningfieldV2.html')
# Script to load a few key details of each sewer outfall location, e.g site name, water company name, address/grid ref
# , water body name, total spill time in hrs, etc...


# Script to highlight section of river with a red colour if there is an active sewer outlet location
# e.g. if river is neighbour to outfall location and total spill time in last year >=1, show river as red.


# Script to find user location using device or to have a manual input for postcode


# Potential to add a hyperlink to EA contact us or to local Member of Parliament contact us webpage (this would rely
# upon ward area polygon and defining a webpage/local MP to contact based on device location or user inputted location


# Create a map centered at specific coordinates
# m = folium.Map(location=[center_lat, center_lon], zoom_start=5)

# Add markers for each location in the DataFrame
# for row in sewers.itertuples():
#    folium.Marker(
#        location=[row.lat, row.lon],
#       tooltip=row.location
#   ).add_to(m)

# Load csv as dataframe and define crs
# df = pd.read_csv('os_grid_ref.csv')
# crs = {'init':'epsg:4326'}

# plt.ion() # make the plotting interactive
