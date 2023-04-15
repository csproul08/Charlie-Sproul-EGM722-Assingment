import pandas as pd
import folium

sewers=pd.read_csv('os_grid_ref.csv')
sewers.head()

# Calculate the center of the map as the mean of the coordinates
center_lat = sewers['lat'].mean()
center_lon = sewers['lon'].mean()

# Create a map centered at the calculated coordinates
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

# generate matplotlib handles to create a legend of the features we put in our map.
def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles

sewers = gpd.read_file(os.path.abspath('data_files/os_grid_ref.csv'))



# Remove columns which are not needed
# df = df.drop(columns=['EFFLUENT_GRID_REF', 'DISCHARGE_SITE_TYPE_CODE', 'DISTRICT_COUNCIL', 'CATCHMENT_CODE', 'EA_REGION',
# 'PERMIT_NUMBER', 'PERMIT_VERSION', 'RECEIVING_ENVIRON_TYPE_CODE', 'REC_ENV_CODE_DESCRIPTION', 'ISSUED_DATE',
# 'EFFECTIVE_DATE', 'REVOCATION_DATE', 'STATUS_OF_PERMIT','STATUS_DESCRIPTION', 'OUTLET_NUMBER',
# 'OUTLET_TYPE_CODE', 'OUTLET_GRID_REF', 'EFFLUENT_NUMBER'])

# Print columns to check previous columns are deleted
# data = df.head()
# for col in data.columns:
    # print(col)
