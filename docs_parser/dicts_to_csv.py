"""
Преобразование JSON файлов в CSV
"""

import csv
import json

data_with_url = ""
with open("result.json", "r", encoding="utf-8") as rf:
    data_with_url = json.loads(rf.read())

data = ""
with open("img_url_text.json", "r", encoding="utf-8") as rf:
    data = json.loads(rf.read())

result = []

for page in data_with_url:
    for img in data_with_url[page]:
        try:
            result.append([page, img, data[img]])
        except KeyError:
            continue

header = ["Page", "Image", "Content"]

with open("result.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(result)
