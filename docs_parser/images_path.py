"""
Получение url изображений из документации
"""

import json
from os import listdir
from os.path import isfile, join

from lxml import html

doc_path = "doc_pages/"
img_path = "imgs/"
onlyfiles = [f for f in listdir(doc_path) if isfile(join(doc_path, f))]

# print(onlyfiles)

file_with_img = {}
imgs_urls = []
root_url = ""

img_count = 0

for filename in onlyfiles:
    data = ""
    with open(doc_path + filename, "r", encoding="utf-8") as rf:
        data = rf.read()

    page_code = html.fromstring(data)
    urls = page_code.xpath("//img/@src")
    urls = list(set(urls))
    img_urls = list(
        filter(lambda x: x if x.startswith("/help/assets/images/") else None, urls)
    )
    img_urls = ["https://www.rustore.ru" + url for url in img_urls]

    img_count += len(img_urls)
    file_with_img[
        "https://www.rustore.ru/help/" + filename.replace(".html", "").replace("_", "/")
    ] = img_urls
    imgs_urls.extend(img_urls)

print(f"Количество изображений из документации: {img_count}")

with open("result.json", "w", encoding="utf-8") as wf:
    wf.write(json.dumps(file_with_img, indent=4))

with open("result_list.json", "w", encoding="utf-8") as wf:
    wf.write(json.dumps(imgs_urls, indent=4))
