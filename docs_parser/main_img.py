"""
Получение текста из изображений документации
"""

import json
from os import listdir
from os.path import isfile, join

import tesserocr
from tesserocr import PyTessBaseAPI

print(tesserocr.tesseract_version())
print(tesserocr.get_languages("langs/"))

images = []

img_path = "images/"
images = [f for f in listdir(img_path) if isfile(join(img_path, f))]


result = {}

img_count = len(images)
img_counter = 0

with PyTessBaseAPI(path="langs/", lang="rus") as api:
    for img in images:
        api.SetImageFile(img_path + img)
        text = api.GetUTF8Text()
        result[img] = text
        img_counter += 1
        print(f"Обработано {img_counter}/{img_count}")
        # print(api.AllWordConfidences())

with open("img_text.json", "w", encoding="utf-8") as wf:
    wf.write(json.dumps(result, indent=4))
