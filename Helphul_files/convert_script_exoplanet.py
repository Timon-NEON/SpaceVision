from math import *
import pandas as pd
from csv import DictReader, DictWriter
import re

mean_magnitude = 7.856698241478249

def round_sig(x, sig=1):
    return round(x, sig - int(floor(log10(abs(x)))) - 1)

def get_radius(apparent_magnitude, P=0.1):
    return P * min(mean_magnitude / apparent_magnitude, 1.5)

start = 1
end = 100
input_name = 'nasa'
output_clear = 'exoplanet'
header = ['id', 'name', 'x', 'y', 'z']
writer = DictWriter(open(output_clear + ".csv", "w+", encoding="utf-8", newline=""), fieldnames=header)
writer.writeheader()


data = DictReader(open(input_name+ ".csv", "r", encoding="utf-8"))
data_entries = []
re_query = "(?<=object_id=)([^&]*)(?=&)?"
id = 1
for line in data:
    object_id = id
    id += 1
    data_entries.append(
        {
            "id": object_id,
            "right ascension": line["rastr"],
            "declination": line["decstr"],
            "distance": line["sy_dist"],
            "name": line["pl_name"],
        }
    )

res_list = []
id = 1
for entry in data_entries:
    if (entry["distance"] == ''):
        continue
    res = {
        "id": id,
        "name": entry["name"],
    }
    id += 1

    H = float(entry["right ascension"].split("h")[0])
    M = float(entry["right ascension"].split("h")[1].split("m")[0])
    S = float(entry["right ascension"].split("m")[1].split("s")[0])

    A = float(entry["declination"].split("d")[0])
    B = float(entry["declination"].split("d")[1].split("m")[0])
    C = float(entry["declination"].split("m")[1].split("s")[0])

    d = float(entry["distance"])

    res["x"] = d * cos((A + B / 60 + C / 3600) * (pi / 180)) * cos(((H + M / 60 + S / 3600) * 15) * (pi / 180))
    res["y"] = d * cos((A + B / 60 + C / 3600) * (pi / 180)) * sin(((H + M / 60 + S / 3600) * 15) * (pi / 180))
    res["z"] = d * sin((A + B / 60 + C / 3600) * (pi / 180))
    res_list.append(res)

writer.writerows(res_list)


df = pd.read_csv(output_clear + '.csv')
df.to_csv(output_clear + '.csv', index=False, header = None)
