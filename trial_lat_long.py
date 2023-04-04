import pandas as pd
import geopandas as gpd
import pyproj
import re

class OsGridRef:
    def __init__(self, easting, northing):
        self.easting = int(easting)
        self.northing = int(northing)

    @staticmethod
    def parse(gridref):
        gridref = str(gridref).strip()

        # check for fully numeric comma-separated gridref format
        match = re.match(r"^(\d+),\s*(\d+)$", gridref)
        if match:
            return OsGridRef(match.group(1), match.group(2))

        # validate format
        match = re.match(r"^[HNST][ABCDEFGHJKLMNOPQRSTUVWXYZ]\s*\d+\s*\d+$", gridref, re.IGNORECASE)
        if not match:
            raise ValueError(f"Invalid grid reference: {gridref}")

        # get numeric values of letter references, mapping A->0, B->1, C->2, etc:
        l1 = ord(gridref.upper()[0]) - ord("A")  # 500km square
        l2 = ord(gridref.upper()[1]) - ord("A")  # 100km square
        # shuffle down letters after "I" since "I" is not used in grid:
        if l1 > 7:
            l1 -= 1
        if l2 > 7:
            l2 -= 1

        # convert grid letters into 100km-square indexes from false origin (grid square SV):
        e100km = ((l1 - 2) % 5) * 5 + (l2 % 5)
        n100km = (19 - (l1 // 5) * 5) - (l2 // 5)

        # skip grid letters to get numeric (easting/northing) part of ref
        en = gridref[2:].strip().split()
        # if e/n not whitespace separated, split half way
        if len(en) == 1:
            en = [en[0][: len(en[0]) // 2], en[0][len(en[0]) // 2 :]]

        # validation
        if len(en[0]) != len(en[1]):
            raise ValueError(f"Invalid grid reference: {gridref}")

        # standardise to 10-digit refs (metres)
        en[0] = en[0].ljust(5, "0")
        en[1] = en[1].ljust(5, "0")

        e = int(f"{e100km:d}{en[0]:s}")
        n = int(f"{n100km:d}{en[1]:s}")

        return OsGridRef(e, n)



gridrefs = ["TQ8400091000", "SP9081071430", "SP6454059690", "TL0278095370"]
for gridref in gridrefs:
    os_grid_ref = OsGridRef.parse(gridref)
    transformer = pyproj.Transformer.from_crs("EPSG:27700", "EPSG:4326", always_xy=True)
    lon, lat, _ = transformer.transform(os_grid_ref.easting, os_grid_ref.northing, 0)
    print(f"Grid Reference: {gridref} => Latitude: {lat:.6f}, Longitude: {lon:.6f}")

    # read the csv file containing sewer outlet locaitons
df = pd.read_csv("consents_active_filtered.csv")

# parse the os grid reference column
#df["0s_grid_ref"] = df["DISCHARGE_NGR"].apply(OsGridRef.parse)

# define the coordinate reference systems
#in_crs = pyproj.CRS("EPSG:27700")
#out_crs = pyproj.CRS("EPSG:4236")

# convert the os grid reference to lat and long
#df["lon"], df["lat"], _ = zip(*[out_crs.transform_point(easting, northing, in_crs) for easting, northing in df["Os_grid_ref"].apply(lambda x: (x.e, x.n))])

