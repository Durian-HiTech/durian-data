import requests
import json
import os
import wget

### 认证 下载all_minified.json


headers = {
    'content-type': 'application/json',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
}

url = 'https://covid19.health/data/all_minified.json'

response = requests.get(url, headers=headers)

print(type(response.content))
a = response.content.decode()
print(type(a))

b = json.loads(a)
print(b.keys())

CountryList = []

for itemT in b:
    if itemT in [ 'confirmedCount', 'curedCount', 'deadCount']:
        continue
    CountryList.append(b[itemT]["ENGLISH"])

print(CountryList)

# print("hello",b["中国"]["中国大陆"]["浙江省"]['confirmedCount'])

file = open("./all_minified.json",'w')
print(a,file=file)
file.close()

'''
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'}
url = 'https://covid19.health/data/all_minified.json'
file_name = wget.download(url, headers=headers)
print(file_name)
'''