import json

def cmp(a):
    return a["value"]

data = json.load(open('./utils/China.json',"r",encoding="utf-8"))
out = []
for item in data["features"]:
    enname = item["properties"]["NAME_1"]
    zhname = item["properties"]["NL_NAME_1"]
    out.append({
        "value":enname,
        "label":zhname
    })
out.sort(key = lambda x :cmp(x))

json.dump(out,open("./utils/china_en2province.json","w",encoding="utf-8"),ensure_ascii=False)