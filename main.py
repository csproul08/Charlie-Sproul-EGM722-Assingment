import pandas as pd
import folium

# Load OS Grid Ref CSV and Storm Overflow Annual Return .xlsx file
sewers = pd.read_csv('os_grid_ref.csv')
excel_file = 'EDM 2022 Storm Overflow Annual Return - all water and sewerage companies.xlsx'
spilltime = pd.read_excel(excel_file, sheet_name=None)

# Combine data from .xlsx worksheets as single DataFrame
spilltime_all = pd.concat(spilltime.values(), ignore_index=True)

print(sewers.head())
print(spilltime_all.head())

# Change name of spilltime .xls column 'EA Permit Reference (EA Consents Database) to 'PERMIT_NUMBER'

# Join OS Grid Ref CSV and Storm Overflow Annual Return .xls file based on column 'PERMIT_NUMBER'


# Remove columns no longer needed
# Need to add columns from spillsite table
df = sewers.drop(columns=['EFFLUENT_GRID_REF', 'DISCHARGE_SITE_TYPE_CODE', 'DISTRICT_COUNCIL', 'CATCHMENT_CODE', 'EA_REGION',
 'PERMIT_VERSION', 'RECEIVING_ENVIRON_TYPE_CODE', 'REC_ENV_CODE_DESCRIPTION', 'ISSUED_DATE',
'EFFECTIVE_DATE', 'REVOCATION_DATE', 'STATUS_OF_PERMIT','STATUS_DESCRIPTION', 'OUTLET_NUMBER',
                          'OUTLET_TYPE_CODE', 'OUTLET_GRID_REF', 'EFFLUENT_NUMBER'])


# Save joined file into new csv ready to be loaded for folium interactive map



# Create a map centered at specific coordinates
m = folium.Map(location=[center_lat, center_lon], zoom_start=5)

# Add markers for each location in the DataFrame
for row in sewers.itertuples():
    folium.Marker(
        location=[row.lat, row.lon],
        tooltip=row.location
    ).add_to(m)

# Display the map
m

# Load csv as dataframe and define crs
df = pd.read_csv('os_grid_ref.csv')
crs = {'init':'epsg:4326'}

plt.ion() # make the plotting interactive




