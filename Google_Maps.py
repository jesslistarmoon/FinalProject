import requests
import random
import sqlite3
import os

AllBrooklyn = [11201,11202,11203,11204,11205,11206,11207,11208,11209,11210,11211,11212,11213,11214,11215,11216,11217,11218,11219,11220,11221,11222,11223,11224,11225,11226,11228,11229,11230,11231,11232,11233,11234,11235,11236,11237,11238,11239,11240,11241,11242,11243,11247,11249,11252,11252,11256]
AllManhattan = [10001, 10002, 10003, 10004, 10005, 10006, 10007, 10009, 10010, 10011, 10012, 10013, 10014, 10016, 10017, 10018, 10019, 10020, 10021, 10022, 10023, 10024, 10025, 10026, 10027, 10028, 10029, 10030, 10031, 10032, 10033, 10034, 10035, 10036, 10037, 10038, 10039, 10040, 10044, 10065, 10069, 10075, 10103, 10110, 10111, 10112, 10115, 10119, 10123, 10128, 10152, 10153, 10154, 10162, 10165, 10166, 10167, 10168, 10169, 10170, 10171, 10172, 10173, 10174, 10177, 10199, 10271, 10278, 10279, 10280, 10282]
AllQueens = [11001, 11004, 11005, 11040, 11096, 11101, 11102, 11103, 11104, 11105, 11106, 11109, 11351, 11354, 11355, 11356, 11357, 11358, 11359, 11360, 11361, 11362, 11363, 11364, 11365, 11366, 11367, 11368, 11369, 11370, 11371, 11372, 11373, 11374, 11375, 11377, 11378, 11379, 11385, 11411, 11412, 11413, 11414, 11415, 11416, 11417, 11418, 11419, 11420, 11421, 11422, 11423, 11426, 11427, 11428, 11429, 11430, 11432, 11433, 11434, 11435, 11436, 11451, 11691, 11692, 11693, 11694, 11695, 11697]
AllBronx = [10451, 10452, 10453, 10454, 10455, 10456, 10457, 10458, 10459, 10460, 10461, 10462, 10463, 10464, 10465, 10466, 10467, 10468, 10469, 10470, 10471, 10472, 10473, 10474, 10475]
AllStatenIsland = [10301, 10302, 10303, 10304, 10305, 10306, 10307, 10308, 10309, 10310, 10311, 10312, 10313, 10314]

API_KEY = "YAIzaSyDoqB0LkalbSFcoDhZVkdf8MnBg63Kx2z0"

# Keep this as-is to create the database and write to a .txt file

def make_database(file_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + file_name + ".db")
    cur = conn.cursor()
    with open(f"{file_name}.txt", "w") as file:
        file.write("Calculation File:\n\n")
    return cur, conn

# Modified to allow multiple executions with limit ≤ 25, and no duplicate ZIPs

def convertZip(zip_list, cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS zips_and_coordinates (id INTEGER PRIMARY KEY AUTOINCREMENT, zip INTEGER UNIQUE, lat REAL, long REAL)")

    inserted_zips = set(row[0] for row in cur.execute("SELECT zip FROM zips_and_coordinates").fetchall())

    works = []
    for code in zip_list:
        if code in inserted_zips:
            continue
        url = f'https://maps.googleapis.com/maps/api/geocode/json?address={code}&key={API_KEY}'
        r = requests.get(url).json()
        if r.get("results"):
            location = r['results'][0]['geometry']['location']
            works.append((code, location['lat'], location['lng']))
        if len(works) >= 25:
            break

    for zip_code, lat, lng in works:
        cur.execute("INSERT OR IGNORE INTO zips_and_coordinates (zip, lat, long) VALUES (?, ?, ?)", (zip_code, lat, lng))

    conn.commit()
    print("Zip and coordinates stored successfully")
