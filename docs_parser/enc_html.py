"""
Смена кодировки в HTML на UTF-8
"""

from os import listdir
from os.path import isfile, join

mypath = "doc_pages/"
filenames = [f for f in listdir(mypath) if isfile(join(mypath, f))]

print(filenames)

for filename in filenames:
    data = ""
    with open(mypath + filename, "r", encoding="utf-8") as rf:
        data = rf.read()

    with open(mypath + filename, "w", encoding="utf-8") as wf:
        data = data.encode("iso-8859-1").decode("utf-8")
        wf.write(data)
    print(filename)
