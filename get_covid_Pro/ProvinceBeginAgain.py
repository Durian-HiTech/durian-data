import requests
import json
import os
from urllib import parse
from datetime import datetime
import time
import sched
import pymysql

###本程序是从all_minified中获取省数据的办法
### 认证 更新covid_province系列表哥

### 读入信息
headers = {
    'content-type': 'application/json',
}
data = {}
Temp = json.load(open("all_minified.json","r",encoding = "utf-8"))
typeType = ["cases","deaths","recovered"]
typeType2 = ["confirmedCount", "deadCount", "curedCount"]
###

### 处理信息
CountryList = ['Global','South Korea','United Arab Emirates','United Kingdom','United States of America']
URL = 'https://disease.sh/v3/covid-19/vaccine/coverage/countries?lastdays=all'
res = requests.get(URL, headers=headers)
for term in json.loads(res.content):
    CountryList.append(term['country'])
for itemT in Temp:
    if itemT in typeType2:
        data[itemT] = Temp[itemT]
    else:
        print(Temp[itemT]["ENGLISH"])
        if Temp[itemT]["ENGLISH"] in CountryList:
            data[itemT] = Temp[itemT]
###

### 数据库操作
conn = pymysql.connect(
    host="rm-uf6ji600qianqe6921o.mysql.rds.aliyuncs.com",
    port=3306,
    user="buaase2021",password="buaase(2021)",
    database="durian",
    charset="utf8")

cursor = conn.cursor() 

####创建数据库
for type1 in typeType:
    '''
    try:
        cursor.execute('drop table Covid_Province_%s'%type1)
    except:
        print("删除失败")
    '''
    try:
        cursor.execute('create table Covid_Province_%s(date datetime,country_name varchar(1000),info text,primary key(date,country_name))'%type1)
    except:
        print("创建失败")

for countryname in data: # 英国
    if countryname in ["中国"]:
        continue
    if countryname in ["confirmedCount", "deadCount", "curedCount","ENGLISH","全球"]:
        continue
    for date in data["全球"]["confirmedCount"]:
        InfoCases = {}
        InfoDeaths = {}
        InfoRecovered = {}
        nameCountry = []
        for countrylittle in data[countryname]: # 英格兰
            if countrylittle in ["confirmedCount", "deadCount", "curedCount","ENGLISH"]:
                continue 
            nameCountry.append(countrylittle)
            # print(countrylittle)
            eng = data[countryname][countrylittle]["ENGLISH"]  
            if date in data[countryname][countrylittle]["confirmedCount"]:
                InfoCases[eng] = data[countryname][countrylittle]["confirmedCount"][date]
            else:
                InfoCases[eng] = 0
            if date in data[countryname][countrylittle]["deadCount"]:
                InfoDeaths[eng] = data[countryname][countrylittle]["deadCount"][date]
            else:
                InfoDeaths[eng] = 0
            if date in data[countryname][countrylittle]["curedCount"]:
                InfoRecovered[eng] = data[countryname][countrylittle]["curedCount"][date]
            else:
                InfoRecovered[eng] = 0
        print(date,countryname,"  ",nameCountry)
        try:
            cursor.execute('insert into Covid_Province_cases(date,country_name,info) values (\'%s\',\'%s\',\'%s\')'%(date,data[countryname]["ENGLISH"],json.dumps(InfoCases)))
            conn.commit()
        except:
            print("Cases插入失败")
        try:
            cursor.execute('insert into Covid_Province_deaths(date,country_name,info) values (\'%s\',\'%s\',\'%s\')'%(date,data[countryname]["ENGLISH"],json.dumps(InfoDeaths)))
            conn.commit()
        except:
            print("Deaths插入失败")
        try:
            cursor.execute('insert into Covid_Province_recovered(date,country_name,info) values (\'%s\',\'%s\',\'%s\')'%(date,data[countryname]["ENGLISH"],json.dumps(InfoRecovered)))
            conn.commit()
        except:
            print("Recovered插入失败")

### 中国大陆特例
countryname = "中国"
countrysmall = "中国大陆"
for date in data["全球"]["confirmedCount"]:
    InfoCases = {}
    InfoDeaths = {}
    InfoRecovered = {}
    nameCountry = []
    for countrylittle in data[countryname][countrysmall]: # 英格兰
        if countrylittle in ["confirmedCount", "deadCount", "curedCount","ENGLISH"]:
            continue 
        nameCountry.append(countrylittle)
        # print(countrylittle)
        eng = data[countryname][countrysmall][countrylittle]["ENGLISH"]  
        if date in data[countryname][countrysmall][countrylittle]["confirmedCount"]:
            InfoCases[eng] = data[countryname][countrysmall][countrylittle]["confirmedCount"][date]
        else:
            InfoCases[eng] = 0
        if date in data[countryname][countrysmall][countrylittle]["deadCount"]:
            InfoDeaths[eng] = data[countryname][countrysmall][countrylittle]["deadCount"][date]
        else:
            InfoDeaths[eng] = 0
        if date in data[countryname][countrysmall][countrylittle]["curedCount"]:
            InfoRecovered[eng] = data[countryname][countrysmall][countrylittle]["curedCount"][date]
        else:
            InfoRecovered[eng] = 0
    print(date,countryname,"  ",nameCountry)
    try:
        cursor.execute('insert into Covid_Province_cases(date,country_name,info) values (\'%s\',\'%s\',\'%s\')'%(date,data[countryname]["ENGLISH"],json.dumps(InfoCases)))
        conn.commit()
    except:
        print("Cases插入失败")
    try:
        cursor.execute('insert into Covid_Province_deaths(date,country_name,info) values (\'%s\',\'%s\',\'%s\')'%(date,data[countryname]["ENGLISH"],json.dumps(InfoDeaths)))
        conn.commit()
    except:
        print("Deaths插入失败")
    try:
        cursor.execute('insert into Covid_Province_recovered(date,country_name,info) values (\'%s\',\'%s\',\'%s\')'%(date,data[countryname]["ENGLISH"],json.dumps(InfoRecovered)))
        conn.commit()
    except:
        print("Recovered插入失败")

###

###港澳台特例
countryname = "中国"
for countrysmall in data[countryname]:
    if countrysmall in ["confirmedCount", "deadCount", "curedCount","ENGLISH","中国大陆"]:
        continue
    for date in data["全球"]["confirmedCount"]:
        InfoCases = {}
        InfoDeaths = {}
        InfoRecovered = {}
        nameCountry = []
        for countrylittle in data[countryname][countrysmall]: # 英格兰
            if countrylittle in ["confirmedCount", "deadCount", "curedCount","ENGLISH"]:
                continue 
            nameCountry.append(countrylittle)
            # print(countrylittle)
            eng = data[countryname][countrysmall][countrylittle]["ENGLISH"]  
            if date in data[countryname][countrysmall][countrylittle]["confirmedCount"]:
                InfoCases[eng] = data[countryname][countrysmall][countrylittle]["confirmedCount"][date]
            else:
                InfoCases[eng] = 0
            if date in data[countryname][countrysmall][countrylittle]["deadCount"]:
                InfoDeaths[eng] = data[countryname][countrysmall][countrylittle]["deadCount"][date]
            else:
                InfoDeaths[eng] = 0
            if date in data[countryname][countrysmall][countrylittle]["curedCount"]:
                InfoRecovered[eng] = data[countryname][countrysmall][countrylittle]["curedCount"][date]
            else:
                InfoRecovered[eng] = 0
        print(date,countryname,"  ",nameCountry)
        try:
            cursor.execute('insert into Covid_Province_cases(date,country_name,info) values (\'%s\',\'%s\',\'%s\')'%(date,data[countryname][countrysmall]["ENGLISH"],json.dumps(InfoCases)))
            conn.commit()
        except:
            print("Cases插入失败")
        try:
            cursor.execute('insert into Covid_Province_deaths(date,country_name,info) values (\'%s\',\'%s\',\'%s\')'%(date,data[countryname][countrysmall]["ENGLISH"],json.dumps(InfoDeaths)))
            conn.commit()
        except:
            print("Deaths插入失败")
        try:
            cursor.execute('insert into Covid_Province_recovered(date,country_name,info) values (\'%s\',\'%s\',\'%s\')'%(date,data[countryname][countrysmall]["ENGLISH"],json.dumps(InfoRecovered)))
            conn.commit()
        except:
            print("Recovered插入失败")
###


cursor.close()
conn.close()   