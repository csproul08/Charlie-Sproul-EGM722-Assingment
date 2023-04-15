import pandas as pd
import folium

# Load OS Grid Ref CSV and Storm Overflow Annual Return .xlsx file
sewers = pd.read_csv('os_grid_ref.csv')
excel_file = 'EDM 2022 Storm Overflow Annual Return - all water and sewerage companies.xlsx'
spilltime = pd.read_excel(excel_file, sheet_name=None)

# Combine data from .xlsx worksheets as single DataFrame
spilltime_all = pd.concat(spilltime.values(), ignore_index=True)

# Change name of spilltime .xls column 'EA Permit Reference (EA Consents Database) to 'PERMIT_NUMBER'
spilltime_all.columns = spilltime_all.columns.str.replace("EA Permit Reference (EA Consents Database)", "PERMIT_NUMBER")

# save spilltime_all xlsx as a csv file for merge function
spilltime_all.to_csv('spilltime_all.csv', encoding='utf-8')

# Move the column name from the second row of the spilltime_all.csv file and set this as the column name, to allow the
# merge function to take place for both csv files
spilltime_all.columns = spilltime_all.iloc[0]

#remove the second row as this is no longer needed
spilltime_all = spilltime_all.drop(index=1)

# Change the name of the column called 'EA Permit Reference\n(EA Consents Database)' to 'PERMIT_NUMBER' to allow for a merge of both csv files
spilltime_all = spilltime_all.rename(columns={'EA Permit Reference\n(EA Consents Database)': 'PERMIT_NUMBER'})

# Merge both csv files using 'PERMIT_NUMBER' as a common column
sewers_spilltime = pd.merge(sewers, spilltime_all, on='PERMIT_NUMBER')

# Remove columns no longer needed for later analysis
sewers_spilltime = sewers_spilltime.drop(columns=['EFFLUENT_GRID_REF', 'DISCHARGE_SITE_TYPE_CODE', 'DISTRICT_COUNCIL', 'CATCHMENT_CODE', 'EA_REGION',
 'PERMIT_VERSION', 'RECEIVING_ENVIRON_TYPE_CODE', 'REC_ENV_CODE_DESCRIPTION', 'ISSUED_DATE',
'EFFECTIVE_DATE', 'REVOCATION_DATE', 'STATUS_OF_PERMIT','STATUS_DESCRIPTION', 'OUTLET_NUMBER',
'OUTLET_TYPE_CODE', 'OUTLET_GRID_REF', 'EFFLUENT_NUMBER', 'Water Company Name', 'Site Name\n(EA Consents Database)',
'Site Name\n(WaSC operational)\n[optional]', 'WaSC Supplementary Permit Ref.\n[optional]',
'Activity Reference on Permit', 'Storm Discharge Asset Type', 'Outlet Discharge NGR\n(EA Consents Database)',
'WFD Waterbody ID (Cycle 2)\n(discharge outlet)', 'WFD Waterbody Catchment Name (Cycle 2)\n(discharge outlet)',
'Receiving Water / Environment (common name)\n(EA Consents Database)',
'Shellfish Water (only populate for storm overflow with a Shellfish Water EDM requirement)',
'Treatment Method\n(over & above Storm Tank settlement / screening)', 'Initial EDM Commission Date',])

print(sewers_spilltime.columns)

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




