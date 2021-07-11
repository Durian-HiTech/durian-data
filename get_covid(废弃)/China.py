import requests
import json
import os
from urllib import parse
from datetime import datetime
import time
import sched
import pymysql

###本程序是从all_minified中获取省数据的办法

### 读入信息
headers = {
    'content-type': 'application/json',
}

url = 'https://covid19.health/data/all_minified.json'

response = requests.get(url, headers=headers)

data = json.loads(response.content.decode())

# data = json.load(open("all_minified.json","r",encoding = "utf-8"))
typeType = ["cases","deaths","recovered"]
typeType2 = ["confirmedCount", "deadCount", "curedCount"]
###

### 处理信息

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
        cursor.execute('drop table Covid_China_%s'%type1)
    except:
        print("删除失败")
    '''
    try:
        cursor.execute('create table Covid_China_%s(date datetime,province_name varchar(1000),info int,primary key(date,province_name))'%type1)
    except:
        print("创建失败")


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

        try:
            cursor.execute('insert into Covid_China_cases(date,province_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname][countrysmall][countrylittle]["ENGLISH"],InfoCases[eng]))
            conn.commit()
        except:
            a = 1
            #print("Cases插入失败")
        try:
            cursor.execute('insert into Covid_China_deaths(date,province_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname][countrysmall][countrylittle]["ENGLISH"],InfoDeaths[eng]))
            conn.commit()
        except:
            a = 1
            #print("Deaths插入失败")
        try:
            cursor.execute('insert into Covid_China_recovered(date,province_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname][countrysmall][countrylittle]["ENGLISH"],InfoRecovered[eng]))
            conn.commit()
        except:
            a = 1
            #print("Recovered插入失败")        
    print(date,countryname,"  ",nameCountry)

###


###港澳台特例
countryname = "中国"
for countrysmall in data[countryname]: #香港，台湾，澳门
    if countrysmall in ["confirmedCount", "deadCount", "curedCount","ENGLISH","中国大陆"]:
        continue
    for date in data["全球"]["confirmedCount"]:
        InfoCases = {}
        InfoDeaths = {}
        InfoRecovered = {}
        nameCountry = []


        eng = data[countryname][countrysmall]["ENGLISH"]  
        if date in data[countryname][countrysmall]["confirmedCount"]:
            InfoCases[eng] = data[countryname][countrysmall]["confirmedCount"][date]
        else:
            InfoCases[eng] = 0
        if date in data[countryname][countrysmall]["deadCount"]:
            InfoDeaths[eng] = data[countryname][countrysmall]["deadCount"][date]
        else:
            InfoDeaths[eng] = 0
        if date in data[countryname][countrysmall]["curedCount"]:
            InfoRecovered[eng] = data[countryname][countrysmall]["curedCount"][date]
        else:
            InfoRecovered[eng] = 0

        try:
            cursor.execute('insert into Covid_China_cases(date,province_name,info) values (\'%s\',\'%s\',%d)'%(date,eng,InfoCases[eng]))
            conn.commit()
        except:
            a = 1
            # print("Cases插入失败")
        try:
            cursor.execute('insert into Covid_China_deaths(date,province_name,info) values (\'%s\',\'%s\',%d)'%(date,eng,InfoDeaths[eng]))
            conn.commit()
        except:
            a = 1
            # print("Deaths插入失败")
        try:
            cursor.execute('insert into Covid_China_recovered(date,province_name,info) values (\'%s\',\'%s\',%d)'%(date,eng,InfoRecovered[eng]))
            conn.commit()
        except:
            a = 1
            # print("Recovered插入失败")
        print(date,countrysmall,"  ",InfoCases[eng],InfoDeaths[eng],InfoRecovered[eng])
###



cursor.close()
conn.close()   
###