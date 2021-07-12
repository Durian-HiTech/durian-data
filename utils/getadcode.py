import json
data =  json.load(open("ChinaMap.json","r",encoding="utf-8"))
res = {}
for item in data["features"]:
    res[item["properties"]["name"]] = item["properties"]["adcode"]
print(res)

json.dump(res,open("provincezhname2adcode.json","w",encoding="utf-8"),ensure_ascii=False)