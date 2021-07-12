import json

def cmp(a):
    return a["value"]

data = json.load(open('provinceen2zh.json',"r",encoding="utf-8"))
res = {}
for item in data:
    enname = item["value"]
    zhname = item["label"]
    res[enname] = zhname

json.dump(res,open("provinceen2zh.json","w",encoding="utf-8"),ensure_ascii=False)