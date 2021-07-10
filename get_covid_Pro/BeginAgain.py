import requests
import json
import os
from urllib import parse
from datetime import datetime
import time
import sched
import pymysql

###本程序是从all_minified中获取数据的办法
### 认证 covid系列表格除了vaccine

### 读入信息
headers = {
    'content-type': 'application/json',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
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

for type1 in typeType:

    try:
        cursor.execute('create table Covid_%s(date datetime,country_name varchar(1000),info int,primary key(date,country_name))'%type1)
    except:
        print("创建失败")

for countryname in data:
    if countryname in ["confirmedCount", "deadCount", "curedCount","ENGLISH"]:
        continue
    ### 中国特判
    """
    if countryname == "中国":
        continue
    """
    ###

    for date in data["全球"]["confirmedCount"]:
        # print(data[countryname]["ENGLISH"])
        if date not in data[countryname]["confirmedCount"]:
            print(date,countryname,0,"confirmed")
            try:
                cursor.execute('insert into Covid_cases(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname]["ENGLISH"],0))
                conn.commit()   
            except:
                print("插入失败")
        else:
            print(date,countryname,data[countryname]["confirmedCount"][date],"confirmed")
            try:
                cursor.execute('insert into Covid_cases(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname]["ENGLISH"],data[countryname]["confirmedCount"][date]))
                conn.commit()   
            except:
                print("插入失败")    
       

    for date in data["全球"]["confirmedCount"]:
        if date not in data[countryname]["deadCount"]:
            print(date,countryname,0,"dead")
            try:
                cursor.execute('insert into Covid_deaths(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname]["ENGLISH"],0))
                conn.commit()   
            except:
                print("插入失败")
        else:
            print(date,countryname,data[countryname]["deadCount"][date],"dead")
            try:
                cursor.execute('insert into Covid_deaths(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname]["ENGLISH"],data[countryname]["deadCount"][date]))
                conn.commit()   
            except:
                print("插入失败")     

    for date in data["全球"]["confirmedCount"]:
        if date not in data[countryname]["curedCount"]:
            print(date,countryname,0,"cured")
            try:
                cursor.execute('insert into Covid_recovered(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname]["ENGLISH"],0))
                conn.commit()   
            except:
                print("插入失败")
        else:
            print(date,countryname,data[countryname]["curedCount"][date],"cured")
            try:
                cursor.execute('insert into Covid_recovered(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname]["ENGLISH"],data[countryname]["curedCount"][date]))
                conn.commit()   
            except:
                print("插入失败")    

"""
###中国特判
countryname = '中国'
for countrysmall in data[countryname]:
    if countrysmall in ["confirmedCount", "deadCount", "curedCount","ENGLISH"]:
        continue
    
    for date in data["全球"]["confirmedCount"]:
        if date not in data[countryname][countrysmall]["confirmedCount"]:
            print(date,countrysmall,0,"confirmed")
            try:
                if countrysmall == "中国大陆":
                    cursor.execute('insert into Covid_cases(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname]["ENGLISH"],0))
                else:
                    cursor.execute('insert into Covid_cases(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname][countrysmall]["ENGLISH"],0))
                conn.commit()   
            except:
                print("插入失败")
        else:
            print(date,countrysmall,data[countryname]["confirmedCount"][date],"confirmed")
            try:
                if countrysmall == "中国大陆":
                    cursor.execute('insert into Covid_cases(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname]["ENGLISH"],data[countryname][countrysmall]["confirmedCount"][date]))
                else:
                    cursor.execute('insert into Covid_cases(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname][countrysmall]["ENGLISH"],data[countryname][countrysmall]["confirmedCount"][date]))
                conn.commit()   
            except:
                print("插入失败")     
    

    for date in data["全球"]["confirmedCount"]:
        if date not in data[countryname][countrysmall]["deadCount"]:
            print(date,countrysmall,0,"dead")
            try:
                if countrysmall == "中国大陆":
                    cursor.execute('insert into Covid_deaths(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname]["ENGLISH"],0))
                else:
                    cursor.execute('insert into Covid_deaths(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname][countrysmall]["ENGLISH"],0))
                conn.commit()   
            except:
                print("插入失败")
        else:
            print(date,countrysmall,data[countryname]["deadCount"][date],"dead")
            try:
                if countrysmall == "中国大陆":
                    cursor.execute('insert into Covid_deaths(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname]["ENGLISH"],data[countryname][countrysmall]["deadCount"][date]))
                else:
                    cursor.execute('insert into Covid_deaths(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname][countrysmall]["ENGLISH"],data[countryname][countrysmall]["deadCount"][date]))
                conn.commit()   
            except:
                print("插入失败")       

    for date in data["全球"]["confirmedCount"]:
        if date not in data[countryname][countrysmall]["curedCount"]:
            print(date,countrysmall,0,"cured")
            try:
                if countrysmall == "中国大陆":
                    cursor.execute('insert into Covid_recovered(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname]["ENGLISH"],0))
                else:
                    cursor.execute('insert into Covid_recovered(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname][countrysmall]["ENGLISH"],0))
                conn.commit()   
            except:
                print("插入失败")
        else:
            print(date,countrysmall,data[countryname]["curedCount"][date],"cured")
            try:
                if countrysmall == "中国大陆":
                    cursor.execute('insert into Covid_recovered(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname]["ENGLISH"],data[countryname][countrysmall]["curedCount"][date]))
                else:
                    cursor.execute('insert into Covid_recovered(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname][countrysmall]["ENGLISH"],data[countryname][countrysmall]["curedCount"][date]))
                conn.commit()   
            except:
                print("插入失败")       
"""

cursor.close()
conn.close()               
        
###
