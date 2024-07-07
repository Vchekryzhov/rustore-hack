"""
Получение HTML страниц документации
"""

import os
import time

import requests
from lxml import etree


doc_html_foldername = "doc_pages/"
doc_parse_timeout_s = 10

doc_url_list = []


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

r = requests.get("https://www.rustore.ru/help/sitemap.xml")
xml = r.text
# print(xml)

root = etree.fromstring(xml.encode("utf-8"))
print(f"Количество страниц документации: {len(root)}")
for sitemap in root:
    children = sitemap.getchildren()
    doc_url_list.append(children[0].text)

if not os.path.exists(doc_html_foldername):
    os.makedirs(doc_html_foldername)

for doc_url in doc_url_list:
    page = requests.get(doc_url, headers=headers)
    doc_filename = (
        doc_html_foldername + doc_url.split("help/")[1].replace("/", "_") + ".html"
    )
    r.encoding = "utf-8"
    with open(doc_filename, "w", encoding="utf-8") as wf:
        wf.write(page.text)
    time.sleep(doc_parse_timeout_s)
