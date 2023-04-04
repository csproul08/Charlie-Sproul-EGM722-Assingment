import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely import wkt

# check csv is correct
df = pd.read_csv('os_grid_ref.csv')
print (df[['COMPANY_NAME', 'DISCHARGE_NGR']])

