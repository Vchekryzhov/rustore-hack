"""
Получение изображений из документации
"""

import json
import os
import shutil
import time

import requests


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "dnt": "1",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "sec-gpc": "1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
}

images_foldername = "images/"
img_parse_timeout_s = 4

img_urls = {}
with open("result_list.json", "r", encoding="utf-8") as rf:
    img_urls = json.loads(rf.read())

if not os.path.exists(images_foldername):
    os.makedirs(images_foldername)

img_counter = 0
img_count = len(img_urls)

for img_url in img_urls:
    page = requests.get(img_url, headers=headers, stream=True)
    img_filename = images_foldername + img_url.split("help/")[1].replace("/", "_")
    with open(img_filename, "wb") as wf:
        shutil.copyfileobj(page.raw, wf)
    img_counter += 1
    print(f"Скачано {img_counter}/{img_count}")
    time.sleep(img_parse_timeout_s)
