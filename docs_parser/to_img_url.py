"""
Перевод названий изображений в URL
"""

import json

data = ""
with open("img_text.json", "r", encoding="utf-8") as rf:
    data = json.loads(rf.read())

result = {}

for x, d in enumerate(data.items()):
    if d[1] == "":
        continue
    result["https://www.rustore.ru/help/" + d[0].replace("_", "/")] = d[1]

with open("img_url_text.json", "w", encoding="utf-8") as wf:
    wf.write(json.dumps(result, indent=4))
