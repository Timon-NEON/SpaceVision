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
input_name = 'data'
output_clear = 'starsdata'
output_overall = 'starsdata'
header = ['id', 'x', 'y', 'z', 'diameter', 'Right ascension', 'Declination', 'distance', 'Constellation', 'name']
writer = DictWriter(open(output_clear + ".csv", "w+", encoding="utf-8", newline=""), fieldnames=header)
writer.writeheader()

for i in range(start, end + 1):
    data = DictReader(open('source/'+input_name + str(i)+ ".csv", "r", encoding="utf-8"))
    data_entries = []
    re_query = "(?<=object_id=)([^&]*)(?=&)?"

    for line in data:
        object_id = re.findall(re_query, line["web-scraper-start-url"])[0]
        data_entries.append(
            {
                "id": object_id,
                "right ascension": line["Right ascension"],
                "declination": line["Declination"],
                "distance": line["Distance"].split("\xa0")[0],
                "name": line["Name"],
                "Right ascension": line["Right ascension"],
                "Declination": line["Declination"],
                "Constellation": line["Constellation"],
                "Apparent magnitude": line["Apparent magnitude"]
            }
        )

    res_list = []

    for entry in data_entries:
        if (entry["distance"] == ""):
            continue
        res = {
            "id": entry["id"],
            "name": entry["name"],
            "distance": entry["distance"],
            "Right ascension": entry["Right ascension"],
            "Declination": entry["Declination"],
            "Constellation": entry["Constellation"]
        }

        H = float(entry["right ascension"].split("h")[0])
        M = float(entry["right ascension"].split("h")[1].split("m")[0])
        S = float(entry["right ascension"].split("m")[1].split("s")[0])

        A = float(entry["declination"].split("Â")[0])
        B = float(entry["declination"].split("°")[1].split("'")[0])
        C = float(entry["declination"].split("°")[1].split("'")[1].split('"')[0])

        d = float(entry["distance"])

        res["x"] = d * cos((A + B / 60 + C / 3600) * (pi / 180)) * cos(((H + M / 60 + S / 3600) * 15) * (pi / 180))
        res["y"] = d * cos((A + B / 60 + C / 3600) * (pi / 180)) * sin(((H + M / 60 + S / 3600) * 15) * (pi / 180))
        res["z"] = d * sin((A + B / 60 + C / 3600) * (pi / 180))
        if (entry["Apparent magnitude"] != '' and float(entry["Apparent magnitude"]) > 0):
            res["diameter"] = get_radius(float(entry["Apparent magnitude"]))
        else:
            res["diameter"] = 0.05
        res_list.append(res)

    writer.writerows(res_list)
    print(i)


df = pd.read_csv(output_clear + '.csv')
df.to_csv(output_clear + '.csv', index=False, header = None)
