"""
Перевод HTML в Markdown
"""

import csv
from os import listdir
from os.path import isfile, join

from markdownify import markdownify as md

doc_path = "doc_pages/"
md_doc_path = "md_pages/"
doc_filepaths = [f for f in listdir(doc_path) if isfile(join(doc_path, f))]

result = []

for filename in doc_filepaths:
    with open(doc_path + filename, "r", encoding="utf-8") as rf:
        data = rf.read()
    res = md(data).replace("\n\n", "").split("![](https://mc.yandex.ru/watch/89370833)")
    res[1] = "\n".join([x for x in res[1].split("\n") if ";base64," not in x])
    result.append(
        [
            "https://www.rustore.ru/help/" + filename.rstrip(".html").replace("_", "/"),
            res[1].strip(),
            res[0].strip(),
        ]
    )

header = ["Page", "Content", "Title"]

with open("page_result.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, escapechar="\\")
    writer.writerow(header)
    writer.writerows(result)
