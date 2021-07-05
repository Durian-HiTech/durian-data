import json

def cmp(a):
    return a["value"]

data = json.load(open('World.json',"r",encoding="utf-8"))
out = []
for item in data["features"]:
    enname = item["properties"]["NAME"]
    zhname = item["properties"]["CHINESE_NAME"]
    out.append({
        "value":enname,
        "label":zhname
    })
out.sort(key = lambda x :cmp(x))

json.dump(out,open("countryen2zh.json","w",encoding="utf-8"),ensure_ascii=False)