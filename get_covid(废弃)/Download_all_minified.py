import requests
import json
import os

# 下载  all_minified.json

headers = {
    'content-type': 'application/json',
}

url = 'https://covid19.health/data/all_minified.json'

response = requests.get(url, headers=headers)

print(type(response.content))
a = response.content.decode()
print(type(a))

b = json.loads(a)
print(b.keys())

# print("hello",b["中国"]["中国大陆"]["浙江省"]['confirmedCount'])

file = open("./all_minified.json",'w')
print(a,file=file)
file.close()