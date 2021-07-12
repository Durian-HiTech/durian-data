import json

def cmp(a):
    return a["value"]

data = json.load(open('provinceen2zh.json',"r",encoding="utf-8"))
res = {}
for item in data:
    enname = item
    zhname = data[item]
    res[zhname] = enname

json.dump(res,open("provincezh2en.json","w",encoding="utf-8"),ensure_ascii=False)