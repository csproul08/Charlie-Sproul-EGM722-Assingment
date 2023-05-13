import pandas as pd
import pyproj
import re
from tqdm import tqdm


# 1.1
class OsGridRef:
    def __init__(self, easting, northing):
        self.easting = int(easting)
        self.northing = int(northing)

    # 1.2/1.3
    @staticmethod
    def parse(gridref):
        gridref = str(gridref).strip()

        # Check that the grid reference is in a fully numeric comma separated format
        match = re.match(r"^(\d+),\s*(\d+)$", gridref)
        if match:
            return OsGridRef(match.group(1), match.group(2))

        # Validate the grid ref format, looking for a starting letter (HNST) and a second letter (not including I)
        match = re.match(r"^[HNST][ABCDEFGHJKLMNOPQRSTUVWXYZ]\s*\d+\s*\d+$", gridref, re.IGNORECASE)
        if not match:
            raise ValueError(f"Invalid grid reference: {gridref}")

        # 1.4 For each letter, get a numeric value starting at A = 0
        l1 = ord(gridref.upper()[0]) - ord("A")  # 500km square
        l2 = ord(gridref.upper()[1]) - ord("A")  # 100km square
        # As I is not used in OS Grid References (too similar to 1), reduce the numeric value of each letter past 7 by 1
        if l1 > 7:
            l1 -= 1
        if l2 > 7:
            l2 -= 1

        # 1.5 Convert the two letter grid reference into 100km-square indexes from a false origin (grid square SV):
        e100km = ((l1 - 2) % 5) * 5 + (l2 % 5)
        n100km = (19 - (l1 // 5) * 5) - (l2 // 5)

        # 1.6 skip grid letters to get the numeric (easting/northing) part of the reference
        en = gridref[2:].strip().split()
        # if e/n not whitespace separated, split half way
        if len(en) == 1:
            en = [en[0][: len(en[0]) // 2], en[0][len(en[0]) // 2:]]

        # validation
        if len(en[0]) != len(en[1]):
            raise ValueError(f"Invalid grid reference: {gridref}")

        # 1.7 standardise to 10-digit refs (metres)
        en[0] = en[0].ljust(5, "0")
        en[1] = en[1].ljust(5, "0")
        # 1.8
        e = int(f"{e100km:d}{en[0]:s}")
        n = int(f"{n100km:d}{en[1]:s}")

        return OsGridRef(e, n)


# 1.9 script to read the csv file
df = pd.read_csv('consents_active_filtered.csv')

# update the 'DISCHARGE_NGR' column with the new values and display % complete and estimated time remaining
for i, gridref in tqdm(enumerate(df['DISCHARGE_NGR']), total=len(df)):
    os_grid_ref = OsGridRef.parse(gridref)
    transformer = pyproj.Transformer.from_crs("EPSG:27700", "EPSG:4326", always_xy=True)
    lon, lat, _ = transformer.transform(os_grid_ref.easting, os_grid_ref.northing, 0)
    df.loc[i, 'DISCHARGE_NGR'] = f"{lon:.6f}, {lat:.6f}"

# save the updated dataframe to a new CSV file
df.to_csv('os_grid_ref.csv', index=False)
