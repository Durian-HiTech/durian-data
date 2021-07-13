import json

def cmp(a):
    return a["value"]

data = json.load(open('World.json',"r",encoding="utf-8"))
out = {}
for item in data["features"]:
    enname = item["properties"]["NAME"]
    zhname = item["properties"]["CHINESE_NAME"]
    out[enname] = zhname



json.dump(out,open("countryen2zh2.json","w",encoding="utf-8"),ensure_ascii=False)